import tkinter as tk
from tkinter import filedialog

def askDIR(title:str = 'Choose a directory to open.'):
    root = tk.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    DIR_path = filedialog.askdirectory(title=title)
    return DIR_path

def askFILE(title:str = 'Choose a single file to open.'):
    root = tk.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    FILE_path = filedialog.askopenfilename(title=title)
    return FILE_path

def askFILES(title:str = 'Choose multiple files to open.', fileTypes:list = []):
    root = tk.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    FILE_path = filedialog.askopenfilenames(title=title, filetypes=fileTypes)
    return FILE_path 