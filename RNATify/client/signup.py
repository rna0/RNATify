# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import sqlite3
import random
import smtplib
import re
import sys
from socket import *

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


def send_email(to_address):
    from_address = 'tcpserversock@gmail.com'
    password = 'serverclient'
    num = str(random.randint(12345, 98765))
    the_message = 'A one-time password has been requested for your user on the RoyTify system' \
                  '\n\nyour password is:\n' + num
    subject = 'RoyTify Email Verification'
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(from_address, password)
        message = 'Subject: {}\n\n{}'.format(subject, the_message)
        server.sendmail(from_address, to_address, message)
        server.quit()
        print("Success: Email sent!")
    except:
        Ui_signUp.showMessageBox(Ui_signUp(), "Error",
                                 "Make sure email is Valid!\n"
                                 "and you are connected to the internet")
        print("Email failed to send.")
        num = '0'
    return num


def check_all(username, email, password):
    b = True

    data = 'CHECK: ' + username

    '''usage of socket module'''
    '''host, port:'''
    try:
        address = (gethostbyname(gethostname()), 51421)
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(address)

        tcpCliSock.send(data)
        data = tcpCliSock.recv(1024)

        tcpCliSock.send('')
        tcpCliSock.close()
    except error:
        print 'THERE IS NO OPEN RoyTify SERVER IN LAN!'

    if data == 'True':
        Ui_signUp.showMessageBox(Ui_signUp(), "UserName",
                                 "USERNAME ALREADY TAKEN")
        b = False

    """check if the username, password and
     email are fitting the requirements"""
    if len(username) > 3 and len(email) > 3 and len(password) > 3:
        if not re.match(r"^[A-Za-z]*$", username):
            Ui_signUp.showMessageBox(Ui_signUp(), "UserName",
                                     "Make sure you only use letters in your username")
            b = False
        if not re.match(r"[A-Za-z0-9@#$%^&+=]", password):
            Ui_signUp.showMessageBox(Ui_signUp(), "Password",
                                     "INVALID USE OF PASSWORD, '_ , . ? -'")
            b = False
    else:
        Ui_signUp.showMessageBox(Ui_signUp(), "Error",
                                 "Make sure all inputs have more than 3 Characters")
        b = False
    return b


class Ui_signUp(QtGui.QWidget):

    def __init__(self):
        super(Ui_signUp, self).__init__()

    def showMessageBox(self, title, message):
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QtGui.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.exec_()

    def insertData(self):
        username = unicode(self.uname_lineEdit.text())
        email = unicode(self.email_lineEdit.text())
        password = unicode(self.password_lineEdit.text())

        if check_all(username, email, password):
            num = send_email(str(email))
            if num != '0':
                start, ok = QtGui.QInputDialog \
                    .getText(self, 'Verify Email',
                             'Email sent\nEnter your verification code')
                if ok:
                    if str(start) == num:

                        data = 'CREATE: ' + username + ' PASSWORD: ' + password + ' EMAIL: ' + email

                        '''usage of socket module'''
                        '''host, port:'''
                        try:
                            address = (gethostbyname(gethostname()), 51421)
                            tcpCliSock = socket(AF_INET, SOCK_STREAM)
                            tcpCliSock.connect(address)

                            tcpCliSock.send(data)
                            tcpCliSock.recv(1024)

                            tcpCliSock.send('')
                            tcpCliSock.close()
                        except error:
                            print 'THERE IS NO OPEN RoyTify SERVER IN LAN!'

                        try:
                            global Dialog
                            Dialog.close()
                        except:
                            print "close manually"
                    else:
                        self.showMessageBox("ERROR", "FAILED VERIFICATION")
                else:
                    self.showMessageBox("NOTICE", "USER ISN'T VERIFIED YET")

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("RoyTify- Create Account"))
        Dialog.resize(570, 375)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(160, 130, 81, 31))

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)

        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(160, 230, 81, 31))

        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(160, 180, 81, 31))

        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.uname_lineEdit = QtGui.QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QtCore.QRect(250, 130, 141, 20))
        self.uname_lineEdit.setObjectName(_fromUtf8("uname_lineEdit"))
        self.email_lineEdit = QtGui.QLineEdit(Dialog)
        self.email_lineEdit.setGeometry(QtCore.QRect(250, 180, 141, 20))
        self.email_lineEdit.setObjectName(_fromUtf8("email_lineEdit"))
        self.password_lineEdit = QtGui.QLineEdit(Dialog)
        self.password_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.password_lineEdit.setGeometry(QtCore.QRect(250, 230, 141, 20))
        self.password_lineEdit.setObjectName(_fromUtf8("password_lineEdit"))
        self.signup_btn = QtGui.QPushButton(Dialog)
        self.signup_btn.setGeometry(QtCore.QRect(270, 290, 75, 23))
        self.signup_btn.setObjectName(_fromUtf8("signup_btn"))

        #  --------------------------- Event -----------------------------
        self.signup_btn.clicked.connect(self.insertData)
        ################################################################
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(150, 10, 321, 81))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "RoyTify- Create Account", None))
        Dialog.setWindowIcon(QtGui.QIcon("useful\Logo.ico"))
        #  Dialog.setStyleSheet(r"border-image: url(useful\back.jpg) 0 0 0 0 stretch stretch;")
        Dialog.setStyleSheet(r"background-image: url(Squares.jpg); background-position: center; color: darkGreen;")

        self.label.setText(_translate("Dialog", "USERNAME", None))
        self.label_2.setText(_translate("Dialog", "PASSWORD", None))
        self.label_3.setText(_translate("Dialog", "EMAIL ID", None))
        self.label_4.setText(_translate("Dialog", "Create Account", None))
        self.signup_btn.setText(_translate("Dialog", "Sign Up", None))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    global Dialog
    Dialog = QtGui.QDialog()
    ui = Ui_signUp()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec_()
