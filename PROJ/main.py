import json
import random
import shutil
import os
import time
from tkFileDialog import *
from tkMessageBox import askyesno
from pyapp.slide import *
from pyapp.page import *
from pyapp.constants import *
from pyapp.utils import *

"""
TODO:
EDITOR:
-REFACTOR REFACTOR REFACTOR

-delete slide option? delete page option?

-some way to pass in/set an offset for "page-index" when exporting to easy chopping stuff together
"""


class Gui(object):
    def __init__(self):
        # check if a temp folder exits, if so wipe it
        # TODO: load from this folder instead
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
            time.sleep(1)
        os.mkdir(TEMP_DIR)

        self.loaded = False
        self.master = Tk()
        self.master.wm_title("Page Selector")

        # page browser
        self.page_label = Label(self.master, text="Pages")
        self.page_label.grid(row=0, column=0)
        self.package_title_label = Label(self.master, text="Package Title")
        self.package_title_label.grid(row=1, column=0)
        self.package_title_entry = Entry(self.master)
        self.package_title_entry.grid(row=2, column=0)
        self.add_page_button = Button(self.master, text="Add Page", command=self.new_page)
        self.add_page_button.grid(row=3, column=0)

        self.scroll_wrapper = Frame(self.master)
        self.scroll_wrapper.grid(row=4, column=0)
        self.page_canvas = Canvas(self.scroll_wrapper, borderwidth=0, width=THUMBNAIL_WIDTH+5, height=3*THUMBNAIL_WIDTH)
        self.page_frame = Frame(self.page_canvas)
        self.page_scroll = Scrollbar(self.scroll_wrapper, orient="vertical", command=self.page_canvas.yview)
        self.page_canvas.configure(yscrollcommand=self.page_scroll.set)

        self.page_scroll.pack(side="right", fill="y")
        self.page_canvas.pack(side="left", fill="both", expand=True)
        self.page_canvas.create_window((0, 0), window=self.page_frame, anchor="nw", tags="self.page_frame",
                                       width=THUMBNAIL_WIDTH+5)

        self.page_frame.bind("<Configure>", self.page_frame_update)

        self.page_row = 0
        self.page_fake_index = 0

        self.page_buttons = []

        # editor
        self.root = Toplevel(self.master)
        # pages
        self.pages = []
        self.page_index = IntVar()
        self.page_index.set(-1)
        self.new_page()

        # UI
        self.slide_index_text = StringVar()
        self.slide_index_text.set(self.page().slide_index_to_string())
        self.display_layers = True
        cols = 0

        self.root.resizable(width=FALSE, height=FALSE)
        self.root.wm_title("Slide Editor")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)  # have the 'X' button close the program
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

        # Layout
        # ----- #
        self.slide_label = Label(self.root, text="Slides")
        self.slide_label.grid(row=0, column=cols)

        self.file_options = {'initialdir': '~/Year-4/PROJ'}  # TODO: this should save/reload instead of having default
        self.open_file_button = Button(self.root, text="Add Slide", command=self.open_file)
        self.open_file_button.grid(row=1, column=cols)

        self.slide_up = Button(self.root, text=u'\u2191', command=self.slide_next)
        self.slide_up.grid(row=2, column=cols)

        self.current_slide_label = Label(self.root, textvariable=self.slide_index_text)
        self.current_slide_label.grid(row=3, column=cols)

        self.slide_down = Button(self.root, text=u'\u2193', command=self.slide_prev)
        self.slide_down.grid(row=4, column=cols)
        cols += 1
        # ----- #
        self.edit_label = Label(self.root, text="Slide")
        self.edit_label.grid(row=0, column=cols)
        self.title_label = Label(self.root, text="Title")
        self.title_label.grid(row=1, column=cols)
        # row 2 is from the page
        self.current_op_label = Label(self.root, textvariable=self.page().op_current)
        self.current_op_label.grid(row=3, column=cols)

        self.thresh_slide = Scale(self.root, from_=1, to=255, orient=HORIZONTAL, label="Threshold", showvalue=0,
                                  length=200, command=self.thresh_slide_update, repeatinterval=250)
        self.thresh_slide.set(THRESH_DEFAULT)
        self.thresh_slide.grid(row=4, column=cols)

        self.image_wrapper = Label(self.root, bg='#e0e0e0', borderwidth=3)
        self.image_wrapper.grid(row=5, column=cols, rowspan=50)
        self.image_tk = blank_image(self.root)
        self.image_frame = Label(self.image_wrapper, bg='#ffffff', image=self.image_tk)
        self.image_frame.pack()

        self.image_frame.bind("<Button-1>", self.image_clicked)
        self.image_frame.bind("<B1-Motion>", self.image_dragged)

        self.editor_col = cols
        cols += 1
        # ----- #
        self.details_label = Label(self.root, text="Slide Details")
        self.details_label.grid(row=0, column=cols)
        self.text_label = Label(self.root, text="Text")
        self.text_label.grid(row=1, column=cols)
        # row 2 is from the slide
        self.details_col = cols
        cols += 1
        # ----- #
        self.label_label = Label(self.root, text="Labels")
        self.label_label.grid(row=0, column=cols)

        self.label_cols = cols
        self.label_id_selected = -1
        # ----- #

        # bind keys to all windows
        roots = [self.master, self.root]
        for root in roots:
            root.bind('<Control-C>', lambda e: self.crop())
            root.bind('<Control-E>', lambda e: self.erase())
            root.bind('<Control-T>', lambda e: self.label())
            root.bind('<Control-D>', lambda e: self.move_layer())

            root.bind('<Control-V>', lambda e: self.toggle_layers())

            root.bind('<Control-e>', lambda e: self.export())
            root.bind('<Control-s>', lambda e: self.save())
            root.bind('<Control-o>', lambda e: self.open_file())

            root.bind('<Control-z>', lambda e: self.undo())
            root.bind('<Control-y>', lambda e: self.redo())

            root.bind('<Escape>', lambda e: self.escape())
            root.bind('<Return>', lambda e: self.accept())
            # debug
            root.bind('<Control-r>', lambda e: self.refresh_image())

        self.running = False  # Tkinter scales are strange

        self.page_go_to(len(self.pages)-1)
        self.loaded = True

    def page_frame_update(self, event):
        self.page_canvas.configure(scrollregion=self.page_canvas.bbox("all"))

    def new_page(self):
        new_page = Page()
        new_page.title_entry = Entry(self.root, textvariable=new_page.title_var)
        new_page.path = str(self.page_fake_index)+'/'
        self.page_fake_index += 1

        self.pages.append(new_page)

        next_index = len(self.pages)-1
        page_button = Button(self.page_frame, command=lambda: self.page_go_to(next_index),
                             textvariable=new_page.title_var)
        self.page_buttons.append(page_button)
        page_button.grid(row=self.page_row, column=0)
        self.page_row += 1

        if self.loaded:
            self.page_go_to(len(self.pages)-1)

    def slide_prev(self):
        self.slide_go_to(self.page().slide_index.get()-1)

    def slide_next(self):
        self.slide_go_to(self.page().slide_index.get()+1)

    def slide_go_to(self, index):
        if self.slide() is not None:
            # remove previous text
            self.slide().text_text.grid_forget()

            # remove previous labels
            for label_entry in self.slide().label_entries:
                label_entry.grid_forget()
            for label_button in self.slide().label_buttons:
                label_button.grid_forget()

        # update current slide
        if self.page().slides:
            self.page().slide_index.set(max(min(index, (len(self.page().slides)-1)), 0))
        else:
            self.page().slide_index.set(max(min(index, (len(self.page().slides)-1)), -1))
        self.slide_index_text.set(self.page().slide_index_to_string())

        if self.slide() is not None:
            # load the text
            self.slide().text_text.grid(row=2, column=self.details_col, rowspan=DETAILS_TEXT_WIDTH, sticky=N)
            # reload any labels for this slide
            self.slide().label_rows = 1
            for index in range(0, len(self.slide().label_entries)):
                self.slide().label_entries[index].grid(row=self.slide().label_rows, column=self.label_cols)
                self.slide().label_buttons[index].grid(row=self.slide().label_rows, column=self.label_cols+1)
                self.slide().label_rows += 1
            # set  the threshold slider
            self.thresh_slide.set(self.slide().thresh_value)

        self.no_op()

    def page_go_to(self, index):
        if index != self.page_index:
            # purge current title
            self.page().title_entry.grid_forget()

            # dump slide images to disk
            self.dump_slides()

            # purge text/description/labels
            if self.slide() is not None:
                self.slide().text_text.grid_forget()
                for label_entry in self.slide().label_entries:
                    label_entry.grid_forget()
                for label_button in self.slide().label_buttons:
                    label_button.grid_forget()

            # update page
            self.page_index.set(max(min(index, (len(self.pages)-1)), 0))

            # load slide images from disk if they exist
            if os.path.exists(TEMP_DIR+self.page().path):
                for file_index, slide in enumerate(self.page().slides):
                    slide.image_orig = np.load(TEMP_DIR+self.page().path+IMAGE_ORIG_DUMP+'_'+str(file_index)+'.npy')
                    slide.image_cv = np.load(TEMP_DIR+self.page().path+IMAGE_CV_DUMP+'_'+str(file_index)+'.npy')
                    slide.image_render = np.load(TEMP_DIR+self.page().path+IMAGE_RENDER_DUMP+'_'+str(file_index)+'.npy')

            # load the title
            self.page().title_entry.grid(row=2, column=self.editor_col)
            # update rest of UI/load the correct slide
            self.slide_go_to(self.page().slide_index.get())
            self.current_op_label.configure(textvariable=self.page().op_current)

    def toggle_layers(self):
        self.display_layers = not self.display_layers
        self.refresh_image()

    def slide(self):
        return self.page().slide()

    def page(self):
        return self.pages[self.page_index.get()]

    def undo(self):
        self.page().undo()
        self.refresh_image()

    def redo(self):
        self.page().redo()
        self.refresh_image()

    def escape(self):
        op = self.page().op_current.get()
        if op == NO_OP:
            self.quit()
        elif op == CROP or op == ERASE or op == MOVE_LAYER:
            if len(self.page().points) > 0:
                self.page().points = []
                self.refresh_image()
            else:
                self.no_op()
        else:
            self.no_op()

    def quit(self):
        if askyesno("Confirm Quit", "Are you sure you want to quit?"):
            self.root.destroy()
            self.root.quit()
            self.master.destroy()
            self.master.quit()

    def accept(self):
        op = self.page().op_current.get()
        if op == NO_OP:
            pass
        elif op == CROP:
            self.crop()
        elif op == ERASE:
            self.erase()
        elif op == LABEL_POINT:
            self.label_point(self.label_id_selected)
        elif op == MOVE_LAYER:
            self.move_layer()

    def no_op(self):
        self.page().op_current.set(NO_OP)
        self.page().points = []
        self.refresh_image()

    def relative_point(self, point):
        # get relative co-ordinates on full image
        x = int(point[0] / self.page().scale_ratio)
        y = int(point[1] / self.page().scale_ratio)

        # if cropped, offset
        if self.page().crop_points:
            x1, y1, x2, y2 = self.page().crop_points
            x += x1
            y += y1

        return x, y

    def image_clicked(self, event):
        if self.page().op_current != NO_OP:
            point = self.relative_point((event.x, event.y))

            size = self.scale_constant(POINT_SCALE) + POINT_CLICK_PADDING
            new_point = True
            # check if spot clicked is already a point
            for index, pt in enumerate(self.page().points):
                px, py = pt
                if point[0] in range(px-size, px+size+1) and point[1] in range(py-size, py+size+1):
                    del self.page().points[index]
                    new_point = False
                    self.refresh_image()
                    break

            if new_point:
                self.add_point(point)

    def image_dragged(self, event):
        op = self.page().op_current.get()
        if op == MOVE_LAYER:
            point = self.relative_point((event.x, event.y))
            if len(self.page().points) == 1:
                self.page().points.append(point)
            else:
                self.page().points[1] = point
            self.refresh_image()

    def add_point(self, point):
        accept_point = True

        op = self.page().op_current.get()
        if op == CROP:
            if len(self.page().points) >= 2:
                self.page().points.pop()
        elif op == LABEL_POINT:
            if len(self.page().points) >= 1:
                self.page().points.pop()
        elif op == MOVE_LAYER:
            self.page().points = []
        elif op == NO_OP:
            accept_point = False

        if accept_point:
            self.page().points.append(point)
            self.refresh_image()

    def dirty_all(self):
        for slide in self.page().slides:
            slide.dirty = True

    def dirty_index(self, index):
        self.page().slides[index].dirty = True

    def crop(self):
        if self.slide() is not None:
            # stage 2 of crop
            if self.page().op_current.get() == CROP:

                # store current crop
                if self.page().crop_points:
                    prev = self.page().crop_points
                else:
                    prev = None

                if len(self.page().points) == 2:
                    xa, ya = self.page().points[0]
                    xb, yb = self.page().points[1]
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

                    self.page().crop_points = (x1, y1, x2, y2)
                    self.no_op()

                    self.page().op_history_add({HIST_OP: CROP,
                                                HIST_PREV: prev,
                                                HIST_CURRENT: self.page().crop_points})

                    self.dirty_all()

                elif len(self.page().points) == 0:
                    self.page().crop_points = None
                    self.page().op_current.set(NO_OP)

                    self.page().op_history_add({HIST_OP: CROP,
                                                HIST_PREV: prev,
                                                HIST_CURRENT: self.page().crop_points})

                    self.dirty_all()
                else:
                    print DEBUG_INVALID

            # stage 1 of crop
            elif self.page().op_current.get() == NO_OP:
                self.page().points = []
                self.page().op_current.set(CROP)
                print "please enter [0|2] points and hit [CTRL-C|Return]"

            # we have interrupted some other operation
            else:
                self.no_op()
                self.crop()

            self.refresh_image()

    def erase(self):
        if self.slide() is not None:
            if self.page().op_current.get() == ERASE:
                if len(self.page().points) > 2:
                    print "successfully erased"
                    # make a copy of the points in case we need to offset them
                    points = list(self.page().points)
                    if self.slide().offset:
                        for index, point in enumerate(points):
                            x, y = point
                            points[index] = (x-self.slide().offset[0], y-self.slide().offset[1])

                    np_points = np.array([points])
                    cv2.fillPoly(self.slide().image_cv, np_points, NO_COLOUR)
                    self.no_op()

                    self.page().op_history_add({HIST_OP: ERASE,
                                                HIST_POINTS: np_points,
                                                HIST_THRESH: self.thresh_slide.get()})

                    self.dirty_index(self.page().slide_index.get())
                elif len(self.page().points) == 0:
                    self.no_op()
                else:
                    print DEBUG_INVALID

            elif self.page().op_current.get() == NO_OP:
                self.page().points = []
                self.page().op_current.set(ERASE)
                print "please define an area and hit [CTRL-E|Return]"

            else:
                self.no_op()
                self.erase()

            self.refresh_image()

    def move_layer(self):
        if self.slide() is not None:
            if self.page().op_current.get() == MOVE_LAYER:
                x1, y1 = self.page().points[0]
                x2, y2 = self.page().points[1]
                if self.slide().offset is not None:
                    prev = self.slide().offset
                    x_prev, y_prev = self.slide().offset
                    self.slide().offset = (x_prev+(x2-x1), y_prev+(y2-y1))
                else:
                    prev = None
                    self.slide().offset = (x2-x1, y2-y1)
                self.no_op()
                self.dirty_index(self.page().slide_index.get())
                self.page().op_history_add({HIST_OP: MOVE_LAYER,
                                            HIST_PREV: prev,
                                            HIST_CURRENT: self.slide().offset})
            elif self.page().op_current.get() == NO_OP:
                if self.page().slide_index.get() > 0:
                    self.page().points = []
                    self.page().op_current.set(MOVE_LAYER)
                    print "please click and drag the layer and hit [CTRL-D|Return]"
                else:
                    print "base layer cannot be moved!"
            else:
                self.no_op()
                self.move_layer()

            self.refresh_image()

    def label(self):
        if self.slide() is not None:
            print "adding label"
            label = Entry(self.root)
            self.slide().label_entries.append(label)
            label.grid(row=self.slide().label_rows, column=self.label_cols)

            colour = "#%06x" % random.randint(0, 0xFFFFFF)

            copy = self.slide().label_id

            button = Button(self.root, command=lambda: self.label_point(copy), bg=colour, width=2, height=1)
            self.slide().label_buttons.append(button)
            button.grid(row=self.slide().label_rows, column=self.label_cols+1)

            label_data = {HIST_OP: ADD_LABEL,
                          'id': self.slide().label_id,
                          'label': label,
                          'button': button,
                          'colour': colour,
                          'point': None,
                          'grid_col': self.label_cols}

            self.slide().labels.append(label_data)
            self.page().op_history_add(label_data)

            self.slide().label_rows += 1
            self.slide().label_id += 1

    def label_point(self, label_id):
        if self.page().op_current.get() == LABEL_POINT:
            if len(self.page().points) == 1:
                label = self.get_label_by_id(label_id)
                if label:
                    if label['point']:
                        prev_point = label['point']
                    else:
                        prev_point = None
                    label['point'] = self.page().points[0]
                    self.page().op_history_add({HIST_OP: LABEL_POINT,
                                                HIST_LABEL: label,
                                                HIST_PREV: prev_point,
                                                HIST_CURRENT: self.page().points[0]})
                    self.no_op()
            elif len(self.page().points) == 0:
                self.no_op()
            else:
                print DEBUG_INVALID

            self.label_id_selected = -1

        elif self.page().op_current.get() == NO_OP:
            self.label_id_selected = label_id
            self.page().points = []
            label = self.get_label_by_id(label_id)
            if label and label['point']:
                self.add_point(label['point'])
            self.page().op_current.set(LABEL_POINT)
            print "please select a point and press [The button|Return]"
        else:
            self.label_id_selected = -1
            self.no_op()
            self.label()

        self.refresh_image()

    def get_label_by_id(self, label_id):
        for label in self.slide().labels:
            if label['id'] == label_id:
                return label
        return None

    def dump_slides(self):
        # dump slide images to disk
        if os.path.exists(TEMP_DIR+self.page().path):
            shutil.rmtree(TEMP_DIR+self.page().path)
        os.mkdir(TEMP_DIR+self.page().path)

        for file_index, slide in enumerate(self.page().slides):
            np.save(TEMP_DIR+self.page().path+IMAGE_ORIG_DUMP+'_'+str(file_index), slide.image_orig)
            np.save(TEMP_DIR+self.page().path+IMAGE_CV_DUMP+'_'+str(file_index), slide.image_cv)
            np.save(TEMP_DIR+self.page().path+IMAGE_RENDER_DUMP+'_'+str(file_index), slide.image_render)
        for slide in self.page().slides:
            slide.image_orig = None
            slide.image_cv = None
            slide.image_orig = None

    def export(self):
        print "exporting..."

        package = {'package': self.package_title_entry.get()}

        package_dir = './package'
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
            time.sleep(1)
        os.mkdir(package_dir)
        f = open(package_dir+'/data.json', 'w')

        # pages
        page_list = []
        for page_index, page in enumerate(self.pages):
            page_dir = package_dir+'/'+str(page_index)
            os.mkdir(page_dir)
            page_dump = {'title': page.title_entry.get()}

            # slides
            slide_list = []
            for slide_index, slide in enumerate(page.slides):
                # load render dump if needed
                loaded = False
                if slide.image_render is None:
                    slide.image_render = np.load(TEMP_DIR+page.path+IMAGE_RENDER_DUMP+'_'+str(slide_index)+'.npy')
                    loaded = True
                # then save image
                slide_loc = page_dir+'/'+str(slide_index)
                cv2.imwrite(slide_loc+'.png', cv2.cvtColor(slide.image_render, cv2.COLOR_RGBA2BGRA))
                if loaded:
                    slide.image_render = None

                # text
                slide_dump = {'text': slide.text_text.get(1.0, END).strip()}
                # labels
                label_list = []
                if page.crop_points:
                    x1, y1, x2, y2 = page.crop_points
                else:
                    loaded = False
                    if slide.image_cv is None:
                        slide.image_cv = np.load(TEMP_DIR+page.path+IMAGE_CV_DUMP+'_'+str(slide_index)+'.npy')
                        loaded = True
                    shape = slide.image_cv.shape
                    if loaded:
                        slide.image_cv = None
                    x1 = 0
                    y1 = 0
                    x2 = shape[1]
                    y2 = shape[0]
                for label in slide.labels:
                    if label['point']:
                        x_pct = ((label['point'][0] - x1) / float(x2 - x1)) * 100
                        y_pct = ((label['point'][1] - y1) / float(y2 - y1)) * 100
                        label_list.append({'xPos': x_pct,
                                           'yPos': y_pct,
                                           'text': label['label'].get()})
                slide_dump['labels'] = label_list
                slide_list.append(slide_dump)

            page_dump['slides'] = slide_list
            page_list.append(page_dump)

        package['pages'] = page_list

        json.dump(package, f)
        f.close()
        print "export complete"

    def save(self):
        # TODO: want to be able to save/reload half-complete edits
        pass

    def run(self):
        try:
            self.master.mainloop()
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

            new_slide = Slide()
            new_slide.image_orig = cv2.imread(name)
            new_slide.image_cv = thresh_image(new_slide.image_orig, self.thresh_slide.get())

            new_slide.text_text = Text(self.root, height=DETAILS_TEXT_WIDTH, width=40)

            self.page().slides.append(new_slide)

            self.slide_go_to(len(self.page().slides)-1)

    def reset_all(self):
        self.page().points = []
        self.page().crop_points = None

    def thresh_slide_update(self, val):
        if self.running:
            self.slide().thresh_value = self.thresh_slide.get()
            self.slide().image_cv = thresh_image(self.slide().image_orig, self.slide().thresh_value)
            self.dirty_index(self.page().slide_index.get())
            self.refresh_image()
        else:
            self.running = True

    def render_temp_offset(self, image):
        x1, y1 = self.page().points[0]
        x2, y2 = self.page().points[1]
        tx = x2-x1
        ty = y2-y1

        rows = image.shape[0]
        cols = image.shape[1]

        translate = np.float32([[1, 0, tx], [0, 1, ty]])

        return cv2.warpAffine(image, translate, (cols, rows))

    def refresh_image(self):
        if self.loaded:
            if len(self.page().slides) > 0:
                op = self.page().op_current.get()

                if self.display_layers:
                    self.page().slides[0].render(self.page().crop_points)
                    base = np.copy(self.page().slides[0].image_render)

                    images = [base]
                    for index, slide in enumerate(self.page().slides):
                        if index != 0:
                            slide.render(self.page().crop_points)
                            if op == MOVE_LAYER and len(self.page().points) == 2 \
                                    and index == self.page().slide_index.get():
                                temp = np.copy(slide.image_render)
                                temp = self.render_temp_offset(temp)

                                images.append(temp)
                            else:
                                images.append(np.copy(slide.image_render))

                    final_image = stack_images(images)
                else:
                    self.page().slides[self.page().slide_index.get()].render(self.page().crop_points)
                    temp = np.copy(self.page().slides[self.page().slide_index.get()].image_render)
                    if op == MOVE_LAYER and len(self.page().points) == 2:
                        final_image = self.render_temp_offset(temp)
                    else:
                        final_image = temp

                x_offset = 0
                y_offset = 0

                if self.page().crop_points:
                    x1, y1, x2, y2 = self.page().crop_points
                    x_offset = x1
                    y_offset = y1

                self.page().scale_ratio = calc_scale_ratio(IMAGE_WIDTH, final_image.shape)

                # draw anything else on top of the base image
                # scale to match crop area
                size = self.scale_constant(POINT_SCALE)
                thickness = self.scale_constant(POINT_LINE_WIDTH)

                # draw crosses to show points
                if op == NO_OP or op == MOVE_LAYER:
                    pass
                else:
                    for p_x, p_y in self.page().points:
                        # point offset due to cropping
                        r_x = p_x-x_offset
                        r_y = p_y-y_offset

                        cv2.line(final_image, (r_x-size, r_y-size), (r_x+size, r_y+size), POINT_COLOUR, thickness)
                        cv2.line(final_image, (r_x-size, r_y+size), (r_x+size, r_y-size), POINT_COLOUR, thickness)

                # draw indicators for any labels
                for label in self.slide().labels:
                    if label['point'] and label['id'] != self.label_id_selected:
                        px, py = label['point']
                        rx = px-x_offset
                        ry = py-y_offset

                        colour = hex_to_rgba(label['colour'])

                        cv2.line(final_image, (rx-size, ry-size), (rx+size, ry+size), colour, thickness)
                        cv2.line(final_image, (rx-size, ry+size), (rx+size, ry-size), colour, thickness)

                # depending on current operation, draw other stuff
                if op == CROP:
                    if len(self.page().points) == 2:
                        x1, y1 = self.page().points[0]
                        x2, y2 = self.page().points[1]
                        x1 -= x_offset
                        x2 -= x_offset
                        y1 -= y_offset
                        y2 -= y_offset

                        thickness = self.scale_constant(LINE_WIDTH)
                        cv2.line(final_image, (x1, y1), (x2, y1), LINE_COLOUR, thickness)
                        cv2.line(final_image, (x2, y1), (x2, y2), LINE_COLOUR, thickness)
                        cv2.line(final_image, (x2, y2), (x1, y2), LINE_COLOUR, thickness)
                        cv2.line(final_image, (x1, y2), (x1, y1), LINE_COLOUR, thickness)
                elif op == ERASE:
                    if len(self.page().points) > 2:
                        if self.page().crop_points:
                            x1, y1, x2, y2 = self.page().crop_points
                            adjusted = []
                            for a, b in self.page().points:
                                adjusted.append((a-x1, b-y1))
                            np_points = np.array([adjusted])
                        else:
                            np_points = np.array([self.page().points])
                        cv2.fillPoly(final_image, np_points, LINE_COLOUR)

                # scale
                display = cv2.resize(final_image, (0, 0), fx=self.page().scale_ratio, fy=self.page().scale_ratio)

                # display image
                img = Image.fromarray(display)
                self.image_tk = ImageTk.PhotoImage(image=img, master=self.root)
                self.image_frame.configure(image=self.image_tk)
            else:
                self.image_tk = blank_image(self.root)
                self.image_frame.configure(image=self.image_tk)

    def scale_constant(self, constant):
        return int(constant/self.page().scale_ratio)


if __name__ == '__main__':
    master = Gui()
    master.run()
