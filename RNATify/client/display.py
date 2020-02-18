# -*- coding: utf-8 -*-
# #!/usr/bin/env python

from socket import *
import sys
from PyQt4 import QtCore, QtGui
import sqlite3
import os
from welcome import Ui_MainWindow
from signup import Ui_signUp

try:
    from PyQt4.phonon import Phonon
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "Music Player",
                               "Your Qt installation does not have Phonon support.",
                               QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                               QtGui.QMessageBox.NoButton)
    sys.exit(1)

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


def socket_send(data):
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
        return data
    except error:
        print 'THERE IS NO OPEN RoyTify SERVER IN LAN!'
        return '0.00'


class display_MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(display_MainWindow, self).__init__()
        super(QtGui.QMainWindow, self).__init__()
        self.username = ''
        self.price = 3.90
        self.my_username()
        self.money = socket_send('GETMONEY: ' + self.username)
        self.displayWindowShow()

        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        self.metaInformationResolver = Phonon.MediaObject(self)

        self.mediaObject.setTickInterval(1000)

        self.mediaObject.tick.connect(self.tick)
        self.mediaObject.stateChanged.connect(self.stateChanged)
        self.metaInformationResolver.stateChanged.connect(self.metaStateChanged)
        self.mediaObject.currentSourceChanged.connect(self.sourceChanged)
        self.mediaObject.aboutToFinish.connect(self.aboutToFinish)

        Phonon.createPath(self.mediaObject, self.audioOutput)

        self.setup_actions()
        self.setup_ui()
        self.setup_menus()
        self.time_lcd.display("00:00")

        self.sources = []
        self.indexer = []

        self.addFiles_Discover()

    def my_username(self):
        try:
            filer = open(r"my_username.txt", "r")
            self.username = filer.read()
            filer.close()
            os.remove('my_username.txt')
        except IOError:
            print 'NO ASSIGNMENT'
            self.username = "anonymous"

    def addFiles(self):
        files = QtGui.QFileDialog.getOpenFileNames(self, "Select Music Files",
                                                   QtGui.QDesktopServices.storageLocation(
                                                       QtGui.QDesktopServices.MusicLocation))
        if not files:
            return

        index = len(self.sources)

        for string in files:
            self.sources.append(Phonon.MediaSource(string))

        if self.sources:
            self.metaInformationResolver.setCurrentSource(self.sources[index])

    def addFiles_playList(self):
        try:
            connection = sqlite3.connect("songs_info.db")
            songs = (connection.execute("SELECT * FROM SONGS")).fetchall()
            j = 0

            for song in self.indexer:
                self.musicTable.setRowCount(len(songs))
                self.musicTable.setColumnCount(4)
                self.musicTable.setItem(j, 0, QtGui.QTableWidgetItem(songs[song][0]))
                self.musicTable.setItem(j, 1, QtGui.QTableWidgetItem(songs[song][1]))
                self.musicTable.setItem(j, 2, QtGui.QTableWidgetItem(songs[song][2]))
                self.musicTable.setItem(j, 3, QtGui.QTableWidgetItem(songs[song][3]))
                j += 1

        except IndexError:
            print 'no Discover'

    def addFiles_Discover(self):
        try:
            connection = sqlite3.connect("songs_info.db")
            songs = (connection.execute("SELECT * FROM SONGS")).fetchall()
            j = 0

            for song in songs:
                self.musicTable_1.setRowCount(len(songs))
                self.musicTable_1.setColumnCount(4)
                self.musicTable_1.setItem(j, 0, QtGui.QTableWidgetItem(song[0]))
                self.musicTable_1.setItem(j, 1, QtGui.QTableWidgetItem(song[1]))
                self.musicTable_1.setItem(j, 2, QtGui.QTableWidgetItem(song[2]))
                self.musicTable_1.setItem(j, 3, QtGui.QTableWidgetItem(str(self.price) + '$'))
                j += 1

        except IndexError:
            print 'no Discover'

    def about(self):
        QtGui.QMessageBox.information(self, "About Music Player",
                                      "The royTify project is original, no copyrights and all rights reserved, "
                                      "the multimedia framework that comes with Qt - to create a "
                                      "simple music player is amazing and that is the reason i could make such "
                                      "a beautiful project."
                                      "\n* if you are getting as anonymous as account all you can do is play files "
                                      "from your system")

    def stateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            if self.mediaObject.errorType() == Phonon.FatalError:
                QtGui.QMessageBox.warning(self, "Fatal Error",
                                          self.mediaObject.errorString())
            else:
                QtGui.QMessageBox.warning(self, "Error",
                                          self.mediaObject.errorString())

        elif newState == Phonon.PlayingState:
            self.playAction.setEnabled(False)
            self.pauseAction.setEnabled(True)
            self.stopAction.setEnabled(True)

        elif newState == Phonon.StoppedState:
            self.stopAction.setEnabled(False)
            self.playAction.setEnabled(True)
            self.pauseAction.setEnabled(False)
            self.time_lcd.display("00:00")

        elif newState == Phonon.PausedState:
            self.pauseAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.playAction.setEnabled(True)

    def tick(self, time):
        displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.time_lcd.display(displayTime.toString('mm:ss'))

    def tableClicked(self, row, column):
        try:
            wasPlaying = (self.mediaObject.state() == Phonon.PlayingState)

            self.mediaObject.stop()
            self.mediaObject.clearQueue()

            self.mediaObject.setCurrentSource(self.sources[row])

            if wasPlaying:
                self.mediaObject.play()
            else:
                self.mediaObject.stop()
        except IndexError:
            connection = sqlite3.connect("songs_info.db")
            index_play = self.musicTable.currentRow()
            name = (connection.execute("SELECT * FROM SONGS")).fetchall()[self.indexer[index_play]]
            name1 = name[3][0:-5] + name[1] + ' - ' + name[0] + '.mp3'
            print name1
            socket_send('SONG_TRANSFER')
            sys.argv = [name1]
            execfile('client.py')

            index = len(self.sources)
            self.sources.append(Phonon.MediaSource(name1.split('\\')[-1]))
    
            if self.sources:
                self.metaInformationResolver.setCurrentSource(self.sources[index])

    def tableClickedDisover(self, row, column):

        indexit = self.musicTable_1.currentRow()
        connection = sqlite3.connect("songs_info.db")
        name = (connection.execute("SELECT * FROM SONGS")).fetchall()[indexit][0]
        try:
            print self.indexer.index(indexit)
            Ui_signUp.showMessageBox(Ui_signUp(), 'Notice', self.username + ', \nyou have already bought ' + name)
        except ValueError:
            if float(str(self.textEdit.toPlainText())) < self.price:
                Ui_signUp.showMessageBox(Ui_signUp(), 'Notice',
                                         self.username + ', \nyou have less money than needed for ' + name)
            else:
                self.textEdit.setText(str(float(str(self.textEdit.toPlainText())) - self.price))
                self.indexer.append(indexit)
                self.addFiles_playList()

    def sourceChanged(self, source):
        self.musicTable.selectRow(self.sources.index(source))
        self.time_lcd.display('00:00')

    def metaStateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            QtGui.QMessageBox.warning(self, "Error opening files",
                                      self.metaInformationResolver.errorString())

            while self.sources and self.sources.pop() != self.metaInformationResolver.currentSource():
                pass

            return

        if newState != Phonon.StoppedState and newState != Phonon.PausedState:
            return

        if self.metaInformationResolver.currentSource().type() == Phonon.MediaSource.Invalid:
            return

        metaData = self.metaInformationResolver.metaData()
        """ searching by featching name, then taking from sql and at last posting it in """
        title = str(self.metaInformationResolver.currentSource()
                    .fileName()[:-4].split('\\')[-1:][0].split(' - ')[1])
        """-------------------- sqllite3 -----------------------------------"""
        connection = sqlite3.connect("songs_info.db")
        try:
            result = (connection.execute("SELECT * FROM SONGS WHERE Title = ?", (title,))).fetchall()[0]
        except IndexError:
            print 'outer music played'
            result = [title[:-4].split('\\')[-1:][0], '', '', '']
        title = result[0]
        if not title:
            title = self.metaInformationResolver.currentSource().fileName()

        titleItem = QtGui.QTableWidgetItem(title)
        titleItem.setFlags(titleItem.flags() ^ QtCore.Qt.ItemIsEditable)

        artist = result[1]
        artistItem = QtGui.QTableWidgetItem(artist)
        artistItem.setFlags(artistItem.flags() ^ QtCore.Qt.ItemIsEditable)

        album = result[2]
        albumItem = QtGui.QTableWidgetItem(album)
        albumItem.setFlags(albumItem.flags() ^ QtCore.Qt.ItemIsEditable)

        cover = result[3]
        coverItem = QtGui.QTableWidgetItem(cover)
        coverItem.setFlags(coverItem.flags() ^ QtCore.Qt.ItemIsEditable)

        currentRow = self.musicTable.rowCount()
        self.musicTable.insertRow(currentRow)
        self.musicTable.setItem(currentRow, 0, titleItem)
        self.musicTable.setItem(currentRow, 1, artistItem)
        self.musicTable.setItem(currentRow, 2, albumItem)
        self.musicTable.setItem(currentRow, 3, coverItem)

        if not self.musicTable.selectedItems():
            self.musicTable.selectRow(0)
            self.musicTable_1.selectRow(0)
            self.mediaObject.setCurrentSource(self.metaInformationResolver.currentSource())

        index = self.sources.index(self.metaInformationResolver.currentSource()) + 1

        if len(self.sources) > index:
            self.metaInformationResolver.setCurrentSource(self.sources[index])
        else:
            self.musicTable.resizeColumnsToContents()
            if self.musicTable.columnWidth(0) > 300:
                self.musicTable.setColumnWidth(0, 300)
                self.musicTable_1.setColumnWidth(0, 300)

    def aboutToFinish(self):
        index = self.sources.index(self.mediaObject.currentSource()) + 1
        if len(self.sources) > index:
            self.mediaObject.enqueue(self.sources[index])

    def setup_actions(self):

        self.playAction = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_MediaPlay), "Play",
            self, shortcut="Ctrl+P", enabled=False,
            triggered=self.mediaObject.play)

        self.pauseAction = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_MediaPause),
            "Pause", self, shortcut="Ctrl+A", enabled=False,
            triggered=self.mediaObject.pause)

        self.stopAction = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_MediaStop), "Stop",
            self, shortcut="Ctrl+S", enabled=False,
            triggered=self.mediaObject.stop)

        self.nextAction = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_MediaSkipForward),
            "Next", self, shortcut="Ctrl+N")

        self.previousAction = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_MediaSkipBackward),
            "Previous", self, shortcut="Ctrl+R")

        self.addFilesAction = QtGui.QAction("Add &Files", self,
                                            shortcut="Ctrl+F", triggered=self.addFiles)

        self.exitAction = QtGui.QAction("E&xit", self, shortcut="Ctrl+X",
                                        triggered=self.close)

        self.aboutAction = QtGui.QAction("A&bout", self, shortcut="Ctrl+B",
                                         triggered=self.about)

        self.aboutQtAction = QtGui.QAction("About &Qt", self,
                                           shortcut="Ctrl+Q", triggered=QtGui.qApp.aboutQt)

    def setup_menus(self):
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.addFilesAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        aboutMenu = self.menuBar().addMenu("&Help")
        aboutMenu.addAction(self.aboutAction)
        aboutMenu.addAction(self.aboutQtAction)

    def setup_ui(self):
        self.setObjectName(_fromUtf8("Display"))
        self.setEnabled(True)
        self.resize(462, 699)
        self.setAccessibleName(_fromUtf8(""))

        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        '''----------------------start of hack section--------------'''

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft YaHei UI"))
        font.setPointSize(12)

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.textEdit_1 = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_1.setMaximumSize(QtCore.QSize(16777215, 31))
        self.textEdit_1.setFont(font)
        self.textEdit_1.setObjectName(_fromUtf8("textEdit"))
        self.textEdit_1.setHtml(_translate("Display", 'Search..', None))

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setMinimumSize(QtCore.QSize(81, 31))
        self.splitter.setMaximumSize(QtCore.QSize(16777215, 81))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))

        self.label = QtGui.QLabel(self.splitter)
        self.label.setMaximumSize(QtCore.QSize(241, 31))
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.label.setText(_translate("Display", "hello " + self.username + ". Money:", None))

        self.textEdit = QtGui.QTextEdit(self.splitter)
        self.textEdit.setEnabled(False)
        self.textEdit.setMaximumSize(QtCore.QSize(81, 31))
        self.textEdit.setFont(font)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit.setHtml(_translate("Display", self.money, None))

        self.checkBox = QtGui.QCheckBox(self.splitter)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox.setText(_translate("Display", "hack money", None))
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.textEdit.setEnabled)
        self.verticalLayout.addWidget(self.textEdit_1)
        self.verticalLayout.addWidget(self.splitter)
        """---------------------------- end of hack--------------------------"""

        bar = QtGui.QToolBar()

        bar.addAction(self.playAction)
        bar.addAction(self.pauseAction)
        bar.addAction(self.stopAction)

        self.seekSlider = Phonon.SeekSlider(self)
        self.seekSlider.setMediaObject(self.mediaObject)

        self.volumeSlider = Phonon.VolumeSlider(self)
        self.volumeSlider.setAudioOutput(self.audioOutput)
        self.volumeSlider.setSizePolicy(QtGui.QSizePolicy.Maximum,
                                        QtGui.QSizePolicy.Maximum)

        volumeLabel = QtGui.QLabel()
        volumeLabel.setPixmap(QtGui.QPixmap('images/volume.png'))

        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkGray)

        self.time_lcd = QtGui.QLCDNumber()
        self.time_lcd.setPalette(palette)
        """---------------------------- tables --------------------------"""

        headers = ["Title", "Artist", "Album", "Cover"]
        items = []
        self.musicTable = QtGui.QTableWidget(0, 4)
        self.musicTable.setStyleSheet("background: lightgreen")

        self.musicTable.setHorizontalHeaderLabels(headers)
        self.musicTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.musicTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.musicTable.cellPressed.connect(self.tableClicked)
        self.musicTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        """---------------------------- end of tables--------------------------"""

        """---------------------------- Discover tables --------------------------"""

        self.musicTable_1 = QtGui.QTableWidget(0, 4)
        headers[3] = 'Price'
        self.musicTable_1.setHorizontalHeaderLabels(headers)
        self.musicTable_1.setStyleSheet("background: springgreen")
        self.musicTable_1.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.musicTable_1.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.musicTable_1.cellPressed.connect(self.tableClickedDisover)
        """---------------------------- end of tables--------------------------"""

        """---------------------------- Discover tabs --------------------------"""

        self.TheMain = QtGui.QTabWidget(self.centralwidget)
        self.TheMain.setMinimumSize(QtCore.QSize(350, 500))
        self.TheMain.setMaximumSize(QtCore.QSize(1000, 10000))
        self.TheMain.setFont(font)
        self.TheMain.setObjectName(_fromUtf8("TheMain"))

        self.Discover_Tab = QtGui.QWidget()
        self.Discover_Tab.setFont(font)
        self.Discover_Tab.setAutoFillBackground(False)
        self.Discover_Tab.setObjectName(_fromUtf8("Discover_Tab"))

        self.verticalLayout_0 = QtGui.QVBoxLayout(self.Discover_Tab)
        self.verticalLayout_0.setObjectName(_fromUtf8("verticalLayout_0"))
        self.verticalLayout_0.addWidget(self.musicTable_1)

        self.TheMain.addTab(self.Discover_Tab, _fromUtf8("Discover"))

        self.songList_Tab = QtGui.QWidget()
        self.songList_Tab.setObjectName(_fromUtf8("songList_Tab"))

        self.verticalLayout_2 = QtGui.QVBoxLayout(self.songList_Tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.verticalLayout_2.addWidget(self.musicTable)

        self.splitter.raise_()

        self.TheMain.addTab(self.songList_Tab, _fromUtf8("Song List"))
        self.CurrentPlaying_Tab = QtGui.QWidget()

        self.verticalLayout_3 = QtGui.QVBoxLayout(self.CurrentPlaying_Tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))

        self.CurrentPlaying_Tab.setObjectName(_fromUtf8("CurrentPlaying_Tab"))
        self.Current_song_pic = QtGui.QLabel(self.CurrentPlaying_Tab)
        self.Current_song_pic.setText('')
        self.Current_song_pic.setGeometry(QtCore.QRect(10, 70, 411, 411))
        self.Current_song_pic.setStyleSheet(_fromUtf8(r"border-image: url(Squares.jpg) 0 0 0 0 stretch stretch;"
                                                      " background-position: center;"))
        self.verticalLayout_3.addWidget(self.Current_song_pic)

        self.Current_song_label = QtGui.QLabel(self.CurrentPlaying_Tab)
        self.Current_song_label.setText('sample')
        self.Current_song_label.setGeometry(QtCore.QRect(10, 70, 31, 81))
        self.Current_song_label.setMaximumSize(QtCore.QSize(1000, 31))
        self.verticalLayout_3.addWidget(self.Current_song_label)

        self.TheMain.addTab(self.CurrentPlaying_Tab, _fromUtf8("Current Playing"))
        """---------------------------- end tabs --------------------------"""

        seekerLayout = QtGui.QHBoxLayout()
        seekerLayout.addWidget(self.seekSlider)
        seekerLayout.addWidget(self.time_lcd)

        playbackLayout = QtGui.QHBoxLayout()
        playbackLayout.addWidget(bar)
        playbackLayout.addStretch()
        playbackLayout.addWidget(volumeLabel)
        playbackLayout.addWidget(self.volumeSlider)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(self.verticalLayout)
        mainLayout.addWidget(self.TheMain)
        mainLayout.addLayout(seekerLayout)
        mainLayout.addLayout(playbackLayout)

        widget = QtGui.QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)
        self.setGeometry(50, 100, 450, 700)
        self.setWindowTitle("Roytify Client")
        self.setWindowIcon(QtGui.QIcon("useful\Logo.ico"))

    def displayWindowShow(self):
        self.welcomeWindow = QtGui.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.welcomeWindow)
        self.welcomeWindow.show()

    def invest(self):
        return 'SETMONEY: ' + str(self.textEdit.toPlainText()) + ' USERNAME: ' + self.username


def myExitHandler():
    temp = socket_send(window.invest())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Music Player")
    app.setQuitOnLastWindowClosed(True)
    window = display_MainWindow()
    app.aboutToQuit.connect(myExitHandler)
    window.show()

    sys.exit(app.exec_())
