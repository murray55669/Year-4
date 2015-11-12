import cv2
import numpy as np
from Tkinter import *
from tkFileDialog import *
from PIL import Image, ImageTk
from multiprocessing import Process

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

POINT_WIDTH = 2
POINT_SCALE = 6
POINT_CLICK_PADDING = 5
POINT_COLOUR = (255, 0, 255, 255)

LINE_WIDTH = 2
LINE_COLOUR = (128, 0, 128, 255)

class Master(object):
    def __init__(self):
        self.root = Tk()

        self.root.resizable(width=FALSE, height=FALSE)
        self.root.wm_title("GUI Test")
        self.root.bind('<Escape>', lambda e: self.escape())
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)  # have the 'X' button close the program

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
                                  length=200, command=self.thresh_slide_update, repeatinterval=250)
        self.thresh_slide.set(200)
        self.thresh_slide.grid(row=1, column=1+PN_W+SN_W)

        self.image_wrapper = Label(self.root, bg='#e0e0e0', borderwidth=3)
        self.image_wrapper.grid(row=2, column=0+PN_W+SN_W, columnspan=IE_W)
        self.image_frame = Label(self.image_wrapper, bg='#ffffff')
        self.image_frame.pack()
        self.image_frame.bind("<Button-1>", self.image_clicked)
        self.image_orig = None
        self.image_cv = None
        self.image_tk = None

        self.regions = []
        self.points = []
        self.crop_points = None
        self.scale_ratio = 1.0

        self.current_op = StringVar()
        self.current_op.set("")

        self.current_op_label = Label(self.root, textvariable=self.current_op)
        self.current_op_label.grid(row=1, column=2+PN_W+SN_W)

        self.root.bind('<q>', lambda e: self.add_area())
        self.root.bind('<c>', lambda e: self.crop())

        # debug
        self.root.bind('<r>', lambda e: self.refresh_image())

        self.running = False  # Tkinter scales are strange

    def escape(self):
        if self.current_op.get() == "":
            if len(self.points) > 0:
                self.points = []
                self.refresh_image()
            else:
                self.root.quit()
        else:
            self.current_op.set("")
            self.reset_points()
            self.refresh_image()

    def image_clicked(self, event):

        # get relative co-ordinates on full image
        x = int(event.x / self.scale_ratio)
        y = int(event.y / self.scale_ratio)

        # if cropped, offset
        if self.crop_points:
            x1, y1, x2, y2 = self.crop_points
            x += x1
            y += y1

        size = self.point_size() + POINT_CLICK_PADDING
        new_point = True
        # check if spot clicked is already a point
        for index, pt in enumerate(self.points):
            px, py = pt
            if x in range(px-size, px+size+1) and y in range(py-size, py+size+1):
                del self.points[index]
                new_point = False
                break

        accept_point = True
        if new_point:
            if self.current_op.get() == "crop":
                if len(self.points) >= 2:
                    accept_point = False

            if accept_point:
                self.points.append((x, y))

        self.refresh_image()

    def selection_complete(self):
        print "area defined"

    def crop(self):
        # stage 2 of crop
        if self.current_op.get() == "crop":
            if len(self.points) == 2:
                print "successfully cropped"
                # finalize the crop
                xa, ya = self.points[0]
                xb, yb = self.points[1]
                if xa <= xb:
                    x1 = xa
                    x2 = xb
                else:
                    x1 = xb
                    x2 = xa
                if ya <= yb:
                    y1 = ya
                    y2 = yb
                else:
                    y1 = yb
                    y2 = ya
                self.reset_points()
                self.crop_points = (x1, y1, x2, y2)
                self.current_op.set("")
                self.refresh_image()
            elif len(self.points) == 0:
                print "resetting crop"
                self.reset_points()
                self.current_op.set("")
                self.refresh_image()
            else:
                print "invalid number of points!"
                self.refresh_image()

        # stage 1 of crop
        elif self.current_op.get() == "":
            self.points = []
            self.current_op.set("crop")
            print "please enter [0|2] points and hit C"

        # we have interrupted some other operation
        else:
            pass

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
        self.reset_points()
        self.image_cv = thresh_image(self.image_orig, self.thresh_slide.get())
        self.refresh_image()

    def reset_points(self):
        self.points = []
        self.regions = []
        self.crop_points = None

    def thresh_slide_update(self, val):
        if self.running:
            self.image_cv = thresh_image(self.image_orig, self.thresh_slide.get())
            self.refresh_image()
        else:
            self.running = True

    def refresh_image(self):
        # don't lose the original information
        display = np.copy(self.image_cv)

        x_offset = 0
        y_offset = 0

        if self.crop_points:
            x1, y1, x2, y2 = self.crop_points
            # crop
            # img[y: y + h, x: x + w]
            display = display[y1:y2, x1:x2]
            x_offset = x1
            y_offset = y1

        self.scale_ratio = calc_scale_ratio(display)

        # draw anything else on top of the base image
        # scale for drawings
        size = self.point_size()

        # draw crosses to show points
        for p_x, p_y in self.points:
            # point offset due to cropping
            r_x = p_x-x_offset
            r_y = p_y-y_offset

            cv2.line(display, (r_x-size, r_y-size), (r_x+size, r_y+size), POINT_COLOUR, int(POINT_WIDTH/self.scale_ratio))
            cv2.line(display, (r_x-size, r_y+size), (r_x+size, r_y-size), POINT_COLOUR, int(POINT_WIDTH/self.scale_ratio))

        # depending on current operation, draw lines between points
        if self.current_op.get() == "crop":
            if len(self.points) == 2:
                x1, y1 = self.points[0]
                x2, y2 = self.points[1]
                x1 -= x_offset
                x2 -= x_offset
                y1 -= y_offset
                y2 -= y_offset

                cv2.line(display, (x1, y1), (x2, y1), LINE_COLOUR, int(LINE_WIDTH/self.scale_ratio))
                cv2.line(display, (x2, y1), (x2, y2), LINE_COLOUR, int(LINE_WIDTH/self.scale_ratio))
                cv2.line(display, (x2, y2), (x1, y2), LINE_COLOUR, int(LINE_WIDTH/self.scale_ratio))
                cv2.line(display, (x1, y2), (x1, y1), LINE_COLOUR, int(LINE_WIDTH/self.scale_ratio))

        # scale
        display = cv2.resize(display, (0, 0), fx=self.scale_ratio, fy=self.scale_ratio)

        img = Image.fromarray(display)
        img_tk = ImageTk.PhotoImage(image=img)
        self.image_tk = img_tk
        self.image_frame.configure(image=self.image_tk)

    def point_size(self):
        return int(POINT_SCALE/self.scale_ratio)


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
