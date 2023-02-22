import os
import shutil
import glob
from pyDialogue import *

class FDMatch():
    def __init__(self, inpath, outpath, number, fileType) -> None:
        if type(inpath) == tuple or type(inpath) == list:
            self.__inpath = os.path.dirname(inpath[0])
            
        self.__outpath:str = outpath
        self.__number:int = number
        self.__fileType:str = fileType
        
        self.__dirName_Storage = [DIR for DIR in os.listdir(outpath) if os.path.isdir(os.path.join(outpath, DIR))]
        self.__fileName_Storage = [os.path.splitext(os.path.basename(file)) for file in inpath]
        
        #Filter out unwanted fileTypes
        self.__fileName_Storage = [file for file in self.__fileName_Storage if file[1] == self.__fileType]
        
        self.__compatible, self.__mismatched_fileNames = self.__check_compatibility()
        
        self.__execMode:str
        self.__success:bool
    
        
    @classmethod
    def FDM_fetchFiles(cls, number:int = 7, fileType:str = '.pdf'):
        return cls(askFILES('Select files to realocate.'), askDIR('Select parent directory of file system.'), number, fileType)
    
    @classmethod
    def FDM_fetchDir(cls, number:int = 7, fileType:str = '.pdf'):
        return cls(glob.glob(f"{askDIR('Select a directory of files to realocate.')}/*{fileType}"), askDIR('Select parent directory of file system.'), number, fileType)
            
    def __check_compatibility(self):
        try:
            assert(any([self.__findMatch(file[0]) in self.__dirName_Storage for file in self.__fileName_Storage]))
            return True, []
        except:
            Err_list = [file[0]+file[1] for file in self.__fileName_Storage if self.__findMatch(file[0]) not in self.__dirName_Storage]
            return False, Err_list
        
    def __findMatch(self, basename:str):
        return basename[:self.__number]
        
    def __move(self):
        assert(self.__compatible)
        for file in self.__fileName_Storage:
            shutil.move(src = os.path.join(self.__inpath, file[0]+file[1]),
                        dst = os.path.join(self.__outpath, self.__findMatch(basename = file[0])))
            
    def __copy(self):
        assert(self.__compatible)
        for file in self.__fileName_Storage:
            shutil.copy2(src = os.path.join(self.__inpath, file[0]+file[1]),
                        dst = os.path.join(self.__outpath, self.__findMatch(basename = file[0])))
            
    def execute(self):
        if self.__execMode == 'Move (unsafe)':
            self.__move()
        elif self.__execMode == 'Copy (safe)':
            self.__copy()
            
        self.__success = True
            
    ## Helper Functions
    def get_inpath(self):
        return self.__inpath
    
    def get_outpath(self):
        return self.__outpath
    
    def get_dirName_Storage(self):
        return self.__dirName_Storage
    
    def get_fileName_Storage(self):
        return self.__fileName_Storage
    
    def isCompatible(self):
        return self.__compatible

    def get_mismatchedFiles(self):
        return self.__mismatched_fileNames
    
    def get_numberOfAllocatedFiles(self):
        return self.__fileName_Storage.__len__()
    
    def get_numberOfMatchingDirectories(self):
        return set([self.__findMatch(file[0]) in self.__dirName_Storage for file in self.__fileName_Storage]).__len__()
    
    def get_execMode(self):
        return self.__execMode
    
    def wasSuccessful(self):
        return self.__success
    
    def set_execMode(self, execMode):
        self.__execMode = execMode
        
    def verify(self):
        try:
            assert(len(self.__fileName_Storage))
            assert(len(self.__dirName_Storage))
            assert(self.__compatible)
            assert(self.get_numberOfAllocatedFiles() >= self.get_numberOfMatchingDirectories())
            return True
        except:
            return False