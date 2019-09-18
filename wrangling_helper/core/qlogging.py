import logging
import datetime
try:
    from PySide2 import QtCore
except:
    from PySide import QtCore


class SignalHandler(QtCore.QObject):
    """This class will handle the Signal that will emit the log event
    """


    logEvent = QtCore.Signal(str)

    def __init__(self):
        super(SignalHandler, self).__init__()


class QLogger(logging.Handler):
    """This logging.Handler will add the possibility to connect the logger with a text QWidget (like QTextEdit, QLineEdit...)
    To do that, you only need to connect the logger with the widget with the following lines:

        #First we need to get the logger:
            logger = qlogger.getQLogger("SPAChecker", True)
        #Then, we must call the connection method with
            qlogger.connect(logger, YOUR_METHOD_HERE)

    """

    signalHander = SignalHandler()

    def __init__(self, format2Html=False, *args, **kwargs):
        super(QLogger, self).__init__(*args, **kwargs)

        self.format2Html = format2Html

    def emit(self, record):
        if self.format2Html:
            level = record.levelname
            date = datetime.datetime.fromtimestamp(record.created).strftime("%b %d %Y %H:%M:%S")
            color = None
            if level == "INFO":
                color="white"
            elif level == "WARNING":
                color="yellow"
            else:
                color="red"
            msg = '<font color="{color}"><b>{date}:</b> {message}</font><br>'.format(color=color, date=date, message=record.getMessage())
        else:
            msg = record.getMessage()

        self.signalHander.logEvent.emit(msg)

    
def getQLogger(name, html=True):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )    
    logger = logging.getLogger(name)
    handle = QLogger(format2Html=html)
    logger.addHandler(handle)
    return logger


def connect(logger, method):
    logger.handlers[0].signalHander.logEvent.connect(method)