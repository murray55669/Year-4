import cv2
import numpy as np
from Tkinter import *
from tkFileDialog import *
from PIL import Image, ImageTk
from itertools import izip, tee

"""
TODO:
-create dummy page/slide lists
-open image file, display it
-threshold image; recombine with original to eliminate noise
-have clickevents on image recorded
-have 4 clickevents define a crop area, set everything outside of this to transparent
-ability to have multiple crop areas, with more than 4 points, everything outside of *all* of these is set to transparent

-store history of operations + relevant data eg: [('crop', (x1, y1, x2, y2)), ('crop', (x3, y3, x4, y4))] to be able to undo/redo in a queue fashion
"""

PN_W = 1  # page nav width
SN_W = 1  # slide nav width
IE_W = 5  # image edit width

POINT_SCALE = 6
POINT_LINE_WIDTH = 2
POINT_CLICK_PADDING = 5
POINT_COLOUR = (255, 0, 255, 255)

LINE_WIDTH = 2
LINE_COLOUR = (128, 0, 128, 255)

NO_COLOUR = (0, 0, 0, 0)

DEBUG_INVALID = "invalid number of points!"

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

        self.op_current = StringVar()
        self.op_current.set("")
        self.op_history = []
        self.op_history_index = -1

        self.current_op_label = Label(self.root, textvariable=self.op_current)
        self.current_op_label.grid(row=1, column=2+PN_W+SN_W)

        self.root.bind('<e>', lambda e: self.erase())
        self.root.bind('<c>', lambda e: self.crop())
        self.root.bind('<z>', lambda e: self.undo())
        self.root.bind('<y>', lambda e: self.redo())

        # debug
        self.root.bind('<r>', lambda e: self.refresh_image())

        self.running = False  # Tkinter scales are strange

    def escape(self):
        op = self.op_current.get()
        if op == "":
            if len(self.points) > 0:
                self.points = []
                self.refresh_image()
            else:
                self.root.quit()
        elif op == "crop" or op == "erase":
            if len(self.points) > 0:
                self.points = []
                self.refresh_image()
            else:
                self.op_current.set("")
                self.points = []
                self.refresh_image()
        else:
            self.op_current.set("")
            self.points = []
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

        size = self.scale_constant(POINT_SCALE) + POINT_CLICK_PADDING
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
            if self.op_current.get() == "crop":
                if len(self.points) >= 2:
                    self.points.pop()

            if accept_point:
                self.points.append((x, y))

        self.refresh_image()

    def crop(self):
        # stage 2 of crop
        if self.op_current.get() == "crop":

            # store current crop
            if self.crop_points:
                prev = self.crop_points
            else:
                prev = None

            if len(self.points) == 2:
                print "successfully cropped"
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

                self.points = []
                self.crop_points = (x1, y1, x2, y2)
                self.op_current.set("")

                self.op_history_add({'op': 'crop',
                                     'prev': prev,
                                     'curr': self.crop_points})

            elif len(self.points) == 0:
                print "resetting crop"
                self.crop_points = None
                self.op_current.set("")

                self.op_history_add({'op': 'crop',
                                     'prev': prev,
                                     'curr': self.crop_points})
            else:
                print DEBUG_INVALID

        # stage 1 of crop
        elif self.op_current.get() == "":
            self.points = []
            self.op_current.set("crop")
            print "please enter [0|2] points and hit C"

        # we have interrupted some other operation
        else:
            pass

        self.refresh_image()

    def erase(self):
        if self.op_current.get() == "erase":
            if len(self.points) > 2:
                print "successfully erased"
                np_points = np.array([self.points])
                cv2.fillPoly(self.image_cv, np_points, NO_COLOUR)
                self.points = []
                self.op_current.set("")
            elif len(self.points) == 0:
                self.op_current.set("")
            else:
                print DEBUG_INVALID

        elif self.op_current.get() == "":
            self.points = []
            self.op_current.set("erase")
            print "please define an area and hit E"

        else:
            pass

        self.refresh_image()

    def op_history_add(self, data):
        # TODO: broken? undo-op-undo/redo kills things
        # discard anything that could be re-done
        if self.op_history_index < len(self.op_history)-1:
            self.op_history = self.op_history[:self.op_history_index]

        self.op_history.append(data)
        self.op_history_index = len(self.op_history)-1

    def undo(self):
        if self.op_history_index >= 0:
            last_op = self.op_history[self.op_history_index]

            if last_op['op'] == "crop":
                self.crop_points = last_op['prev']

            self.op_history_index -= 1
            self.refresh_image()

    def redo(self):
        if self.op_history_index < len(self.op_history)-1:
            self.op_history_index += 1
            next_op = self.op_history[self.op_history_index]

            if next_op['op'] == "crop":
                self.crop_points = next_op['curr']

            self.refresh_image()

    def run(self):
        try:
            self.root.mainloop()
        except:
            self.reset_all()
            self.refresh_image()
            raise
        finally:
            print "Exiting..."
            
    def open_file(self):
        name = askopenfilename(**self.file_options)
        self.file_options['initialdir'] = name.rsplit('/', 1)[0]

        self.image_orig = cv2.imread(name)
        self.reset_all()
        self.image_cv = thresh_image(self.image_orig, self.thresh_slide.get())
        self.refresh_image()

    def reset_all(self):
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
        # scale to match crop area
        size = self.scale_constant(POINT_SCALE)
        thickness = self.scale_constant(POINT_LINE_WIDTH)

        # draw crosses to show points
        for p_x, p_y in self.points:
            # point offset due to cropping
            r_x = p_x-x_offset
            r_y = p_y-y_offset

            cv2.line(display, (r_x-size, r_y-size), (r_x+size, r_y+size), POINT_COLOUR, thickness)
            cv2.line(display, (r_x-size, r_y+size), (r_x+size, r_y-size), POINT_COLOUR, thickness)

        # depending on current operation, draw lines between points
        op = self.op_current.get()
        if op == "crop":
            if len(self.points) == 2:
                x1, y1 = self.points[0]
                x2, y2 = self.points[1]
                x1 -= x_offset
                x2 -= x_offset
                y1 -= y_offset
                y2 -= y_offset

                thickness = self.scale_constant(LINE_WIDTH)
                cv2.line(display, (x1, y1), (x2, y1), LINE_COLOUR, thickness)
                cv2.line(display, (x2, y1), (x2, y2), LINE_COLOUR, thickness)
                cv2.line(display, (x2, y2), (x1, y2), LINE_COLOUR, thickness)
                cv2.line(display, (x1, y2), (x1, y1), LINE_COLOUR, thickness)
        elif op == "erase":
            if len(self.points) > 2:
                np_points = np.array([self.points])
                cv2.fillPoly(display, np_points, LINE_COLOUR)

        # scale
        display = cv2.resize(display, (0, 0), fx=self.scale_ratio, fy=self.scale_ratio)

        img = Image.fromarray(display)
        img_tk = ImageTk.PhotoImage(image=img)
        self.image_tk = img_tk
        self.image_frame.configure(image=self.image_tk)

    def scale_constant(self, constant):
        return int(constant/self.scale_ratio)


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

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

if __name__ == '__main__':
    master = Master()
    master.run()
