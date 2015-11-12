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

        self.thresh_slide = Scale(self.root, from_=1, to=255, orient=HORIZONTAL, label="Threshold", showvalue=0,
                                  command=self.thresh_slide_update, length=200)
        self.thresh_slide.set(200)
        self.thresh_slide.grid(row=1, column=1+PN_W+SN_W)

        self.image_wrapper = Label(self.root, image='')
        self.image_wrapper.grid(row=2, column=0+PN_W+SN_W, columnspan=IE_W)
        self.image_frame = Label(self.image_wrapper, bg='#ff00ff')
        self.image_frame.pack()
        self.image_frame.bind("<Button-1>", self.image_clicked)
        self.image_orig = None
        self.image_cv = None
        self.image_tk = None

        self.regions = []
        self.points = []
        self.crop_points = None
        self.scale_ratio = 1.0

        self.root.bind('<q>', lambda e: self.add_area())
        self.root.bind('<c>', lambda e: self.crop())

    def image_clicked(self, event):

        # get relative co-ordinates on full image
        x = int(event.x / self.scale_ratio)
        y = int(event.y / self.scale_ratio)

        # if cropped, offset
        if self.crop_points:
            x1, y1, x2, y2 = self.crop_points
            x += x1
            y += y1

        self.points.append((x, y))
        print "clicked at", event.x, event.y, "translated to", x, y

    def selection_complete(self):
        print "area defined"

    def crop(self):
        if len(self.points) >= 2:
            x1, y1 = self.points[0]
            x2, y2 = self.points[1]

            print "crop:", x1, x2, y1, y2

            self.points = []

            self.crop_points = (x1, y1, x2, y2)

            self.refresh_image()
        else:
            print "not enough points to crop, resetting crop"
            self.points = []
            self.crop_points = None
            self.refresh_image()

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

        self.image_orig = cv2.imread(name)

        self.image_cv = thresh_image(self.image_orig, self.thresh_slide.get())
        self.refresh_image()

    def thresh_slide_update(self, xd):
        print xd
        self.image_cv = thresh_image(self.image_orig, self.thresh_slide.get())
        self.refresh_image()

    def refresh_image(self):
        display = self.image_cv

        if self.crop_points:
            x1, y1, x2, y2 = self.crop_points
            # crop
            # img[y: y + h, x: x + w]
            display = display[y1:y2, x1:x2]
            self.scale_ratio = calc_scale_ratio(display)
            # scale
            display = cv2.resize(display, (0, 0), fx=self.scale_ratio, fy=self.scale_ratio)
        else:
            self.scale_ratio = calc_scale_ratio(self.image_cv)
            # scale
            display = cv2.resize(display, (0, 0), fx=self.scale_ratio, fy=self.scale_ratio)

        img = Image.fromarray(display)
        img_tk = ImageTk.PhotoImage(image=img)
        self.image_tk = img_tk
        self.image_frame.configure(image=self.image_tk)

def thresh_image(image, thresh_val):
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    blur_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    retval, thresh_gray = cv2.threshold(blur_gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    threshed = cv2.bitwise_and(image, image, mask=thresh_gray)

    b, g, r = cv2.split(threshed)
    return cv2.merge((r, g, b, thresh_gray))

def calc_scale_ratio(image):
    shape = image.shape
    width = shape[1]
    return 640 / float(width)

if __name__ == '__main__':
    master = Master()
    master.run()
