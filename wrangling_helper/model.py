from gui_utils.Qt import QtWidgets, QtCore, QtGui, QtCompat
import sys
import os

from core.utils import send_wrangling_email, export_rule, decode_json
from core.background_process import BackgroundProcess
from view.rule_widget import RulesWidget
from view.console import Console
from resources import resource
from core.qlogging import getQLogger
from addons.priority_importer.core import generate_priority_rules


logger = getQLogger("Wrangling", True)


_MAIN_UI = os.path.join(os.path.dirname(__file__), "resources", "ui", "main.ui")


class WranglingHelper(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(WranglingHelper, self).__init__(parent=parent)
        QtCompat.loadUi(_MAIN_UI, self)

        self._background_process = None
        self._started = False
        self._list_model = self.loaded_rules_lw.model()
        # self._rules_widgets = list()
        self.console = Console()
        self._connect_signals()

    @property
    def rules_widgets(self):
        """A property that hold all loaded rules
        
        Returns:
            list: list of RulesWidgets
        """
        return [self.rules_tabs_widget.widget(x) for x in xrange(self.rules_tabs_widget.count())]

    def _connect_signals(self):
        """Connect default signals
        """
        self.actionNew.triggered.connect(self._create_new_rule)
        self.actionRemove.triggered.connect(self._remove_rule)
        self.actionConsole.triggered.connect(self._show_console)
        self.actionStart.triggered.connect(self.start)
        self.actionExport.triggered.connect(self._export_rule)
        self.actionImport.triggered.connect(self._import_rule)
        self.actionPriority_excel_import.triggered.connect(self._import_priority_rule)
        self.rules_tabs_widget.tabBar().tabMoved.connect(self._tab_moved)
        self._list_model.rowsMoved.connect(self._item_in_list_moved)
        self.loaded_rules_lw.itemDoubleClicked.connect(self._handle_item_double_clicked)
        self.rules_searcher_le.textChanged.connect(self._search_in_list)
        logger.handlers[0].signalHander.logEvent.connect(self.registerLogger)

    def registerLogger(self, log):
        """Insert all log entries into the Console
        
        Args:
            log (str): Log entry
        """
        self.console.console_widget.insertHtml(log)  

    def _tab_moved(self, from_index, to_index):
        """Slot that handle the tabMoved signal. It will reorder also the ListWidget with
        all rules loaded (self.loaded_rules_lw)
        
        Args:
            from_index (int): Index referencing the Source
            to_index (int): Index referencing the target
        """
        self.loaded_rules_lw.clear()
        count = self.rules_tabs_widget.tabBar().count()
        for index in xrange(count):
            tab_name = self.rules_tabs_widget.tabBar().tabText(index)
            self.loaded_rules_lw.addItem(tab_name)

    def _search_in_list(self, text):
        """Filter the loaded rules in the ListWidget based on the text
        
        Args:
            text (str): Search pattern
        """
        if text and self.loaded_rules_lw.count() != 0:
            items = self.loaded_rules_lw.findItems(text, QtCore.Qt.MatchContains)
            # if not items:
            #     return 

            # We need to do this little hacky fix, because if we check if an item is contained in a list
            # an NotImplementedError will occur:
            # if item in items:
            #   NotImplementedError: operator not implemented.
            # https://bugreports.qt.io/browse/PYSIDE-74
            items_ids = list()
            if items:
                items_ids = [id(item) for item in items]

            for row in xrange(self.loaded_rules_lw.count()):
                item = self.loaded_rules_lw.item(row)
                selected = False
                if id(item) in items_ids:
                    selected = True

                tab = self.rules_tabs_widget.widget(row)
                for tag in tab.tags:
                    if text in tag:
                        selected = True
                        break
                item.setSelected(selected)

    def _item_in_list_moved(self, parent, start, end, destination, row):
        """Slot that handle the rowMoved signal from the ListWidget. It will also move the tab within
        the tabbar
        
        Args:
            parent ([type]): [description]
            start ([type]): [description]
            end ([type]): [description]
            destination ([type]): [description]
            row ([type]): [description]
        """
        if row != 0:
            row = row - 1
        self.rules_tabs_widget.tabBar().moveTab(start, row)

    def _handle_item_double_clicked(self, item):
        """Slot that handle the itemDoubleClicked signal from the ListWidget.
        It will select the tab that corresponds to the clicked item
        
        Args:
            item (QListWidgetItem): Double clicked item
        """
        row = self.loaded_rules_lw.row(item)
        self.rules_tabs_widget.setCurrentIndex(row)

    def _import_priority_rule(self):
        """This method handles the import priority Excel
        It will opens a QFileDialog that allows you to choose the file.
        It will import all the priorities rules in individual tabs
        """
        file, filters = QtWidgets.QFileDialog.getOpenFileName(self, "Priority file...")
        if file:        
            for rule in generate_priority_rules(file):
                info = rule.get("info")
                rule_data = rule.get("rule")

                shot = info.get("shot")
                user = info.get("login")
                rule_name = "{} - {}".format(shot, user)

                rule_widget = self._create_new_rule(rule_name)
                rule_widget.import_rule(rule_data)

    def _show_console(self):
        """Shows the Console Widget
        """
        self.console.show()

    def _create_new_rule(self, name=None):
        """Handles the creation of a rule.
        This method is one of the main methods of this class
        If a name is not provided, a prompt will ask you to provide a name.
        It creates a RuleWidget widget
        
        Args:
            name (str, optional): Name of the Rule. Defaults to None.
        
        Returns:
            RuleWidget: The rule created
        """
        accepted = True
        if not name:
            name, accepted = QtWidgets.QInputDialog.getText(self, "Wrangling helper", "Rule name: ")
        if name and accepted:
            rule_widget = RulesWidget()
            self.rules_tabs_widget.addTab(rule_widget, name)
            # self._rules_widgets.append(rule_widget)
            self.loaded_rules_lw.addItem(name)
            return rule_widget
        return None

    def _remove_rule(self):
        """Remove the current focused RuleWidget
        """
        widget = self.rules_tabs_widget.currentWidget()
        index = self.rules_tabs_widget.currentIndex()

        # self._rules_widgets.remove(widget)
        self.rules_tabs_widget.removeTab(index)
        self.loaded_rules_lw.takeItem(index)

    def _results_emitted(self, jobs):
        """This method is called whenever the Background process emits some results
        If the emit it is not empty, it will try to match a rule, and if it matchs, 
        it will apply the specified options
        
        Args:
            jobs (list): List of Deadline Jobs
        """
        if not jobs:
            logger.info("Any job received this time")
            return
        logger.info("Getting {} new jobs!".format(len(jobs)))
        for job in jobs:
            for rule_widget in self.rules_widgets:
                rule = rule_widget.create_rule(job)
                match = rule.job_match_rule(job)
                if not match:
                    continue
                rule.apply_rule_options(job)
                send_wrangling_email(job, rule.options)
                logger.info("Rule {} applied to job {} with ID {}".format(rule.options, job["Props"]["Name"], job["_id"]))

    def _thread_finished(self):
        print("Thread Finished")

    def _export_rule(self):
        """Export the current Rule in a Json file
        """
        widget = self.rules_tabs_widget.currentWidget()
        index = self.rules_tabs_widget.currentIndex()

        tab_name = self.rules_tabs_widget.tabText(index)
        rule = widget.export_rule()
        path = export_rule(tab_name, rule)
        if path:
            QtWidgets.QMessageBox.information(self, "Exported", "File exported in:\n{}".format(path))

    def _import_rule(self):
        """Import a Json file rule.
        """
        file, filters = QtWidgets.QFileDialog.getOpenFileName(self, "Import file...", "T:/framework/settings/wrangling")
        if file:
            rule_data = decode_json(file)
            rule_name = os.path.splitext(os.path.basename(file))[0]
            rule_widget = self._create_new_rule(rule_name)
            rule_widget.import_rule(rule_data)

    def start(self):
        """Main method of this class
        It will create a BackgroundProcess that will be interacting with Deadline.
        The Background process is a Daemon Thread. It will be triggered every 30 secs.
        It will get any new job that is Active (Rendering, Queried) or Pending

        Once this BackgroundProcess timedout, it will automatically pass all the results
        through the method ``_results_emitted``
        """
        if not self._started:
            if not self._background_process:
                only_new_jobs = self.actionWrangler_only_jobs_from_now_on.isChecked()
                self._background_process = BackgroundProcess(only_new_jobs=only_new_jobs, parent=self)
                self._background_process.finished.connect(self._thread_finished)
                self._background_process.emit_results.connect(self._results_emitted)

                self._timer = QtCore.QTimer(self)
                self._timer.setInterval(30000)
                # self._timer.setSingleShot(True)
                self._timer.timeout.connect(self._background_process.start)
            
            self._timer.start()        
            self._started = True
            self.actionStart.setText("Pause")
            self.actionStart.setIcon(QtGui.QIcon(":/icons/light/pause.svg"))
            logger.info("Starting")
        else:
            self._timer.stop()
            self._background_process.terminate()
            self._background_process.wait()
            self.actionStart.setText("Start")
            self.actionStart.setIcon(QtGui.QIcon(":/icons/light/play.svg"))
            self._started = False        
            logger.info("Pausing")
        self.rules_tabs_widget.setDisabled(self._started)   


def initialize():
    app = QtWidgets.QApplication(sys.argv)
    wh = WranglingHelper()
    # wh = BaseOption()
    # wh.start()
    wh.show()
    app.exec_()    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wh = WranglingHelper()
    # wh = BaseOption()
    # wh.start()
    wh.show()
    app.exec_()