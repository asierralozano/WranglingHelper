import functools
import os
import sys

from gui_utils.Qt import QtCompat, QtCore, QtGui, QtWidgets
from core.deadline_bootstrap import DeadlineConnection
from core.rules import Rule
from core.utils import time_to_seconds, get_chunk_frames, deep_update
from resources import resource
from view.options import OPTIONS
from view.tag_delegate import TagDelegate
from view.tag_dialog import CreateTagDialog


_RULE_WIDGET_UI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "ui", "rules.ui")


class RuleWidget(QtWidgets.QWidget):

    delete = QtCore.Signal(object)

    def __init__(self, parent=None):
        """This widget corresponds with each Individual Rule that will be applied
        to a Rule.
        It gives a Visual representation of a rule
        
        Args:
            parent (QWidget, optional): Widget's parent. Defaults to None.
        """
        super(RuleWidget, self).__init__(parent=parent)
        QtCompat.loadUi(_RULE_WIDGET_UI, self)

        self.delete_bt.clicked.connect(functools.partial(self.delete.emit, self))

    def get_rule(self):
        """Get the values from the Widget, and give the ``Rule`` rule
        
        Returns:
            tuple: Tuple with all the needed information to create a Rule rule
        """
        key = self.key_le.text()
        operator = self.operators_cb.currentText()
        value = self.value_le.text()
        regex = self.regex_cb.isChecked()
        if not key and not value:
            return None
        return (key, operator, value, regex)

    def set_rule_values(self, key, operator, value, regex):
        """Imports and set the UI with the corresponding values
        
        Args:
            key (str): Key
            operator (str): Operator to use
            value (str): Value
            regex (bool): Used of regex
        """
        self.key_le.setText(key)
        index = self.operators_cb.findText(operator)
        self.operators_cb.setCurrentIndex(index)
        self.value_le.setText(value)
        self.regex_cb.setChecked(regex)


_RULES_WIDGET_UI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "ui", "rules_widget.ui")


class RulesWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """This Widget is a Visual representation of the ``Rule`` object.
        It will be encourage to create the ``Rule`` with the rules and the options
        specified in this Widget
        
        Args:
            parent (QWidget, optional): Parent of the widget. Defaults to None.
        """
        super(RulesWidget, self).__init__(parent=parent)
        QtCompat.loadUi(_RULES_WIDGET_UI, self)    

        self._rule = None
        self._options_widgets = list()
        self._rules_widget = list()
        self._deadline_connection = DeadlineConnection()

        self.add_rule_bt.clicked.connect(self._add_rule)
        self.add_tag_bt.clicked.connect(self._add_tag)

        self._init_ui()

    @property
    def rule(self):
        return self._rule

    @property
    def tags(self):
        return [self.tags_lw.item(row).text() for row in xrange(self.tags_lw.count())]

    def _init_ui(self):
        """Initialize the UI
        """
        self.tags_lw.setItemDelegate(TagDelegate())
        for option in OPTIONS:
            option_obj = option()
            self.options_layout.addRow(option_obj.NAME, option_obj)
            self._options_widgets.append(option_obj)

    def _add_tag(self, tag_name=None, tag_color=None):
        if not tag_name or not tag_color:
            dialog = CreateTagDialog(self)
            dialog.exec_()
            result = dialog.result()
            if result:
                tag_color = dialog._color
                tag_name = dialog._name
            else:
                return

        item = QtWidgets.QListWidgetItem()
        item.setText(tag_name)
        item.setData(QtCore.Qt.BackgroundRole, QtGui.QBrush(QtGui.QColor(tag_color)))
        self.tags_lw.addItem(item)

    def _add_rule(self):
        """Add a ``RuleWidget`` within this Widget
        
        Returns:
            RuleWidget: Rule widget created
        """
        rule_widget = RuleWidget()
        rule_widget.delete.connect(self._delete_rule)
        self._rules_widget.append(rule_widget)

        index = self.rules_layout.count()
        if index != 0:
            index = index - 1
        self.rules_layout.insertWidget(index, rule_widget)

        if index == 0:
            self.rules_layout.addStretch(1)

        return rule_widget

    def _delete_rule(self, rule_widget):
        """Delete a ``RuleWidget`` that was previously added
        
        Args:
            rule_widget (RuleWidget): RuleWidget to take out
        """
        self._rules_widget.remove(rule_widget)
        layout_item_index = self.rules_layout.indexOf(rule_widget)
        layout_item = self.rules_layout.takeAt(layout_item_index)
        layout_item.widget().deleteLater()

        if len(self._rules_widget) == 0:
            while self.rules_layout.count() != 0:
                layout_item = self.rules_layout.takeAt(0)

    def _get_tags(self):
        tags = list()
        for index in xrange(self.tags_lw.count()):
            item = self.tags_lw.item(index)
            text = item.text()
            color = item.data(QtCore.Qt.BackgroundRole).color().name()
            tags.append((text, color))
        return tags

    def get_rule(self):
        """Get the ``RulesWidget`` rules.
        To get that, it iterate through all previously added ``RuleWidget``, and 
        get each rule
        
        Returns:
            list: List of rules
        """
        rules = list()
        for rule_widget in self._rules_widget:
            rule = rule_widget.get_rule()
            if not rule:
                continue
            rules.append(rule)
        return rules

    def get_options(self, job):
        """Get the ``RulesWidget`` options.
        It iterate through all the Options declared
        
        Args:
            job (dict): Deadline Job dict. We need this, because the options can be relative, so
            we need to know some of the Job info
        
        Returns:
            dict: All the options gathered
        """
        options = dict()
        for option in self._options_widgets:
            option_info = option.option_info(job=job)
            if not option_info:
                continue
            options = deep_update(options, option_info)
        return options   

    def create_rule(self, job):
        """It creates a ``Rule`` object with the specified Rules and Options
        
        Args:
            job (dict): Deadline Job dict
        
        Returns:
            Rule: Rule created
        """
        rules = self.get_rule()
        options = self.get_options(job)
        if rules and options:
            self._rule = Rule(rules, options)
        return self._rule

    def export_rule(self):
        """Export the rule in a Dict format
        
        Returns:
            dict: Dictionary containing all the ``RulesWidget`` information
        """
        rule = dict()
        rules = self.get_rule()
        tags = self._get_tags()
        rule["rules"] = rules
        rule["tags"] = tags
        rule["options"] = dict()

        for option in self._options_widgets:
            info = option.export_info()
            name = option.NAME
            rule["options"].setdefault(name, info)

        return rule

    def import_rule(self, rule_data):
        """Imports an previously exported ``RulesWidget``.
        It will set all the UI values to match the exported one
        
        Args:
            rule_data (dict): Previously exported ``RulesWidget``
        """
        rules = rule_data.get("rules")
        options = rule_data.get("options")
        tags = rule_data.get("tags")
        for rule in rules:
            rule_widget = self._add_rule()
            rule_widget.set_rule_values(*rule)
        
        for widget, values in options.iteritems():

            for option in self._options_widgets:
                if option.NAME != widget:
                    continue

                value = values.get("value")
                enabled = values.get("enabled")
                relative = values.get("relative")

                option._handle_enabled_toggle(enabled, force=True)
                option._handle_relative_toggle(relative, force=True)
                option.set_option_value(value)

        for tag in tags:
            name, color = tag
            self._add_tag(name, color)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wh = RulesWidget()
    wh.show()
    app.exec_()        
