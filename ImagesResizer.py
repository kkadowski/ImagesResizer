from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QDesktopWidget, QTreeView, QWidget, QVBoxLayout, QMenu, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, QModelIndex, QDir
import pathlib
import sys
import os
import shutil
import cv2
import time
from PIL import Image
from os import walk
from os import listdir
from os.path import isfile, join

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        self.listadozmiany=[]
        self.destdir = 'resized/'
        self.path = ''
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 501)
        MainWindow.setMinimumSize(QtCore.QSize(650, 480))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 1)
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 2, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_4.addWidget(self.textEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setProperty("value", 50)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_2.addWidget(self.spinBox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_5.addWidget(self.pushButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 22))
        self.menubar.setObjectName("menubar")
        self.menuPlik = QtWidgets.QMenu(self.menubar)
        self.menuPlik.setObjectName("menuPlik")
        MainWindow.setMenuBar(self.menubar)
        self.actionZamknij = QtWidgets.QAction(MainWindow)
        self.actionZamknij.setObjectName("actionZamknij")
        self.menuPlik.addAction(self.actionZamknij)
        self.menubar.addAction(self.menuPlik.menuAction())
        
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath('')
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.treeView.setModel(self.dirModel)
        self.treeView.setRootIndex(self.dirModel.index(os.getenv("HOME")))
        self.treeView.setAnimated(False)
        self.treeView.setIndentation(20)
        self.treeView.setSortingEnabled(True)
        #
        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath('')
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)
        self.listView.setModel(self.fileModel)
        self.listView.setRootIndex(self.fileModel.index(os.getenv("HOME")))
       #
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.treeView.clicked.connect(self.dodaj)
        self.listView.clicked.connect(self.info)
        self.pushButton.clicked.connect(self.zmien)
        self.actionZamknij.triggered.connect(self.Zamknij)
    
    def zmien(self):
        destination = self.path+'/'+time.strftime('%Y_%m_%d_%H_%M_', time.localtime())+self.destdir
        os.mkdir(destination)
        flaga = True
        for plik in self.listadozmiany:
            try:
                shutil.copy(plik, destination)
                flaga=True
            except shutil.SameFileError:
                self.makeMessage("Copying problem", "Source and destination represents the same file.", "Problem", 'warn', 'button_warn')
                flaga=False
            except IsADirectoryError:
                print(f"Destination {destinantion} is a directory.", 'warn', 'button_warn')
                flaga=False
            except PermissionError:
                self.makeMessage("Permission problem","Permission denied.", "Problem", 'warn', 'button_warn')
                flaga=False
            except:
                self.makeMessage("Copying problem", "Error occurred while copying files.", "Problem", 'warn', 'button_warn')
                flaga=False
        if flaga:
            self.resize(destination)
            
    def resize(self, dest):
        scale_percent = self.spinBox.value()
       
        myfiles = [f for f in listdir(dest) if isfile(join(dest, f))]
        
        for _image in myfiles:
            _img = dest+_image
            img = cv2.imread(_img, cv2.IMREAD_UNCHANGED)
            w = int(img.shape[1] * scale_percent / 100)
            h = int(img.shape[0] * scale_percent / 100)
            res_img = cv2.resize(img, (w, h), interpolation = cv2.INTER_AREA)
            cv2.imwrite(_img, res_img)
        self.makeMessage("Resizing complited","Resizing complited.", "Info", 'info', 'button_info')
            
    def info(self, index):
        indexItem = self.fileModel.index(index.row(), 0, index.parent())
        self.fileName = self.fileModel.fileName(indexItem)
        
        self.Full = self.path+'/'+self.fileName
        
        if self.Full.endswith(".jpg") or self.Full.endswith(".jpeg") or self.Full.endswith(".png") or self.Full.endswith(".bmp"):
            im = cv2.imread(self.Full)
            self.h, self.w, self.c = im.shape
            poprzedni = ''.join(self.textEdit.toPlainText())
            self.textEdit.setText(f"File name: {self.fileName} \nFile directory: {self.path} \nHeight: {self.h} \nWidth: {self.w} \nChannels: {self.c}\n\n {poprzedni}\n        \n\n")
            self.listadozmiany.append(self.Full)
        else:
            self.makeMessage("This is not an image file", "You can select only jpg, jpeg, png and bmp files.", "Problem", 'warn', 'button_warn')

    def makeMessage(self, text, info, title, type, typeButton):
        self.msg = QMessageBox()
        if type == 'warn':
            self.msg.setIcon(QMessageBox.Warning)
        elif type == 'info':
            self.msg.setIcon(QMessageBox.Information)
        elif type =='question':
            self.msg.setIcon(QMessageBox.Question)
    
        self.msg.setText(text)
        self.msg.setInformativeText(info)
        self.msg.setWindowTitle(title)
        if typeButton == 'button_warn' or typeButton =='button_info':
            self.msg.setStandardButtons(QMessageBox.Ok)
        elif typeButton == 'button_yesno':
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            self.msg.setDefaultButton(QMessageBox.No)
        self.msg.show()
        
        retval = self.msg.exec_()
        if retval == QMessageBox.Yes:
            sys.exit(app.exec_())
        else:
            pass
    
    def Zamknij(self):
        self.makeMessage("Quit", "Do you want to quit?", "Do you want to quit?", "question", "button_yesno")
    
    def dodaj(self, index):
        self.listadozmiany.clear()
        self.path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.listView.setRootIndex(self.fileModel.setRootPath(self.path))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Images Resizer"))
        self.label_4.setText(_translate("MainWindow", "Source directory:"))
        self.label_3.setText(_translate("MainWindow", "Image info:"))
        self.label.setText(_translate("MainWindow", "Size:"))
        self.spinBox.setSuffix(_translate("MainWindow", "%"))
        self.pushButton.setText(_translate("MainWindow", "Resize"))
        self.menuPlik.setTitle(_translate("MainWindow", "File"))
        self.actionZamknij.setText(_translate("MainWindow", "Close"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
