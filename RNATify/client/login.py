# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from signup import Ui_signUp
import os
from socket import *
import sys
import subprocess

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


class Ui_Dialog(object):

    def signUpShow(self):
        self.signUpWindow = QtGui.QDialog()
        self.ui = Ui_signUp()
        self.ui.setupUi(self.signUpWindow)
        self.signUpWindow.show()

    def welcomeWindowShow(self):
        """usage of socket module"""
        try:
            host = gethostbyname(gethostname())
            port = 51421
            address = (host, port)
            tcpCliSock = socket(AF_INET, SOCK_STREAM)
            tcpCliSock.connect(address)

            tcpCliSock.send('SONG_TRANSFER')
            data = tcpCliSock.recv(1024)
            tcpCliSock.send('')
            tcpCliSock.close()
            sys.argv = ['songs_Info.db']
            execfile('client.py')
        except error:
            print 'THERE IS NO OPEN RoyTify SERVER IN LAN!'
        subprocess.Popen([sys.executable, 'display.py'],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit()

    def loginCheck(self):
        username = unicode(self.uname_lineEdit.text())
        password = unicode(self.pass_lineEdit.text())

        data = 'USERNAME: ' + username + ' PASSWORD: ' + password

        """usage of socket module"""
        try:
            host = gethostbyname(gethostname())
            port = 51421
            address = (host, port)
            tcpCliSock = socket(AF_INET, SOCK_STREAM)
            tcpCliSock.connect(address)

            tcpCliSock.send(data)
            data = tcpCliSock.recv(1024)
            tcpCliSock.send('')
            tcpCliSock.close()
        except error:
            print 'THERE IS NO OPEN RoyTify SERVER IN LAN!'

        if data == "True":
            print("User Found ! ")

            filer = open(r"my_username.txt", "w")
            filer.write(username)
            filer.close()

            self.welcomeWindowShow()
        else:
            print("User Not Found !")
            Ui_signUp.showMessageBox(Ui_signUp(), 'Warning', 'Invalid Username And Password')

    def signUpCheck(self):
        print(" Sign Up Button Clicked !")
        self.signUpShow()

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(496, 265)
        self.u_name_label = QtGui.QLabel(Dialog)
        self.u_name_label.setGeometry(QtCore.QRect(150, 110, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(50)
        self.u_name_label.setFont(font)
        self.u_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.u_name_label.setObjectName(_fromUtf8("u_name_label"))
        self.pass_label = QtGui.QLabel(Dialog)
        self.pass_label.setGeometry(QtCore.QRect(150, 150, 71, 21))
        self.pass_label.setFont(font)
        self.pass_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pass_label.setObjectName(_fromUtf8("pass_label"))
        self.uname_lineEdit = QtGui.QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QtCore.QRect(230, 110, 113, 20))
        self.uname_lineEdit.setObjectName(_fromUtf8("uname_lineEdit"))
        self.pass_lineEdit = QtGui.QLineEdit(Dialog)
        self.pass_lineEdit.setGeometry(QtCore.QRect(230, 150, 113, 20))
        self.pass_lineEdit.setObjectName(_fromUtf8("pass_lineEdit"))
        self.pass_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.login_btn = QtGui.QPushButton(Dialog)
        self.login_btn.setGeometry(QtCore.QRect(230, 200, 51, 23))
        self.login_btn.setObjectName(_fromUtf8("login_btn"))

        #  ----------------------- Button Event ------------------------------
        self.login_btn.clicked.connect(self.loginCheck)
        #  -------------------------------------------------------------------
        self.signup_btn = QtGui.QPushButton(Dialog)
        self.signup_btn.setGeometry(QtCore.QRect(290, 200, 51, 23))
        self.signup_btn.setObjectName(_fromUtf8("signup_btn"))
        #  ------------------------ Button Event ------------------------------
        self.signup_btn.clicked.connect(self.signUpCheck)
        #  --------------------------------------------------------------------
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(190, 10, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Login Form", None))
        Dialog.setWindowIcon(QtGui.QIcon("useful\Logo.ico"))
        Dialog.setStyleSheet("background-image: url(Squares.jpg);"
                             " background-position: center; color: darkGreen;")

        self.u_name_label.setText(_translate("Dialog", "USERNAME ", None))
        self.pass_label.setText(_translate("Dialog", "PASSWORD", None))
        self.login_btn.setText(_translate("Dialog", "Login", None))
        self.signup_btn.setText(_translate("Dialog", "Sign Up", None))
        self.label.setText(_translate("Dialog", "Login Form", None))


def myExitHandler():
    for i in ["login.pyc", "welcome.pyc", "signup.pyc", "display.pyc"]:
        try:
            os.remove(i)
        except WindowsError:
            pass


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)

    Dialog.show()
    app.aboutToQuit.connect(myExitHandler)
    sys.exit(app.exec_())
