from Tkinter import *
from pyapp.constants import *
import numpy as np
from pyapp.utils import *

class Page():
    def __init__(self):
        # slides
        self.slides = []
        self.slide_index = IntVar()
        self.slide_index.set(-1)

        # image
        self.crop_points = None
        self.scale_ratio = 1.0
        self.points = []

        # Undo/redo
        self.op_current = StringVar()
        self.op_history = []
        self.op_history_index = -1

        self.op_current.set(NO_OP)

        # title
        self.title_entry = None
        self.title_var = StringVar()

        self.path = ""

    def slide(self):
        if self.slides:
            return self.slides[self.slide_index.get()]
        else:
            return None

    def slide_index_to_string(self):
        return "Slide: "+str(self.slide_index.get()+1)+"/"+str(len(self.slides))

    def op_history_add(self, data):
        # data is a dictionary
        data[HIST_SLIDE_INDEX] = self.slide_index.get()
        # discard anything that could be re-done
        if self.op_history_index < len(self.op_history)-1:
            self.op_history = self.op_history[:self.op_history_index+1]

        self.op_history.append(data)
        self.op_history_index = len(self.op_history)-1

    def undo(self):
        # acts on the current action being pointed to
        if self.op_history_index >= 0:
            last_op = self.op_history[self.op_history_index]
            target_slide_index = last_op[HIST_SLIDE_INDEX]

            op = last_op[HIST_OP]
            if op == CROP:
                self.crop_points = last_op[HIST_PREV]
            elif op == ERASE:
                self.slides[target_slide_index].image_cv = thresh_image(np.copy(
                    self.slides[target_slide_index].image_orig), last_op[HIST_THRESH])

                for prev in self.op_history[:self.op_history_index]:
                    if prev[HIST_OP] == ERASE and prev[HIST_SLIDE_INDEX] == target_slide_index:
                        cv2.fillPoly(self.slides[target_slide_index].image_cv, prev[HIST_POINTS], NO_COLOUR)

            elif op == ADD_LABEL:
                # purge label/button from visible
                last_op['label'].grid_forget()
                last_op['button'].grid_forget()
                self.slide().label_rows -= 1

                self.slides[target_slide_index].labels = \
                    [l for l in self.slides[target_slide_index].labels if not l['id'] == last_op['id']]

            elif op == LABEL_POINT:
                last_op[HIST_LABEL]['point'] = last_op[HIST_PREV]
            elif op == MOVE_LAYER:
                self.slides[target_slide_index].offset = last_op[HIST_PREV]

            self.op_history_index -= 1

            for slide in self.slides:
                slide.dirty = True

    def redo(self):
        # acts on the action after the one being pointed to
        if self.op_history_index < len(self.op_history)-1:
            self.op_history_index += 1
            next_op = self.op_history[self.op_history_index]

            op = next_op['op']
            if op == CROP:
                self.crop_points = next_op['current']
            elif op == ERASE:
                cv2.fillPoly(self.slides[next_op[HIST_SLIDE_INDEX]].image_cv, next_op[HIST_POINTS], NO_COLOUR)
            elif op == ADD_LABEL:
                # make label/button visible
                next_op['label'].grid(row=self.slide().label_rows, column=next_op['grid_col'])
                next_op['button'].grid(row=self.slide().label_rows, column=next_op['grid_col']+1)
                self.slide().label_rows += 1

                self.slides[next_op[HIST_SLIDE_INDEX]].labels.append(next_op)

            elif op == LABEL_POINT:
                next_op[HIST_LABEL]['point'] = next_op[HIST_CURRENT]
            elif op == MOVE_LAYER:
                self.slides[next_op[HIST_SLIDE_INDEX]].offset = next_op[HIST_CURRENT]

            for slide in self.slides:
                slide.dirty = True