import os, cv2
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui_app import Ui_MainWindow

os.environ.update({"QT_QPA_PLATFORM_PLUGIN_PATH": "/home/anh/.local/lib/python3.8/site-packages/PySide2/Qt/plugins"})

filename = 0
category = 1
noiserate = 2
blur = 3
overexposure = 4
dark = 5
fluid = 6

def openFolder():
    dir_ = os.getcwd()
    dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder:', dir_, QFileDialog.ShowDirsOnly)
    
    if dir_ != '':
        return str(dir_)
    else:
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folderPath = None
        self.imageData = []
        self.listImageData = []
        self.currentId = 0

        self.ui.actionOpen_folder.triggered.connect(self.btn_actionOpen_folderIsClicked)
        self.btn_actionOpen_folderIsClicked()
        self.ui.btn_next.clicked.connect(self.nextImage)
        self.ui.btn_back.clicked.connect(self.backImage)

        self.ui.btn_info.clicked.connect(self.btnInfoClicked)
        self.ui.btn_noninfo.clicked.connect(self.btnNonInfoClicked)

        # self.ui.btn_25.clicked.connect(self.btn25Clicked)
        # self.ui.btn_50.clicked.connect(self.btn50Clicked)
        # self.ui.btn_75.clicked.connect(self.btn75Clicked)
        # self.ui.btn_100.clicked.connect(self.btn100Clicked)
        # self.ui.btn_noninfo.clicked.connect(self.btnNonInfoClicked)
        # self.ui.btn_noninfo.clicked.connect(self.btnNonInfoClicked)

        self.show()

    def disableNoiseOption(self):
        self.ui.btn_25.setCheckable(False)
        self.ui.btn_50.setCheckable(False)
        self.ui.btn_75.setCheckable(False)
        self.ui.btn_100.setCheckable(False)
        self.ui.btn_blur.setCheckable(False)
        self.ui.btn_over.setCheckable(False)
        self.ui.btn_dark.setCheckable(False)
        self.ui.btn_fluid.setCheckable(False)

    def enableNoiseOption(self):
        self.ui.btn_25.setCheckable(True)
        self.ui.btn_50.setCheckable(True)
        self.ui.btn_75.setCheckable(True)
        self.ui.btn_100.setCheckable(True)
        self.ui.btn_blur.setCheckable(True)
        self.ui.btn_over.setCheckable(True)
        self.ui.btn_dark.setCheckable(True)
        self.ui.btn_fluid.setCheckable(True)

    def btnInfoClicked(self):
        if self.ui.btn_info.isChecked():
            self.ui.btn_noninfo.setChecked(False)
            self.disableNoiseOption()
        else:
            self.enableNoiseOption()
    def btnNonInfoClicked(self):
        if self.ui.btn_noninfo.isChecked():
            self.ui.btn_info.setChecked(False)
            self.disableNoiseOption()
        else:
            self.enableNoiseOption()

    def btn_actionOpen_folderIsClicked(self):
        # self.folder_path = openFolder()
        self.folder_path = "/home/anh/Pictures"
        if self.folder_path != None:
            loadDir = QDir(self.folder_path)
            loadDir.setNameFilters(['*.jpg', '*.JPG', '*.png', '*.PNG', '*.jpeg', '*.JPEG'])
            self.infoList = loadDir.entryInfoList()
            for item in self.infoList:
                self.imageData = [item.absoluteFilePath(), None, None, None, None, None, None]
                self.listImageData.append(self.imageData)

            self.displayImage()
                
    def displayImage(self):
        pixmap = QPixmap(self.listImageData[self.currentId][filename])
        self.ui.display.setPixmap(pixmap.scaled(self.ui.display.size(), Qt.KeepAspectRatio))

    def nextImage(self):
        if self.currentId < self.listLength():
            self.cleanData()
            self.writeData()
            self.currentId += 1
            self.clearDataDisplay()
            self.readData()
            self.displayImage()

    def backImage(self):
        if self.currentId != 0:
            self.cleanData()
            self.writeData()
            self.currentId -= 1
            self.clearDataDisplay()
            self.readData()
            self.displayImage()

    def listLength(self):
        return len(self.listImageData)
    
    def clearDataDisplay(self):
        self.enableNoiseOption()
        self.ui.btn_info.setChecked(False)
        self.ui.btn_noninfo.setChecked(False)
        self.ui.btn_25.setChecked(False)
        self.ui.btn_50.setChecked(False)
        self.ui.btn_75.setChecked(False)
        self.ui.btn_100.setChecked(False)
        self.ui.btn_blur.setChecked(False)
        self.ui.btn_over.setChecked(False)
        self.ui.btn_dark.setChecked(False)
        self.ui.btn_fluid.setChecked(False)
        return
    
    def cleanData(self):
        name = self.listImageData[self.currentId][filename]
        self.listImageData[self.currentId] = [name, None, None, None, None, None, None]
    
    def readData(self):
        data = self.listImageData[self.currentId]
        if data[category] == "None":
            return
        elif data[category] == "Info":
            self.ui.btn_info.setChecked(True)
            return
        elif data[category] == "Non_Info":
            self.ui.btn_noninfo.setChecked(True)
            return
        
        elif data[category] == "Noise":
            if data[noiserate] == 0.25:
                self.ui.btn_25.setChecked(True)
            elif data[noiserate] == 0.50:
                self.ui.btn_50.setChecked(True)
            elif data[noiserate] == 0.75:
                self.ui.btn_75.setChecked(True)
            elif data[noiserate] == 1.00:
                self.ui.btn_100.setChecked(True)
            
            if data[blur] == 1:
                self.ui.btn_blur.setChecked(True)
            if data[overexposure] == 1:
                self.ui.btn_over.setChecked(True)
            if data[dark] == 1:
                self.ui.btn_dark.setChecked(True)
            if data[fluid] == 1:
                self.ui.btn_fluid.setChecked(True)
        

    def writeData(self):
        if self.ui.btn_info.isChecked():
            self.listImageData[self.currentId][category] = "Info"
            self.listImageData[self.currentId][noiserate] = "#"
        elif self.ui.btn_noninfo.isChecked():
            self.listImageData[self.currentId][category] = "Non_Info"
            self.listImageData[self.currentId][noiserate] = "#"
        else:
            self.listImageData[self.currentId][category] = "Noise"
        
        if self.ui.btn_25.isChecked():
            self.listImageData[self.currentId][noiserate] = 0.25
        elif self.ui.btn_50.isChecked():
            self.listImageData[self.currentId][noiserate] = 0.50
        elif self.ui.btn_75.isChecked():
            self.listImageData[self.currentId][noiserate] = 0.75
        elif self.ui.btn_100.isChecked():
            self.listImageData[self.currentId][noiserate] = 1.00
        
        if self.ui.btn_blur.isChecked():
            self.listImageData[self.currentId][blur] = 1
        if self.ui.btn_over.isChecked():
            self.listImageData[self.currentId][overexposure] = 1
        if self.ui.btn_dark.isChecked():
            self.listImageData[self.currentId][dark] = 1
        if self.ui.btn_fluid.isChecked():
            self.listImageData[self.currentId][fluid] = 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    view = MainWindow()

    sys.exit(app.exec_())