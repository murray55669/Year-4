import cv2
import numpy as np
import json
import random
from Tkinter import *
from tkFileDialog import *
from PIL import Image, ImageTk

"""
TODO:
-be able to define labels with a point (exported as relative %ages relative to image size)
-be able to add text to a slide

-undo/redo label stuff

-make the whole thing scrollable

-set filetypes that can be read - have a special container for reading in saved stuff to load up editor
    -split into CTRL-S / CTRL-E?

-be able to layer images (same crop/ratio, but able to drag the images around?)
"""

POINT_SCALE = 6
POINT_LINE_WIDTH = 2
POINT_CLICK_PADDING = 5
POINT_COLOUR = (255, 0, 255, 255)

LINE_WIDTH = 2
LINE_COLOUR = (128, 0, 128, 255)

NO_COLOUR = (0, 0, 0, 0)

DEBUG_INVALID = "invalid number of points!"

NO_OP = ""
CROP = "crop"
ERASE = "erase"
LABEL_POINT = "label_point"


class Master(object):
    def __init__(self):
        self.root = Tk()
        cols = 0

        self.regions = []
        self.points = []
        self.crop_points = None
        self.scale_ratio = 1.0
        self.labels = []

        self.op_current = StringVar()
        self.op_current.set(NO_OP)
        self.op_history = []
        self.op_history_index = -1

        self.root.resizable(width=FALSE, height=FALSE)
        self.root.wm_title("GUI Test")
        self.root.bind('<Escape>', lambda e: self.escape())
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)  # have the 'X' button close the program

        # Layout
        # ----- #
        self.page_label = Label(self.root, text="Pages")
        self.page_label.grid(row=0, column=cols)
        cols += 1
        # ----- #
        self.slide_label = Label(self.root, text="Slides")
        self.slide_label.grid(row=0, column=cols)
        cols += 1
        # ----- #
        self.edit_label = Label(self.root, text="Slide Editor")
        self.edit_label.grid(row=0, column=cols)
        
        self.file_options = {'initialdir': '~/Year-4/PROJ'}  # TODO: this should point somewhere more useful
        self.open_file_button = Button(self.root, text="Open File", command=self.open_file)
        self.open_file_button.grid(row=1, column=cols)

        self.thresh_slide = Scale(self.root, from_=1, to=255, orient=HORIZONTAL, label="Threshold", showvalue=0,
                                  length=200, command=self.thresh_slide_update, repeatinterval=250)
        self.thresh_slide.set(200)
        self.thresh_slide.grid(row=2, column=cols)

        self.current_op_label = Label(self.root, textvariable=self.op_current)
        self.current_op_label.grid(row=3, column=cols)

        self.image_wrapper = Label(self.root, bg='#e0e0e0', borderwidth=3)
        self.image_wrapper.grid(row=4, column=cols, rowspan=20)
        self.image_frame = Label(self.image_wrapper, bg='#ffffff')
        self.image_frame.pack()
        self.image_frame.bind("<Button-1>", self.image_clicked)
        self.image_orig = None
        self.image_cv = None
        self.image_tk = None
        cols += 1
        # ----- #
        self.label_label = Label(self.root, text="Labels")
        self.label_label.grid(row=0, column=cols)

        self.label_cols = cols
        self.label_rows = 1
        self.label_id = 0
        self.label_id_selected = -1
        # ----- #

        self.root.bind('<Control-C>', lambda e: self.crop())
        self.root.bind('<Control-E>', lambda e: self.erase())
        self.root.bind('<Control-T>', lambda e: self.label())

        self.root.bind('<Control-e>', lambda e: self.export())
        self.root.bind('<Control-s>', lambda e: self.save())

        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())

        self.root.bind('<Return>', lambda e: self.accept())

        # debug
        self.root.bind('<Control-r>', lambda e: self.refresh_image())

        self.running = False  # Tkinter scales are strange

    def escape(self):
        op = self.op_current.get()
        if op == NO_OP:
            if len(self.points) > 0:
                self.points = []
                self.refresh_image()
            else:
                self.root.quit()
        elif op == CROP or op == ERASE:
            if len(self.points) > 0:
                self.points = []
                self.refresh_image()
            else:
                self.no_op()
        else:
            self.no_op()

    def accept(self):
        op = self.op_current.get()
        if op == NO_OP:
            pass
        elif op == CROP:
            self.crop()
        elif op == ERASE:
            self.escape()
        elif op == LABEL_POINT:
            self.label_point(self.label_id_selected)

    def no_op(self):
        self.op_current.set(NO_OP)
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

        if new_point:
            self.add_point((x, y))

        self.refresh_image()

    def add_point(self, point):
        accept_point = True

        op = self.op_current.get()
        if op == CROP:
            if len(self.points) >= 2:
                self.points.pop()
        elif op == LABEL_POINT:
            if len(self.points) >= 1:
                self.points.pop()

        if accept_point:
            self.points.append(point)

        self.refresh_image()

    def crop(self):
        # stage 2 of crop
        if self.op_current.get() == CROP:

            # store current crop
            if self.crop_points:
                prev = self.crop_points
            else:
                prev = None

            if len(self.points) == 2:
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

                self.crop_points = (x1, y1, x2, y2)
                self.no_op()

                self.op_history_add({'op': CROP,
                                     'prev': prev,
                                     'next': self.crop_points})

            elif len(self.points) == 0:
                self.crop_points = None
                self.op_current.set(NO_OP)

                self.op_history_add({'op': CROP,
                                     'prev': prev,
                                     'next': self.crop_points})
            else:
                print DEBUG_INVALID

        # stage 1 of crop
        elif self.op_current.get() == NO_OP:
            self.points = []
            self.op_current.set(CROP)
            print "please enter [0|2] points and hit [CTRL-C|Return]"

        # we have interrupted some other operation
        else:
            self.no_op()
            self.crop()

        self.refresh_image()

    def erase(self):
        if self.op_current.get() == ERASE:
            if len(self.points) > 2:
                print "successfully erased"
                np_points = np.array([self.points])
                prev_image = np.copy(self.image_cv)
                cv2.fillPoly(self.image_cv, np_points, NO_COLOUR)
                next_image = np.copy(self.image_cv)
                self.no_op()

                self.op_history_add({'op': ERASE,
                                     'prev': prev_image,
                                     'next': next_image})
            elif len(self.points) == 0:
                self.no_op()
            else:
                print DEBUG_INVALID

        elif self.op_current.get() == NO_OP:
            self.points = []
            self.op_current.set(ERASE)
            print "please define an area and hit [CTRL-E|Return]"

        else:
            self.no_op()
            self.erase()

        self.refresh_image()

    def label(self):
        print "adding label"
        label = Entry(self.root)
        label.grid(row=self.label_rows, column=self.label_cols)

        colour = "#%06x" % random.randint(0, 0xFFFFFF)

        copy = self.label_id

        button = Button(self.root, command=lambda: self.label_point(copy), bg=colour)
        button.grid(row=self.label_rows, column=self.label_cols+1)

        self.label_rows += 1

        self.labels.append({'id': self.label_id,
                            'label': label,
                            'button': button,
                            'colour': colour,
                            'point': None})
        self.label_id += 1

    def label_point(self, label_id):
        if self.op_current.get() == LABEL_POINT:
            if len(self.points) == 1:
                label = self.get_label_by_id(label_id)
                if label:
                    label['point'] = self.points[0]
                    self.no_op()
            elif len(self.points) == 0:
                self.no_op()
            else:
                print DEBUG_INVALID

            self.label_id_selected = -1

        elif self.op_current.get() == NO_OP:
            self.label_id_selected = label_id
            self.points = []
            label = self.get_label_by_id(label_id)
            if label and label['point']:
                self.add_point(label['point'])
            self.op_current.set(LABEL_POINT)
            print "please select a point and press [The button|Return]"
        else:
            self.label_id_selected = -1
            self.no_op()
            self.label()

        self.refresh_image()

    def get_label_by_id(self, label_id):
        for label in self.labels:
            if label['id'] == label_id:
                return label
        return None

    def export(self):
        print "exporting to output.txt"
        f = open('output.txt', 'w')

        # labels
        label_list = []
        if self.crop_points:
            x1, y1, x2, y2 = self.crop_points
        else:
            shape = self.image_cv.shape
            x1 = 0
            y1 = 0
            x2 = shape[0]
            y2 = shape[1]
        for label in self.labels:
            if label['point']:
                x_pct = ((label['point'][0] - x1) / float(x2 - x1)) * 100
                y_pct = ((label['point'][1] - y1) / float(y2 - y1)) * 100
                label_list.append((x_pct, y_pct, label['label'].get()))
        json.dump({'labels': label_list}, f)

    def save(self):
        # TODO: want to be able to save/reload half-complete edits
        pass

    def op_history_add(self, data):
        # discard anything that could be re-done
        if self.op_history_index < len(self.op_history)-1:
            self.op_history = self.op_history[:self.op_history_index+1]

        self.op_history.append(data)
        self.op_history_index = len(self.op_history)-1

    def undo(self):
        if self.op_history_index >= 0:
            last_op = self.op_history[self.op_history_index]

            op = last_op['op']
            if op == CROP:
                self.crop_points = last_op['prev']
            elif op == ERASE:
                self.image_cv = np.copy(last_op['prev'])

            self.op_history_index -= 1
            self.refresh_image()

    def redo(self):
        if self.op_history_index < len(self.op_history)-1:
            self.op_history_index += 1
            next_op = self.op_history[self.op_history_index]

            op = next_op['op']
            if op == CROP:
                self.crop_points = next_op['next']
            elif op == ERASE:
                self.image_cv = np.copy(next_op['next'])

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
        if name:
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
        if self.image_cv is not None:
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

            # draw indicators for any labels
            for label in self.labels:
                if label['point'] and label['id'] != self.label_id_selected:
                    px, py = label['point']
                    rx = px-x_offset
                    ry = py-y_offset

                    colour = hex_to_rgba(label['colour'])

                    cv2.line(display, (rx-size, ry-size), (rx+size, ry+size), colour, thickness)
                    cv2.line(display, (rx-size, ry+size), (rx+size, ry-size), colour, thickness)

            # depending on current operation, draw lines between points
            op = self.op_current.get()
            if op == CROP:
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
            elif op == ERASE:
                if len(self.points) > 2:
                    if self.crop_points:
                        x1, y1, x2, y2 = self.crop_points
                        adjusted = []
                        for a, b in self.points:
                            adjusted.append((a-x1, b-y1))
                        np_points = np.array([adjusted])
                    else:
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


def hex_to_rgba(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return rgb+(255,)


if __name__ == '__main__':
    master = Master()
    master.run()
