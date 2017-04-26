# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_temp.ui'
#
# Created: Thu Jun 30 12:35:29 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1280, 1024)
        self.Frame = QtGui.QLabel(Form)
        self.Frame.setGeometry(QtCore.QRect(100, 40, 600, 600))
        self.Frame.setTextFormat(QtCore.Qt.AutoText)
        self.Frame.setWordWrap(False)
        self.Frame.setObjectName(_fromUtf8("Frame"))
        self.button = QtGui.QPushButton(Form)
        self.button.setGeometry(QtCore.QRect(300, 790, 98, 27))
        self.button.setObjectName(_fromUtf8("button"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.Frame.setText(_translate("Form", "ADARSH", None))
        self.button.setText(_translate("Form", "exit", None))

