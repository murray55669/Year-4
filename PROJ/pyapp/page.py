from Tkinter import *
from pyapp.utils import *
import numpy as np
from pyapp.constants import *


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

        # icon
        self.thumb = None
        self.thumb_tk = None

        # title
        self.title_entry = None

        self.path = ""

    def render_thumbnail(self):
        self.slides[0].render(self.crop_points)
        display = np.copy(self.slides[0].image_thumbnail)

        images = [display]
        for i, slide in enumerate(self.slides):
            if i > 0:
                slide.render(self.crop_points)
                temp = np.copy(slide.image_thumbnail)
                images.append(temp)

        final_image = stack_images(images)

        self.thumb = Image.fromarray(final_image)

    def slide(self):
        if self.slides:
            return self.slides[self.slide_index.get()]
        else:
            return None

    def slide_index_to_string(self):
        return "Slide: "+str(self.slide_index.get()+1)+"/"+str(len(self.slides))

    def op_history_add(self, data):
        # TODO: remember slide index
        # discard anything that could be re-done
        if self.op_history_index < len(self.op_history)-1:
            self.op_history = self.op_history[:self.op_history_index+1]

        self.op_history.append(data)
        self.op_history_index = len(self.op_history)-1

    def undo(self):
        # TODO: act upon slide index; dirty slides
        pass
        """
        if self.op_history_index >= 0:
            last_op = self.op_history[self.op_history_index]

            op = last_op['op']
            if op == CROP:
                self.crop_points = last_op['prev']
            elif op == ERASE:
                self.slides[0].image_cv = np.copy(last_op['prev'])  # TODO: broken

            self.op_history_index -= 1
        self.refresh_image()
        """

    def redo(self):
        # TODO: act upon slide index; dirty slides
        pass
        """
        if self.op_history_index < len(self.op_history)-1:
            self.op_history_index += 1
            next_op = self.op_history[self.op_history_index]

            op = next_op['op']
            if op == CROP:
                self.crop_points = next_op['next']
            elif op == ERASE:
                self.slides[0].image_cv = np.copy(next_op['next'])  # TODO: broken
        self.refresh_image()
        """