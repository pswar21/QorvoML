import win32com.client
import os
import mdfParser
import shutil
import tkinter.messagebox

def makeMDF(fileName):

    awrde = win32com.client.Dispatch('MWOApp.MWOffice')
    g = awrde.Project.Schematics(1)
    g = awrde.Project.DataFiles(1)

    newDirectory = os.getcwd()
    newFilePath = os.path.join(newDirectory, fileName)
    if os.path.exists(newFilePath):
        a = tkinter.messagebox.askokcancel("Warning", "Making this folder would replace an existing folder, are you sure you want to replace that folder?")
        if a:
            shutil.rmtree(newFilePath)
        else:
            return False
    os.mkdir(newFilePath)

    fp = os.getcwd() + "\\" + fileName + "\\" + fileName + ".mdf"
    g.Export(fp)
    mdfParser.readMDF(fileName)
    g = awrde.Project.Graphs("PAE and Output Power Contours at X dB Compression")
    return True