from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSpinBox,
    QMessageBox
)
import os
import sys
basedir = os.path.dirname(__file__)

try:
    from ctypes import windll # Only exists on Windows. Used to set unique Windows Exe ID.
    myappid = 'Zatyrus.FDMatch.V1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass



from FDMatch_Backend import FDMatch

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.__FDMStartupMode:str
        self.__FDMNumber:int
        self.__FDMFileType:str
        self.__FDMatch:FDMatch
        self.__FDMExecMode:str
        
        self.setWindowTitle('Funky File Directory Matching - Hover for ToolTips')
        
        preinitial_layout = QVBoxLayout()
        initial_layout = QVBoxLayout()
        label_layout = QVBoxLayout()
        exec_layout = QVBoxLayout()
        global_layout = QHBoxLayout()
        
        self.__FDMNumberSpin = QSpinBox()
        self.__FDMNumberSpin.valueChanged.connect(self.__FDMNumber_changed)
        self.__FDMNumberSpin.setMinimum(0)
        self.__FDMNumberSpin.setValue(7)
        self.__FDMNumberSpin.setToolTip('Choose the number of characters considered for file-directory matching. Counting starts left-side.')
        
        self.__FDMFileTypeSelection = QComboBox()
        self.__FDMFileTypeSelection.currentTextChanged.connect(self.__FDMFileType_changed)
        self.__FDMFileTypeSelection.addItems(['.pdf', '.txt', '.png', '.jpeg', '.jpg', '.csv'])
        self.__FDMFileTypeSelection.setCurrentText('.pdf')
        self.__FDMFileTypeSelection.setToolTip('Choose a SINGLE file type to fetch.')

        self.__FDMStartupModeSelection = QComboBox()
        self.__FDMStartupModeSelection.currentTextChanged.connect(self.__FDMStartupMode_changed)
        self.__FDMStartupModeSelection.addItems(["Select multiple Files", "Fetch whole Directory"])
        self.__FDMStartupModeSelection.setCurrentText("Select multiple Files")
        self.__FDMStartupModeSelection.setToolTip("'Select multiple Files' - Let's you choose the files to test for matching directories. \n 'Fetch whole Directory' - Load ALL files in a selected directory matching the selected file type.")
                
        self.__Fetch = QPushButton()
        self.__Fetch.setText('Click to Fetch!')
        self.__Fetch.clicked.connect(self.__FDMFetch)
        
        self.__FileLabel = QLabel()
        self.__FileLabel.setText('Pending...')
        self.__FileLabel.setStyleSheet("padding-bottom: 1px")
        
        self.__DirLabel = QLabel()
        self.__DirLabel.setText('Pending...')
        self.__DirLabel.setStyleSheet("padding-bottom: 9px")
        
        self.__FDMExecModeSelect = QComboBox()
        self.__FDMExecModeSelect.currentTextChanged.connect(self.__FDMExecModeSelect_changed)
        self.__FDMExecModeSelect.addItems(['Copy (safe)', 'Move (unsafe)'])
        self.__FDMExecModeSelect.setCurrentText('Copy (safe)')
        self.__FDMExecModeSelect.setToolTip("'Copy (safe)' - COPIES files. \n 'Move (unsafe)' - COPIES and DELETS affected files. \n Both methods will overwrite files with the same name present in the target directory")
        
        self.__Exec = QPushButton()
        self.__Exec.setText('Click to verify!')
        self.__Exec.setToolTip("Verify if all preior steps (left-side in application) have been completed. \n Will transform into EXECUTION button after successful verification.")
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
        
        try:
            if self.__FDMStartupMode == "Select multiple Files":
                self.__FDMatch = FDMatch.FDM_fetchFiles(number=self.__FDMNumber,
                                                        fileType = self.__FDMFileType)
            if self.__FDMStartupMode == "Fetch whole Directory":
                self.__FDMatch = FDMatch.FDM_fetchDir(number=self.__FDMNumber,
                                                    fileType = self.__FDMFileType)
            
            if self.__FDMatch.check_inpathIsEmpty():
                return self.__InpathIsEmptyDialogue()
            
            if self.__FDMatch.check_outpathIsEmpty():
                return self.__OutpathIsEmptyDialogue()
                            
            if self.__FDMatch.isCompatible():
                self.__Fetch.setStyleSheet("background-color : palegreen")
                self.__Fetch.setText(f"Succeffully allocated files")
                
                self.__FileLabel.setText(f"Allocated {self.__FDMatch.get_numberOfAllocatedFiles()} File/s in {self.__FDMatch.get_inpath()}")
                self.__DirLabel.setText(f"{self.__FDMatch.get_numberOfMatchingDirectories()} matching Directory/ies in {self.__FDMatch.get_inpath()}")
                
                self.__Exec.setText('Click to verify!')
                self.__Exec.setStyleSheet("background-color : lightgray")
                
            elif not self.__FDMatch.isCompatible():
                self.__Fetch.setStyleSheet("background-color : lightcoral")
                self.__Fetch.setText(f"Something went wrong")
                self.__errDialogue(self.__FDMatch.get_mismatchedFiles())
                
        except:
            self.__objNoConstructionDialogue()
            
    def __FDMVerify(self):
        try:
            assert (self.__FDMatch != None)
            assert (self.__FDMatch.verify())
            assert (self.__FDMExecMode != None)
            self.__Exec.setCheckable(True)
            self.__Exec.setStyleSheet("background-color : orange")
            self.__Exec.setText('Ready? --- Sort!')
        except:
            self.__Exec.setStyleSheet("background-color : lightcoral")
            self.__Exec.setText('Check your input!')
            
    def __FDMExec(self, checked):
        if checked:
            self.__FDMatch.set_execMode(self.__FDMExecMode)
            file_already_in_dir, err_arr = self.__FDMatch.check_if_exists()
            if file_already_in_dir:
                return self.__moveWarnDialogue(err_arr=err_arr)
                
            elif not file_already_in_dir:
                self.__FDMatch.execute()
            
            if self.__FDMatch.wasSuccessful():
                self.__Exec.setStyleSheet("background-color : palegreen")
                self.__Exec.setText(f'{self.__FDMatch.get_numberOfAllocatedFiles()} File/s re-allocated successfully !')
                self.__Exec.setCheckable(False)
                self.__reset()
    
    def __reset(self):
        self.__Fetch.setText('Click to Fetch!')
        self.__Fetch.setStyleSheet("background-color : lightgray")
        del self.__FDMatch
        
    def __objNoConstructionDialogue(self):
        dlg = QMessageBox.critical(
            self,
            "FDMatch Object could not be constructed!",
            "Please, specify and fetch files. First choose the files to re-distribute, then choose the parent directory containing the target folders.",
            buttons=QMessageBox.Ok | QMessageBox.Abort,
            defaultButton=QMessageBox.Ok
        )
        
        if dlg == QMessageBox.Ok:
            return
            
        elif dlg == QMessageBox.Abort:
            app.exit()
    
    def __InpathIsEmptyDialogue(self):
        dlg = QMessageBox.warning(
            self,
            "No valid Files were chosen or match the Description set.",
            "Please, verify the file type chosen!",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok
        )
        
        if dlg == QMessageBox.Ok:
            del self.__FDMatch
            return
            
    def __OutpathIsEmptyDialogue(self):
        dlg = QMessageBox.warning(
            self,
            "No Directories were discovered in the Path provided.",
            "Please, verify that the chosen outpath points to the directory containing the target folders!",
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok
        )
        
        if dlg == QMessageBox.Ok:
            del self.__FDMatch
            return

        
    def __errDialogue(self, err_arr):
        dlg = QMessageBox.critical(
            self,
            "File-Directory Mismatch detected!",
            f"The following file/s could not be matched with the directory tree:\n\n{err_arr}",
            buttons=QMessageBox.Reset | QMessageBox.Abort | QMessageBox.Ignore,
            defaultButton=QMessageBox.Reset
        )
        
        if dlg == QMessageBox.Reset:
            self.__reset()
            
        elif dlg == QMessageBox.Ignore:
            return
            
        elif dlg == QMessageBox.Abort:
            app.exit()
            
    def __moveWarnDialogue(self, err_arr):
        dlg = QMessageBox.warning(
            self,
            "Files already exist in Directory Tree!",
            f"Do you want to continue and overwrite the following files?\n\n{err_arr}",
            buttons=QMessageBox.Yes | QMessageBox.No |  QMessageBox.Reset | QMessageBox.Abort,
            defaultButton=QMessageBox.No
        )
        
        if dlg == QMessageBox.No:
            self.__Exec.setChecked(False)
            return
            
        elif dlg == QMessageBox.Reset:
            self.__Exec.setChecked(False)
            self.__reset()
            
        elif dlg == QMessageBox.Yes:
            self.__FDMatch.execute()
            
            if self.__FDMatch.wasSuccessful():
                self.__Exec.setStyleSheet("background-color : palegreen")
                self.__Exec.setText(f'{self.__FDMatch.get_numberOfAllocatedFiles()} File/s re-allocated successfully !')
                self.__Exec.setCheckable(False)
                self.__reset()
            
        elif dlg == QMessageBox.Abort:
            app.exit()


app = QApplication(sys.argv)
app.setStyleSheet("""
                  QMainWindow {background-color: whitesmoke}
                  QLabel {padding: 5px; font: bold 12px; font-family: Courier New}
                  QPushButton {padding: 5px; font: 12px; font-family: Courier New}
                  QComboBox {padding: 3px; font: 12px;  font-family: Courier New}
                  QSpinBox {padding: 3px; font: 12px;  font-family: Courier New}""")


app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'favicon.ico')))

window = MainWindow()
window.show()
app.exec()