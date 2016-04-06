# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Fri Nov 28 13:52:39 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ui(object):
    def setupUi(self, ui):
        ui.setObjectName("ui")
        ui.resize(335, 194)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../imagemap_plugin/src"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ui.setWindowIcon(icon)
        self.gridlayout = QtGui.QGridLayout(ui)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.label = QtGui.QLabel(ui)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 1, 0, 1, 1)
        self.comboBoxEdificio = QtGui.QComboBox(ui)
        self.comboBoxEdificio.setObjectName("comboBoxEdificio")
        self.gridlayout.addWidget(self.comboBoxEdificio, 5, 0, 1, 1)
        self.comboBoxPlantas = QtGui.QComboBox(ui)
        self.comboBoxPlantas.setObjectName("comboBoxPlantas")
        self.gridlayout.addWidget(self.comboBoxPlantas, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(ui)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(ui)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ui)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 6, 0, 1, 1)

        self.retranslateUi(ui)
	# para cerrar el formulario
	QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),ui.reject)

        QtCore.QMetaObject.connectSlotsByName(ui)

    def retranslateUi(self, ui):
        ui.setWindowTitle(QtGui.QApplication.translate("ui", "Plugin de SIGUA para QGIS", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ui", "Carga de edificios de Sigua", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ui", "Selecciona una planta", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ui", "Selecciona un edificio", None, QtGui.QApplication.UnicodeUTF8))

