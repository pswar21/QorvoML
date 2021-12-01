import tkinter
from tkinter.constants import CENTER
from tkinter.ttk import *
import Test
import mdfParser
import models
import os
import numpy as np


class myGUI():
    def __init__(self):
        self.poly = None
        self.effModel = None
        self.powModel = None
        self.GUI = tkinter.Tk()
        self.GUI.title("Machine Learning for Load Pull Simulations")
        self.GUI.geometry("300x400")
        self.GUI.resizable(False, False)

        self.fileEntry = Entry(self.GUI, width=20)
        self.fileEntry.bind('<Return>', self.runSimulation)
        self.fileEntry.place(relx=.5, rely=.05, anchor=CENTER)
        self.fileCreatedLabel = tkinter.Label(self.GUI)

        entryButton = tkinter.ttk.Button(self.GUI, text="Submit File Name", width=20, command=self.runSimulation)
        entryButton.place(relx=.5, rely=.15, anchor=CENTER)


        self.GUI.mainloop()

    def runSimulation(self, a=None):
        fileName = self.fileEntry.get()
        self.fileCreatedLabel.place(relx=.5, rely=.23, anchor=CENTER)
        if not len(fileName):
            self.fileCreatedLabel.config(text="Must have a File Name")
            return

        a = Test.makeMDF(fileName)
        if not a:
            return
        self.fileCreatedLabel.config(text="File Created")

        self.powModel, self.effModel, self.poly = models.makeModel(fileName + "//" + fileName)
        self.launchApp()

    def launchApp(self):


        showEffGraphButton = tkinter.ttk.Button(self.GUI, text="Show Efficiency Graph", command=self.printEffGraph, width=20)
        showEffGraphButton.place(relx=.25, rely=.3, anchor=CENTER)

        showPowGraphButton = tkinter.ttk.Button(self.GUI, text="Show Power Graph", command=self.printPowGraph, width=20)
        showPowGraphButton.place(relx=.75, rely=.3, anchor=CENTER)

        button = tkinter.ttk.Button(self.GUI, text="Get Max Power and Efficiency Points", width=40, command=self.predictMax)
        button.place(relx=.5, rely=.45, anchor=CENTER)

        predictButton = tkinter.ttk.Button(self.GUI, text="Predict Power and Efficiency at Point", width=40,
                                           command=self.predictPoint)
        predictButton.place(relx=.5, rely=.7, anchor=CENTER)

        xlabel = tkinter.Label(self.GUI, text="x")
        xlabel.place(relx=.3, rely=.77, anchor=CENTER)

        ylabel = tkinter.Label(self.GUI, text="r")
        ylabel.place(relx=.7, rely=.77, anchor=CENTER)

        self.predictx = Entry(self.GUI, width=10)
        self.predictx.place(relx=.3, rely=.84, anchor=CENTER)

        self.predicty = Entry(self.GUI, width=10)
        self.predicty.place(relx=.7, rely=.84, anchor=CENTER)

        self.predictErrorLabel = tkinter.Label(self.GUI, text="Invalid inputs (x and y must be -0.8 to 0.8)")

        predictXLabel = tkinter.Label(self.GUI)
        predictXLabel.place(anchor=CENTER, relx=.25, rely=.93)

        predictYLabel = tkinter.Label(self.GUI)
        predictYLabel.place(anchor=CENTER, relx=.75, rely=.93)

    def predictMax(self):
        bestEff, bestEffPoint = models.getMax((self.effModel, self.poly))
        bestPow, bestPowPoint = models.getMax((self.powModel, self.poly))
        real1, imaginary1 = models.cartesianToSmith(bestEffPoint[0, 0], bestEffPoint[0, 1])
        real2, imaginary2 = models.cartesianToSmith(bestPowPoint[0, 0], bestPowPoint[0, 1])
        self.maxELabel = tkinter.Label(self.GUI, text="Best Efficiency : {:2.1f}% at X={:.3f}, R={:.3f}".format(bestEff, real1, imaginary1))
        self.maxELabel.place(relx=.5, rely = .51, anchor=CENTER)
        self.maxPLabel = tkinter.Label(self.GUI, text="Best Power : {:.3f}dBm at X={:.3f}, R={:.3f}".format(bestPow, real2,imaginary2))
        self.maxPLabel.place(relx=.5, rely=.57, anchor=CENTER)

    def predictPoint(self):
        self.predictErrorLabel.place_forget()
        x = self.predictx.get()
        y = self.predicty.get()
        try:
            float(x)
            float(y)
        except:
            self.predictErrorLabel.place(relx=.5, rely=.94, anchor=CENTER)
            return
        if float(x) < -.8 or float(x) > .8 or float(y) < -.8 or float(y) > .8:
            self.predictErrorLabel.place(relx=.5, rely=.94, anchor=CENTER)
            return
        X_transform = self.poly.fit_transform(np.array([[x, y]]))
        predictEff = self.effModel.predict(X_transform)
        predictPow = self.powModel.predict(X_transform)
        print(predictEff, predictPow)
        self.predictELabel = tkinter.Label(self.GUI, text="Efficiency at point : {:2.1f}%".format(predictEff[0]))
        self.predictELabel.place(relx=.5, rely = .91, anchor=CENTER)
        self.predictPLabel = tkinter.Label(self.GUI, text="Power at point : {:2.1f}%".format(predictPow[0]))
        self.predictPLabel.place(relx=.5, rely=.96, anchor=CENTER)

    def printEffGraph(self):
        models.printGraph((self.effModel, self.poly), "e")

    def printPowGraph(self):
        models.printGraph((self.powModel, self.poly), "p")

if __name__ == "__main__":
    g = myGUI()
