import cv2
import numpy as np
from Tkinter import *
from tkFileDialog import *

"""
TODO:
-create dummy page/slide slists
-open image file, display it
-threshold image; recombine with original to eliminate noise
-have clickevents on image recorded
-have 4 clickevents define a crop area, set everything outside of this to transparent
-ability to have multiple crop areas, with more than 4 points, everything outside of *all* of these is set to transparent
"""

PAGENAV_WIDTH = 1
SLIDENAV_WIDTH = 1
IMAGEEDIT_WIDTH = 1

class Master(object):
    def __init__(self):
        self.root = Tk()
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.wm_title("GUI Test")
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        self.test_label = Label(self.root, text="Slide Editor")
        self.test_label.grid(row=0, column=0)
        
        self.file_options = {}
        self.file_options['initialdir'] = '~/'
        self.open_file_button = Button(self.root, text="Open File", command=self.open_file)
        self.open_file_button.grid(row=1, column=0)
        
    def run(self):
        try:
            self.root.mainloop()
        except:
            raise
        finally:
            print "Exiting..."
            
    def open_file(self):
        name = askopenfilename(**self.file_options)
        self.file_options['initialdir'] = name.rsplit('/', 1)[0]
        file = open(name, 'r+')
        for line in file:
            print line.strip()
            
if __name__ == '__main__':
    master = Master()
    master.run()