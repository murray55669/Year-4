import cv2
import numpy as np
from Tkinter import *
from tkFileDialog import *
from PIL import Image, ImageTk

"""
TODO:
-create dummy page/slide lists
-open image file, display it
-threshold image; recombine with original to eliminate noise
-have clickevents on image recorded
-have 4 clickevents define a crop area, set everything outside of this to transparent
-ability to have multiple crop areas, with more than 4 points, everything outside of *all* of these is set to transparent
"""

PN_W = 1  # page nav width
SN_W = 1  # slide nav width
IE_W = 5  # image edit width

class Master(object):
    def __init__(self):
        self.root = Tk()

        self.root.resizable(width=FALSE, height=FALSE)
        self.root.wm_title("GUI Test")
        self.root.bind('<Escape>', lambda e: self.root.quit())

        self.page_label = Label(self.root, text="Pages")
        self.page_label.grid(row=0, column=0)

        self.slide_label = Label(self.root, text="Slides")
        self.slide_label.grid(row=0, column=0+PN_W)

        self.edit_label = Label(self.root, text="Slide Editor")
        self.edit_label.grid(row=0, column=3+PN_W+SN_W)
        
        self.file_options = {'initialdir': '~/Year-4/PROJ'} # TODO: this should point somewhere more useful
        self.open_file_button = Button(self.root, text="Open File", command=self.open_file)
        self.open_file_button.grid(row=1, column=3+PN_W+SN_W)

        self.image_frame = Label(self.root)
        self.image_frame.grid(row=2, column=0+PN_W+SN_W, columnspan=IE_W)
        self.image_frame.bind("<Button-1>", self.image_clicked)
        self.image_cv = None
        self.image_tk = None

        self.regions = []
        self.points = []
        self.root.bind('<q>', lambda e: self.add_area())
        self.root.bind('<c>', lambda e: self.crop())

        self.crop_flag = False

    def image_clicked(self, event):
        self.points.append((event.x, event.y))
        print "clicked at", event.x, event.y

    def selection_complete(self):
        print "area defined"

    def crop(self):

        self.crop_flag = True
        self.refresh_image()

        print "crop"

    def add_area(self):
        print "add area"

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

        cvimg = cv2.imread(name)
        blur = cv2.GaussianBlur(cvimg, (5, 5), 0)
        blur_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        retval, thresh_gray = cv2.threshold(blur_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh_gray_inv = cv2.bitwise_not(thresh_gray)
        cvimg = cv2.bitwise_and(cvimg, cvimg, mask=thresh_gray_inv)

        b, g, r = cv2.split(cvimg)
        cvimg = cv2.merge((r, g, b, thresh_gray_inv))

        self.image_cv = cvimg
        self.refresh_image()

    def refresh_image(self):
        # scale
        shape = self.image_cv.shape
        width = shape[1]
        scale_ratio = 640 / float(width)
        scaled = cv2.resize(self.image_cv, (0, 0), fx=scale_ratio, fy=scale_ratio)

        # crop
        if self.crop_flag:
            self.crop_flag = False
            # img[y: y + h, x: x + w]
            x1, y1 = self.points[0]
            x2, y2 = self.points[1]
            self.points = []
            scaled = scaled[y1:y2, x1:x2]

        img = Image.fromarray(scaled)
        img_tk = ImageTk.PhotoImage(image=img)
        self.image_tk = img_tk
        self.image_frame.configure(image=self.image_tk)


if __name__ == '__main__':
    master = Master()
    master.run()
