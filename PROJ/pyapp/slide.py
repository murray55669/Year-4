from pyapp.constants import *
from pyapp.utils import *
import numpy as np


class Slide(object):
    def __init__(self):
        self.labels = []

        self.label_rows = 1
        self.label_entries = []
        self.label_buttons = []
        self.flip_buttons = []
        self.label_id = 0

        self.thresh_value = THRESH_DEFAULT

        self.text_text = None

        self.image_orig = None
        self.image_cv = None
        self.image_render = None

        self.dirty = True

        self.offset = None

    def render(self, crop_points):
        if self.image_cv is not None and self.dirty:

            if self.offset:
                rows = self.image_cv.shape[0]
                cols = self.image_cv.shape[1]

                translate = np.float32([[1, 0, self.offset[0]], [0, 1, self.offset[1]]])

                self.image_render = cv2.warpAffine(self.image_cv, translate, (cols, rows))
            else:
                self.image_render = np.copy(self.image_cv)

            if crop_points:
                x1, y1, x2, y2 = crop_points
                # crop
                # img[y: y + h, x: x + w]
                self.image_render = self.image_render[y1:y2, x1:x2]

            self.dirty = False

