from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import Ui_ui


class ui_Control(QDialog, Ui_ui):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent, fl)
        self.setupUi(self)
