"""
Authors:
Ido Betesh 307833822
Guy Sharir 310010244
Opal Peltzman 208521385
"""

import re
import numpy as np
from tkinter import *
from tkinter import filedialog
import math

class myWindowApp():
    """
    initialize all app varibles
            """

    def __init__(self):
        self.menu = 0
        self.window = 0
        self.canvas = 0
        self.img = 0
        self.size = 700

        # container for help information
        self.help = 0
        self.messages = 0

        # control points from inserting file
        self.circles = []
        self.lines = []
        self.curves = []

        # transformations variables
        self.tollbar = 0
        self.flag = 0
        self.x_entry = 0
        self.y_entry = 0
        self.scaling_value = 0
        self.move_x = 0
        self.move_y = 0
        self.rotation = 0
        self.axis = 0

        # default color for pixel (black in hex)
        self.color = "#041412"

        # start function
        self.initWindow()

    """
       clean_canvas(self):
       fix all negative positions to be inside the frame
       considering all other dots as well.
            """

    def bring_to_view(self):
        min_x = 0
        min_y = 0

        for line in self.lines:
            for i in range(0, len(line)):
                if i % 2 == 0:  # x values
                    min_x = min(line[i], min_x)

                if i % 2 == 1:  # x values
                    min_y = min(line[i], min_y)

        for curve in self.curves:
            for i in range(0, len(curve)):
                if i % 2 == 0:  # x values
                    min_x = min(curve[i], min_x)

                if i % 2 == 1:  # x values
                    min_y = min(curve[i], min_y)

        for circle in self.circles:
            min_x = min(circle[0], min_x)
            min_y = min(circle[1], min_y)

        for line in self.lines:
            for i in range(0, len(line)):
                if i % 2 == 0:  # x values
                    line[i] -= min_x

                if i % 2 == 1:  # y values
                    line[i] -= min_y

        for curve in self.curves:
            for i in range(0, len(curve)):
                if i % 2 == 0:  # x values
                    curve[i] -= min_x

                if i % 2 == 1:  # x values
                    curve[i] -= min_y

        for circle in self.circles:
            circle[0] -= min_x
            circle[1] -= min_y

    """
        clean_canvas(self):
        clean all drawing from canvas window
            """
    def clean_canvas(self):
        if self.canvas != 0:
            self.canvas.delete("all")
            self.messages.config(text="All clean! Let's start again")
            # Adding img
            self.img = PhotoImage(width=self.size, height=self.size)
            self.canvas.create_image(
                (self.size // 2, self.size // 2), image=self.img, state="normal")

    """
        browseFiles(self):
        open the file explorer window to brows file.
            """
    def browseFiles(self):
        # check if canvas window  is closed
        if self.canvas == 0:
            self.messages.config(
                text="please open canvas first! using Open canvas button")
        else:
            filename = filedialog.askopenfilename(initialdir="/",
                                                  title="Select a File",
                                                  filetypes=(("Text files",
                                                              "*.txt*"),
                                                             ("all files",
                                                              "*.*")))
            self.getObjects(filename)

    """
        getObjects(self, fileName):
        open file and reads all control points.
            """
    def getObjects(self, fileName):
        self.circles = []
        self.lines = []
        self.curves = []
        if fileName:
            with open(fileName) as f:
                for row in f:
                    # find all points from source file
                    points = re.findall(r'\d+[.]+\d|\d+', row)
                    points = list(map(float, points))
                    new = points

                    pointsLen = len(new)
                    if pointsLen == 3:
                        self.circles.append(new)
                    if pointsLen == 4:
                        self.lines.append(new)
                    if pointsLen == 8:
                        self.curves.append(new)

        self.normalize_file_input()
        self.draw_file(self.lines, self.circles, self.curves)

    """
        normalize_file_input(self):
        normalize the word coordinates to our
        canvas coordinates.
            """

    def normalize_file_input(self):
        maxWidth = 1
        maxHight = 1

        for line in self.lines:
            for i in range(0, len(line)):
                if i % 2 == 0:  # x values
                    maxWidth = max(line[i], maxWidth)

                if i % 2 == 1:  # y values
                    maxHight = max(line[i], maxHight)

        for curve in self.curves:
            for i in range(0, len(curve)):
                if i % 2 == 0:  # x values
                    maxWidth = max(curve[i], maxWidth)

                if i % 2 == 1:  # y values
                    maxHight = max(curve[i], maxHight)

        for circle in self.circles:
            maxWidth = max(circle[0], maxWidth)
            maxHight = max(circle[1], maxHight)

        n_lines = []
        n_circles = []
        n_curves = []

        maxWidth += maxWidth
        maxHight += maxHight

        for line in self.lines:
            tmp = []
            for i in range(0, len(line)):
                if i % 2 == 0:  # x values
                    tmp.append(line[i] / maxWidth * self.size)
                if i % 2 == 1:  # y values
                    tmp.append((line[i] / maxHight * self.size))

            n_lines.append(tmp)

        for curve in self.curves:
            tmp = []
            for i in range(0, len(curve)):
                if i % 2 == 0:  # x values
                    tmp.append(curve[i] / maxWidth * self.size)
                if i % 2 == 1:  # y values
                    tmp.append((curve[i] / maxHight * self.size))

                n_curves.append(tmp)

        for circle in self.circles:
            n_circles.append([circle[0] / maxWidth * self.size,
                              (circle[1] / maxHight * self.size),
                              circle[2] / maxHight * self.size])

        self.lines = n_lines
        self.curves = n_curves
        self.circles = n_circles

    """
        draw_file(self, lines, circles, curves):
        draw all lines according to the file's information
            """

    def draw_file(self, lines, circles, curves):

        for line in lines:
            self.canvas.create_line(line[0], line[1], line[2], line[3])

        for circle in circles:
            self.create_circle(circle[0], circle[1], circle[2])

        for curve in curves:
            self.draw_curve(curve[0], curve[1], curve[2],
                            curve[3], curve[4], curve[5], curve[6], curve[7])

    """
        transformation_help(self):
        change text information to information about transactions.            
        """

    def transformation_help(self):
        self.help.delete('1.0', END)
        info = """In order to display your coordinates file\nmake sure it follows these rules:\n- Line has to be formatted as (x1, y1, x2, y2)\n- Circle has to be formatted as (x, y, radius)\n- Curve has to be formatted as (x1, y1, x2, y2, x3, y3, x4, y4).\n"""
        self.help.insert(END, info)

    """
        file_help(self):
        change text information to information about file.
            """

    def file_help(self):
        self.help.delete('1.0', END)
        info = """You should upload TXT file that contains your structure.\nIn the file, the structure should be divided to control points for\ncurves, circles and lines.\nFor the points structures please go to Transactions Help.\n"""
        self.help.insert(END, info)

    """
        destroy_transaction_widget(self):
        deletes all widgets relevant to specific transaction.
            """

    def destroy_transaction_widget(self):
        if self.tollbar != 0:
            self.tollbar.destroy()

    """
        get_user_inputs(self):
        get user inputs according to the transaction
        and call the correct transformation function.
            """

    def get_user_inputs(self):
        # {0:scaling, 1:rotation, 2:translation, 3:mirror, 4:shearing}
        if self.flag == 0:
            self.scaling_value = 0
            if self.x_entry.get() and self.y_entry.get():
                self.scaling_value = float(self.x_entry.get())
                self.axis = str(self.y_entry.get())
                self.scalling_transformation()
            else:
                self.messages.config(
                    text="please enter the correct values!")
        elif self.flag == 1:
            self.move_x = self.move_y = 0
            if self.x_entry.get():
                self.move_x = float(self.x_entry.get())
            if self.y_entry.get():
                self.move_y = float(self.y_entry.get())
            self.translation()
        elif self.flag == 2:
            self.rotation = 0
            if self.x_entry.get():
                self.rotation = float(self.x_entry.get())
            self.rotate()
        elif self.flag == 3:
            if self.x_entry.get():
                self.axis = str(self.x_entry.get())
                self.mirror_transformation()
            else:
                self.messages.config(
                    text="please enter axis!")
        elif self.flag == 4:
            self.move_x = 0
            if self.x_entry.get():
                self.axis = str(self.x_entry.get())
                if self.y_entry.get():
                    self.move_x = float(self.y_entry.get())
                self.shearing()
            else:
                self.messages.config(
                    text="please enter axis!")

    """
        draw_curve(self, x1, y1, x2, y2, x3, y3, x4, y4):
        draws curve given 4 points based on
        Bezier algorithm for drawing curve
            """

    def draw_curve(self, x1, y1, x2, y2, x3, y3, x4, y4):

        linesInCurve = 1000
        dt = 1 / linesInCurve

        ax, ay = -x1 + 3 * x2 - 3 * x3 + x4, -y1 + 3 * y2 - 3 * y3 + y4
        bx, by = 3 * x1 - 6 * x2 + 3 * x3, 3 * y1 - 6 * y2 + 3 * y3
        cx, cy = -3 * x1 + 3 * x2, -3 * y1 + 3 * y2
        dx, dy = x1, y1

        while dt < 1.0:  # go until reaches linesInCurve value
            xt = int(ax * dt ** 3 + bx * dt ** 2 + cx * dt + dx)
            yt = int(ay * dt ** 3 + by * dt ** 2 + cy * dt + dy)
            self.canvas.create_line(x1, y1, xt, yt)
            x1, y1 = xt, yt
            dt += 1 / linesInCurve
        self.canvas.create_line(xt, yt, x4, y4)

    """
        create_circle(self, t, y, r): using the tkinter core function create_oval draws circle by x,y and radius
            """

    def create_circle(self, t, y, r):  # center coordinates, radius
        x0 = t - r
        y0 = y - r
        x1 = t + r
        y1 = y + r
        self.canvas.create_oval(x0, y0, x1, y1)

    #################################
    #######  transformations  #######
    #################################
    """
        scaling_input(self):
        get scaling value from user
            """
    def scalling_input(self):
        self.flag = 0
        # Create toolbar menu for user inputs
        self.destroy_transaction_widget()
        self.tollbar = Frame(self.menu)
        self.tollbar.pack(fill=X)
        x_value = Label(self.tollbar, text="enter scaling value: ")
        x_value.pack(side=LEFT, padx=2, pady=2)
        self.x_entry = Entry(self.tollbar)
        self.x_entry.pack(side=LEFT, padx=2, pady=2)
        y_value = Label(self.tollbar, text="enter up/down: ")
        y_value.pack(side=LEFT, padx=2, pady=2)
        self.y_entry = Entry(self.tollbar)
        self.y_entry.pack(side=LEFT, padx=2, pady=2)

        send = Button(
            self.tollbar,
            relief=FLAT,
            compound=LEFT,
            text="SEND",
            activebackground='pink',
            command=self.get_user_inputs
        )
        send.pack(side=LEFT, padx=2, pady=2)

    """
        Transformations -
        1.scaling_transformation(self):
            given a value, the function will resize the object acording to the input
    """
    def scalling_transformation(self):
        if self.axis == "down" or self.axis == "up" and self.scaling_value != 0:
            # clean canvas before translations
            self.clean_canvas()

            s_lines = []
            s_circles = []
            s_curves = []

            for line in self.lines:
                if self.axis == "up":
                    s_lines.append([x * self.scaling_value for x in line])
                if self.axis == "down":
                    s_lines.append([x / self.scaling_value for x in line])
            for circle in self.circles:
                if self.axis == "up":
                    s_circles.append([x * self.scaling_value for x in circle])
                if self.axis == "down":
                    s_circles.append([x / self.scaling_value for x in circle])
            for curve in self.curves:
                if self.axis == "up":
                    s_curves.append([x * self.scaling_value for x in curve])
                if self.axis == "down":
                    s_curves.append([x / self.scaling_value for x in curve])

            self.lines = s_lines
            self.circles = s_circles
            self.curves = s_curves

            self.draw_file(s_lines, s_circles, s_curves)
        else:
            if self.scaling_value == 0:
                self.messages.config(
                    text="can't get zero! please change value")
            self.messages.config(
                text="wrong scale value! please change to up/down")

    """
        translation_input(self):
        get translation( x and y ) value from user
            """
    def translation_input(self):
        self.flag = 1
        # Create toolbar menu for user inputs
        self.destroy_transaction_widget()
        self.tollbar = Frame(self.menu)
        self.tollbar.pack(fill=X)
        x_value = Label(self.tollbar, text="enter X value")
        x_value.pack(side=LEFT, padx=2, pady=2)
        self.x_entry = Entry(self.tollbar)
        self.x_entry.pack(side=LEFT, padx=2, pady=2)
        y_value = Label(self.tollbar, text="enter Y value")
        y_value.pack(side=LEFT, padx=2, pady=2)
        self.y_entry = Entry(self.tollbar)
        self.y_entry.pack(side=LEFT, padx=2, pady=2)
        send = Button(
            self.tollbar,
            relief=FLAT,
            compound=LEFT,
            text="SEND",
            activebackground='pink',
            command=self.get_user_inputs
        )
        send.pack(side=LEFT, padx=2, pady=2)

    """
        Transformations -
        2.translation(self):
            given x and y values, move the object according to input on the x,y pane
            """
    def translation(self):
        # clean canvas before translations
        self.clean_canvas()
        s_lines = []
        s_circles = []
        s_curves = []

        for line in self.lines:
            s_lines.append([line[0] + self.move_x, line[1] + self.move_y,
                            line[2] + self.move_x, line[3] + self.move_y])

        for circle in self.circles:
            s_circles.append(
                [circle[0] + self.move_x, circle[1] + self.move_y, circle[2]])

        for curve in self.curves:
            tmp = []
            i = 0
            for x in curve:
                tmp.append(x + self.move_x if i % 2 == 0 else x + self.move_y)
                i += 1

            s_curves.append(tmp)

        self.lines = s_lines
        self.circles = s_circles
        self.curves = s_curves

        self.draw_file(self.lines, self.circles, self.curves)

    """
        rotate_input(self):
        get angle value from user
            """

    def rotate_input(self):
        self.flag = 2
        # Create toolbar menu for user inputs
        self.destroy_transaction_widget()
        self.tollbar = Frame(self.menu)
        self.tollbar.pack(fill=X)
        x_value = Label(self.tollbar, text="enter rotation value")
        x_value.pack(side=LEFT, padx=2, pady=2)
        self.x_entry = Entry(self.tollbar)
        self.x_entry.pack(side=LEFT, padx=2, pady=2)

        send = Button(
            self.tollbar,
            relief=FLAT,
            compound=LEFT,
            text="SEND",
            activebackground='pink',
            command=self.get_user_inputs
        )
        send.pack(side=LEFT, padx=2, pady=2)

    """
        change_coordinates(self, x, y):
        helper function to rotate the object.
        switches from cartesian to polar coordinates
                """
    def change_coordinates(self, x, y):
        r = math.sqrt(pow(x, 2) + pow(y, 2))
        phi = math.atan2(y, x) * 180 / math.pi
        phi = phi / 180 * math.pi

        return r * math.cos(phi), r * math.sin(phi)

    """
        Transformations -
        3.rotate(self):
        this transformation rotates the object around the (0,0) point.
            """
    def rotate(self):
        # clean canvas before translations
        self.clean_canvas()

        # set the value of needed rotation in degrees
        sinus = math.sin(self.rotation / 180 * math.pi)
        cosinus = math.cos(self.rotation / 180 * math.pi)

        s_lines = []
        s_curves = []
        s_circles = []

        # transform all lines
        for line in self.lines:
            x1 = line[0]
            y1 = line[1]
            x2 = line[2]
            y2 = line[3]

            # convert cartesian to polar
            g_x1, g_y1 = self.change_coordinates(x1, y1)
            g_x2, g_y2 = self.change_coordinates(x2, y2)

            # save converted lines
            s_lines.append([g_x1 * cosinus - g_y1 * sinus, g_y1 * cosinus + g_x1 *
                            sinus, g_x2 * cosinus - g_y2 * sinus, g_y2 * cosinus + g_x2 * sinus])

        # transform all curves
        for curve in self.curves:
            x1 = curve[0]
            y1 = curve[1]
            x2 = curve[2]
            y2 = curve[3]
            x3 = curve[4]
            y3 = curve[5]
            x4 = curve[6]
            y4 = curve[7]

            # convert cartesian to polar
            g_x1, g_y1 = self.change_coordinates(x1, y1)
            g_x2, g_y2 = self.change_coordinates(x2, y2)
            g_x3, g_y3 = self.change_coordinates(x3, y3)
            g_x4, g_y4 = self.change_coordinates(x4, y4)

            # save converted curves
            s_curves.append([
                g_x1 * cosinus - g_y1 * sinus,
                g_x1 * sinus + g_y1 * cosinus,
                g_x2 * cosinus - g_y2 * sinus,
                g_x2 * sinus + g_y2 * cosinus,
                g_x3 * cosinus - g_y3 * sinus,
                g_x3 * sinus + g_y3 * cosinus,
                g_x4 * cosinus - g_y4 * sinus,
                g_x4 * sinus + g_y4 * cosinus
            ])

        # transform all circles
        for circle in self.circles:
            x = circle[0]
            y = circle[1]

            # convert cartesian to polar
            g_x, g_y = self.change_coordinates(x, y)

            # save converted circles
            s_circles.append([g_x * cosinus - g_y * sinus,
                              g_x * sinus + g_y * cosinus, circle[2]])

        # save new positions for consistence
        self.lines = s_lines
        self.circles = s_circles
        self.curves = s_curves

        # bring object in to view if needed
        self.bring_to_view()

        # draw shape
        self.draw_file(self.lines, self.circles, self.curves)

    """
        mirror_input(self):
        get axis from user
            """

    def mirror_input(self):
        self.flag = 3
        # Create toolbar menu for user inputs
        self.destroy_transaction_widget()
        self.tollbar = Frame(self.menu)
        self.tollbar.pack(fill=X)
        x_value = Label(self.tollbar, text="enter axis: X/Y")
        x_value.pack(side=LEFT, padx=2, pady=2)
        self.x_entry = Entry(self.tollbar)
        self.x_entry.pack(side=LEFT, padx=2, pady=2)

        send = Button(
            self.tollbar,
            relief=FLAT,
            compound=LEFT,
            text="SEND",
            activebackground='pink',
            command=self.get_user_inputs
        )
        send.pack(side=LEFT, padx=2, pady=2)

    """
        Transformations -
        4.mirror_transformation(self):
        according to axis x/y multiply the opposite axis with -1
            """
    def mirror_transformation(self):
        # clean canvas before translations
        self.clean_canvas()
        s_lines = []
        s_circles = []
        s_curves = []

        if self.axis == 'X' or self.axis == 'x':
            for line in self.lines:
                s_lines.append([line[0], line[1] * -1, line[2],
                                line[3] * -1])

            for circle in self.circles:
                s_circles.append([circle[0], circle[1] * -1, circle[2]])

            for curve in self.curves:
                s_curves.append([curve[0], curve[1] * -1, curve[2], curve[3] * -1, curve[4], curve[5] * -1, curve[6],
                                 curve[7] * -1])

        elif self.axis == 'Y' or self.axis == 'y':
            for line in self.lines:
                s_lines.append([line[0] * -1, line[1], line[2] * -1,
                                line[3]])

            for circle in self.circles:
                s_circles.append([circle[0] * -1, circle[1], circle[2]])

            for curve in self.curves:
                s_curves.append(
                    [curve[0] * -1, curve[1], curve[2] * -1, curve[3], curve[4] * -1, curve[5], curve[6] * -1,
                     curve[7]])

        self.lines = s_lines
        self.circles = s_circles
        self.curves = s_curves

        self.bring_to_view()
        self.draw_file(self.lines, self.circles, self.curves)

    """
        shearing_input(self):
        get shearing value and axis from user.
            """

    def shearing_input(self):
        self.flag = 4
        # Create toolbar menu for user inputs
        self.destroy_transaction_widget()
        self.tollbar = Frame(self.menu)
        self.tollbar.pack(fill=X)
        x_value = Label(self.tollbar, text="enter axis: X/Y")
        x_value.pack(side=LEFT, padx=2, pady=2)
        self.x_entry = Entry(self.tollbar)
        self.x_entry.pack(side=LEFT, padx=2, pady=2)
        y_value = Label(self.tollbar, text="enter shearing value")
        y_value.pack(side=LEFT, padx=2, pady=2)
        self.y_entry = Entry(self.tollbar)
        self.y_entry.pack(side=LEFT, padx=2, pady=2)
        send = Button(
            self.tollbar,
            relief=FLAT,
            compound=LEFT,
            text="SEND",
            activebackground='pink',
            command=self.get_user_inputs
        )
        send.pack(side=LEFT, padx=2, pady=2)

    """
        shearing(self):
        given axis and value -> shear the image by the given value according to x:y ratio and max width/height        
            """
    def shearing(self):
        # clean canvas before translations
        self.clean_canvas()

        sh_lines = []
        sh_circles = []
        sh_curves = []

        val = self.move_x

        maxWidth = 1
        maxHight = 1

        for line in self.lines:
            for i in range(0, len(line)):
                if i % 2 == 0:  # x values
                    maxWidth = max(line[i], maxWidth)

                if i % 2 == 1:  # y values
                    maxHight = max(line[i], maxHight)

        for curve in self.curves:
            for i in range(0, len(curve)):
                if i % 2 == 0:  # x values
                    maxWidth = max(curve[i], maxWidth)

                if i % 2 == 1:  # y values
                    maxHight = max(curve[i], maxHight)

        for circle in self.circles:
            maxWidth = max(circle[0], maxWidth)
            maxHight = max(circle[1], maxHight)

        for line in self.lines:
            if self.axis == 'x' or self.axis == 'X':
                tmp_line = ([line[0] + line[1] / maxHight * val, line[1], line[2] + line[3] / maxHight * val, line[3]])
            else:
                tmp_line = ([line[0], line[1] + line[0] / maxWidth * val, line[2], line[3] + line[2] / maxWidth * val])
            sh_lines.append(tmp_line)

        for circle in self.circles:
            if self.axis == 'x' or self.axis == 'X':
                tmp_circle = ([circle[0] + circle[1] / maxHight * val, circle[1], circle[2]])
            else:
                tmp_circle = ([circle[0], circle[1] + circle[0] / maxWidth * val, circle[2]])
            sh_circles.append(tmp_circle)

        for curve in self.curves:
            if self.axis == 'x' or self.axis == 'X':
                tmp_curve = (
                [curve[0] + curve[1] / maxHight * val, curve[1], curve[2] + curve[3] / maxHight * val, curve[3],
                 curve[4] + curve[5] / maxHight * val, curve[5], curve[6] + curve[7] / maxHight * val, curve[7]])
            else:
                tmp_curve = (
                [curve[0], curve[1] + curve[0] / maxWidth * val, curve[2], curve[3] + curve[2] / maxWidth * val,
                 curve[4], curve[5] + curve[4] / maxWidth * val, curve[6], curve[7] + curve[6] / maxWidth * val])
            sh_curves.append(tmp_curve)

        self.lines = sh_lines
        self.circles = sh_circles
        self.curves = sh_curves

        self.draw_file(self.lines, self.circles, self.curves)

    #################################
    #######        GUI        #######
    #################################

    def on_closing(self):
        self.window.destroy()
        self.window = 0
        self.canvas = 0

    """
        open_canvas(self):
        open another window to show drawing on canvas.
            """

    def open_canvas(self):
        if self.window == 0:
            self.window = Toplevel(master=self.menu)
            # Set bar Title
            self.window.title('CANVAS')
            # Set fixed dimensions to window
            self.window.geometry("700x700")
            # Adding canvas to the window
            self.canvas = Canvas(self.window, width=self.size,
                                 height=self.size, background='white')
            self.canvas.pack(fill=X)
            # Adding img
            self.img = PhotoImage(width=self.size, height=self.size)
            self.canvas.create_image(
                (self.size // 2, self.size // 2), image=self.img, state="normal")

            if self.window != 0:
                self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        else:
            self.messages.config(
                text="canvas window is already open")

    """
        initWindow(): creates the application menu.
        creating window with Python GUI Tkinter
            """

    def initWindow(self):
        self.menu = Tk()
        self.menu.title("menu")
        self.menu.geometry("600x400")

        # add massage box to contact with the user
        self.messages = Label(self.menu, bg='pink', text=" Lets start! Please choose you're transformation ", anchor='w')
        self.messages.pack(fill=X, side=BOTTOM)

        # main menu
        menubar = Menu(self.menu)
        # add file upload option
        file_menu = Menu(menubar)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Browse File", command=self.browseFiles)
        file_menu.add_separator()
        file_menu.add_command(label="File Help", command=self.file_help)

        # add open canvas button
        menubar.add_command(label="Open canvas", command=self.open_canvas)

        # add transformations options to menu
        transform_menu = Menu(menubar)
        menubar.add_cascade(label="Transformations", menu=transform_menu)
        transform_menu.add_command(
            label="Scaling", command=self.scalling_input)
        transform_menu.add_separator()
        transform_menu.add_command(label="Rotation", command=self.rotate_input)
        transform_menu.add_separator()
        transform_menu.add_command(
            label="Translation", command=self.translation_input)
        transform_menu.add_separator()
        transform_menu.add_command(label="Mirror", command=self.mirror_input)
        transform_menu.add_separator()
        transform_menu.add_command(
            label="Shearing", command=self.shearing_input)
        transform_menu.add_separator()
        transform_menu.add_command(
            label="Transformations Help", command=self.transformation_help)

        menubar.add_command(label="Clean canvas", command=self.clean_canvas)
        menubar.add_command(label="Exit", command=self.menu.destroy)
        self.menu.config(menu=menubar)

        # Create label for help information
        label = Label(self.menu, text="HELP")
        label.config(font=("Courier", 11))
        # create text widget
        self.help = Text(self.menu, height=20, width=70, wrap="none")
        # Insert text
        info = """For HELP information please choose File Help or Transformations Help.\n"""
        label.pack()
        self.help.pack()
        self.help.insert(END, info)
        # window.mainloop(), enables Tkinter listen to events in the menu window
        self.menu.mainloop()

"""
run app
"""
def main():
    myWindowApp()

if __name__ == '__main__':
    main()
