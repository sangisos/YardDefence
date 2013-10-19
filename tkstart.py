# encoding: utf-8
try:  # import as appropriate for 2.x vs. 3.x
    from tkinter import Tk,Canvas,Event,CURRENT
except:
    from Tkinter import Tk,Canvas,Event,CURRENT
from PIL import Image,ImageTk
import os, time
from random import randint,choice
global root
root=Tk()
