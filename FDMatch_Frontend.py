from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QLabel, QLineEdit, QVBoxLayout, QWidget,QMenu ,QAction
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFontComboBox,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
    QSpinBox,
    QHBoxLayout,
    QVBoxLayout
)

import sys

from FDMatch_Backend import FDMatch

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.__FDMStartupMode:str
        self.__FDMNumber:int
        self.__FDMFileType:str
        self.__FDMatch:FDMatch
        self.__FDMExecMode:str
        
        self.setWindowTitle('Funky File Directory Matching App')
        
        preinitial_layout = QVBoxLayout()
        initial_layout = QVBoxLayout()
        label_layout = QVBoxLayout()
        exec_layout = QVBoxLayout()
        global_layout = QHBoxLayout()
        
        self.__FDMNumberSpin = QSpinBox()
        self.__FDMNumberSpin.valueChanged.connect(self.__FDMNumber_changed)
        self.__FDMNumberSpin.setMinimum(0)
        self.__FDMNumberSpin.setValue(7)
        
        self.__FDMFileTypeSelection = QComboBox()
        self.__FDMFileTypeSelection.currentTextChanged.connect(self.__FDMFileType_changed)
        self.__FDMFileTypeSelection.addItems(['.pdf', '.txt', '.png', '.jpeg', '.jpg', '.csv'])
        self.__FDMFileTypeSelection.setCurrentText('.pdf')

        self.__FDMStartupModeSelection = QComboBox()
        self.__FDMStartupModeSelection.currentTextChanged.connect(self.__FDMStartupMode_changed)
        self.__FDMStartupModeSelection.addItems(["Select multiple Files", "Fetch whole Directory"])
        self.__FDMStartupModeSelection.setCurrentText("Select multiple Files")
                
        self.__Fetch = QPushButton()
        self.__Fetch.setText('Click to Fetch!')
        self.__Fetch.clicked.connect(self.__FDMFetch)
        
        self.__FileLabel = QLabel()
        self.__FileLabel.setText('Pending...')
        
        self.__DirLabel = QLabel()
        self.__DirLabel.setText('Pending...')
        
        self.__FDMExecModeSelect = QComboBox()
        self.__FDMExecModeSelect.currentTextChanged.connect(self.__FDMExecModeSelect_changed)
        self.__FDMExecModeSelect.addItems(['Copy (safe)', 'Move (unsafe)'])
        self.__FDMExecModeSelect.setCurrentText('Copy (safe)')
        
        self.__Exec = QPushButton()
        self.__Exec.setText('Click to verify!')
        self.__Exec.clicked.connect(self.__FDMVerify)
        self.__Exec.clicked.connect(self.__FDMExec)
        
        preinitial_layout.addWidget(self.__FDMNumberSpin)
        preinitial_layout.addWidget(self.__FDMFileTypeSelection)
        
        initial_layout.addWidget(self.__FDMStartupModeSelection)
        initial_layout.addWidget(self.__Fetch)
        
        label_layout.addWidget(self.__FileLabel)
        label_layout.addWidget(self.__DirLabel)
        
        exec_layout.addWidget(self.__FDMExecModeSelect)
        exec_layout.addWidget(self.__Exec)
        
        global_layout.addLayout(preinitial_layout)
        global_layout.addLayout(initial_layout)
        global_layout.addLayout(label_layout)
        global_layout.addLayout(exec_layout)
        
        widget = QWidget()
        widget.setLayout(global_layout)
        self.setCentralWidget(widget)
        
        
    def __FDMStartupMode_changed(self, mode:str):
        self.__FDMStartupMode = mode
        
    def __FDMFileType_changed(self, fileType:str):
        self.__FDMFileType = fileType
    
    def __FDMNumber_changed(self, number:str):
        self.__FDMNumber = number
        
    def __FDMExecModeSelect_changed(self, mode:str):
        self.__FDMExecMode = mode
    
    def __FDMFetch(self):
        assert(type(self.__FDMNumber) == int)
        assert(self.__FDMStartupMode != None)
        
        if self.__FDMStartupMode == "Select multiple Files":
            self.__FDMatch = FDMatch.FDM_fetchFiles(number=self.__FDMNumber,
                                                    fileType = self.__FDMFileType)
        if self.__FDMStartupMode == "Fetch whole Directory":
            self.__FDMatch = FDMatch.FDM_fetchDir(number=self.__FDMNumber,
                                                  fileType = self.__FDMFileType)
                        
        if self.__FDMatch.isCompatible():
            self.__Fetch.setStyleSheet("background-color : green")
            self.__Fetch.setText(f"Succeffully allocated files")
            
            self.__FileLabel.setText(f"Allocated {self.__FDMatch.get_numberOfAllocatedFiles()} File/s in {self.__FDMatch.get_inpath()}")
            self.__DirLabel.setText(f"{self.__FDMatch.get_numberOfMatchingDirectories()} matching Directory/ies in {self.__FDMatch.get_inpath()}")
            
            self.__Exec.setText('Click to verify!')
            self.__Exec.setStyleSheet("background-color : white")
            
        elif not self.__FDMatch.isCompatible():
            self.__Fetch.setStyleSheet("background-color : red")
            self.__Fetch.setText(f"Something went wrong")
            
    def __FDMVerify(self):
        try:
            assert (self.__FDMatch != None)
            assert (self.__FDMatch.verify())
            assert (self.__FDMExecMode != None)
            self.__Exec.setCheckable(True)
            self.__Exec.setStyleSheet("background-color : orange")
            self.__Exec.setText('Ready? --- Sort!')
        except:
            self.__Exec.setStyleSheet("background-color : red")
            self.__Exec.setText('Check your input!')
            
    def __FDMExec(self, checked):
        if checked:
            self.__FDMatch.set_execMode(self.__FDMExecMode)
            self.__FDMatch.execute()
            
            if self.__FDMatch.wasSuccessful():
                self.__Exec.setStyleSheet("background-color : green")
                self.__Exec.setText(f'{self.__FDMatch.get_numberOfAllocatedFiles()} Files sorted successfully !')
                self.__Exec.setCheckable(False)
                self.__reset()
    
    def __reset(self):
        self.__Fetch.setText('Click to Fetch!')
        self.__Fetch.setStyleSheet("background-color : white")
        del self.__FDMatch
            
                
                


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()