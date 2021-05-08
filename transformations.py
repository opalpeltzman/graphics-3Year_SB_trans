"""
Authors:
Ido Betesh 307833822
Guy Sharir 310010244
Opal Peltzman 208521385
"""

import re
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
import math

"""
App class
"""


class myWindowApp():

    def __init__(self):
        self.menu = 0
        self.window = 0
        self.canvas = 0
        self.img = 0

        # container for help information
        self.help = 0
        self.messages = 0

        # control dots from inserting file
        self.circles = []
        self.lines = []
        self.curves = []

        # transformations variables
        self.tollbar = 0
        self.flag = 0   # {0:scaling, 1:rotation, 2:translation}
        self.x_entry = 0
        self.y_entry = 0

        self.scaling_value = 0

        self.move_x = 0
        self.move_y = 0

        self.rotation = 0

        # colors
        # default color for pixel (black in hex)
        self.color = "#041412"

        # start function
        self.initWindow()

    """
       clean_canvas(self):
       deletes all drawing from canvas.
            """

    def clean_canvas(self):
        if self.canvas != 0:
            print("here")
            self.canvas.delete("all")
            print("clean canvas")
            self.messages.config(text="All clean! Let's start again")
            # Adding img
            self.img = PhotoImage(width=1000, height=500)
            self.canvas.create_image(
                (1000 // 2, 500 // 2), image=self.img, state="normal")

    # ############################################## files ############################################################
    """
        browseFiles(self):
        open the file explorer window.
            """

    def browseFiles(self):
        # window with canvas is closed
        if self.canvas == 0:
            self.messages.config(
                text="please open canvas first! using Open canvas button")
        else:
            print(self.canvas)
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
        if fileName:
            with open(fileName) as f:
                for row in f:
                    points = re.findall(r'\d+[.]+\d|\d+', row)
                    points = np.array(points)

                    points = list(map(float, points))
                    new = [int(x * 10) for x in points]

                    pointsLen = len(new)
                    if pointsLen == 3:
                        self.circles.append(new)
                    if pointsLen == 4:
                        self.lines.append(new)
                    if pointsLen == 8:
                        self.curves.append(new)

        self.draw_file(self.lines, self.circles, self.curves)

    """
        draw_file(self, lines, circles, curves):

            """

    def draw_file(self, lines, circles, curves):

        for line in lines:
            self.canvas.create_line(line[0], line[1], line[2], line[3])

        for circle in circles:
            self.create_circle(circle[0], circle[1], circle[2])

        for curve in curves:
            self.draw_curve(curve[0], curve[1], curve[2],
                            curve[3], curve[4], curve[5], curve[6], curve[7])

    # ############################################## help ############################################################
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
        get user inputs and call the correct transformations.
            """

    def get_user_inputs(self):
        # {0:scaling, 1:rotation, 2:translation}
        if self.flag == 0:
            self.scaling_value = float(self.x_entry.get())
            self.scalling_transformation()
        elif self.flag == 1:
            self.move_x = float(self.x_entry.get())
            self.move_y = float(self.y_entry.get())
            self.translation()
        elif self.flag == 2:
            self.rotation = float(self.x_entry.get())
            self.rotate()
        elif self.flag == 3:
            pass
        elif self.flag == 4:
            pass

    # ############################################## shapes ##########################################################
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
        create_circle(self, t, y, r):
            """

    def create_circle(self, t, y, r):  # center coordinates, radius
        x0 = t - r
        y0 = y - r
        x1 = t + r
        y1 = y + r
        self.canvas.create_oval(x0, y0, x1, y1)

    # ############################################ transformations ###################################################
    # ############################################ scaling ###########################################################
    """
        scalling_input(self):
        get scaling value from user
            """

    def scalling_input(self):
        self.flag = 0
        # Create toolbar menu for user inputs
        self.destroy_transaction_widget()
        self.tollbar = Frame(self.menu)
        self.tollbar.pack(fill=X)
        x_value = Label(self.tollbar, text="enter X value")
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
        1.scalling_transformation(self):

            """

    def scalling_transformation(self):

        s_lines = []
        s_circles = []
        s_curves = []

        for line in self.lines:
            s_lines.append([x * self.scaling_value for x in line])

        for circle in self.circles:
            s_circles.append([x * self.scaling_value for x in circle])

        for curve in self.curves:
            s_curves.append([x * self.scaling_value for x in curve])

        self.draw_file(s_lines, s_circles, s_curves)

    # ############################################ translation ######################################################
    """
        translation_input(self):
        get translation value from user
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
            """

    def translation(self):
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

        self.draw_file(s_lines, s_circles, s_curves)

    # ############################################ rotate ###########################################################
    """
            scalling_input(self):
            get scaling value from user
                """

    def rotate_input(self):
        self.flag = 2
        # Create toolbar menu for user inputs
        self.destroy_transaction_widget()
        self.tollbar = Frame(self.menu)
        self.tollbar.pack(fill=X)
        x_value = Label(self.tollbar, text="enter X value")
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
        2.rotate(self):

            """
    # not working need to fix

    def rotate(self):
        sinus = math.sin(self.rotation)
        cosinus = math.cos(self.rotation)

        print("here")

        s_lines = []
        s_curves = []

        for line in self.lines:
            x1 = line[0]
            y1 = line[1]
            x2 = line[2]
            y2 = line[3]
            s_lines.append([x1 * cosinus - y1 * sinus, x1 * sinus + y1 * cosinus, x2 * cosinus - y2 * sinus,
                            x2 * sinus + y2 * cosinus])

        for curve in self.curves:
            x1 = curve[0]
            y1 = curve[1]
            x2 = curve[2]
            y2 = curve[3]
            x3 = curve[4]
            y3 = curve[5]
            x4 = curve[6]
            y4 = curve[7]
            s_curves.append([
                x1 * cosinus - y1 * sinus,
                x1 * sinus + y1 * cosinus,
                x2 * cosinus - y2 * sinus,
                x2 * sinus + y2 * cosinus,
                x3 * cosinus - y3 * sinus,
                x3 * sinus + y3 * cosinus,
                x4 * cosinus - y4 * sinus,
                x4 * sinus + y4 * cosinus
            ])

        print(s_lines)
        print(s_curves)

        print("done")
        self.draw_file(s_lines, self.circles, s_curves)

    # ############################################ mirror ###########################################################
    # ############################################ shearing #########################################################

    # ############################################ windows ##########################################################
    """
        open_canvas(self):
        open another window to show drawing on canvas.
            """

    def open_canvas(self):
        self.window = Toplevel(master=self.menu)
        # Set bar Title
        self.window.title('CANVAS')
        # Set fixed dimensions to window
        self.window.geometry("800x500")
        # Adding canvas to the window
        self.canvas = Canvas(self.window, width=1000,
                             height=500, background='white')
        self.canvas.pack(fill=X)
        # Adding img
        self.img = PhotoImage(width=1000, height=500)
        self.canvas.create_image(
            (1000 // 2, 500 // 2), image=self.img, state="normal")

    """
        initWindow(): creates the application menu.
        creating window with Python GUI Tkinter
            """

    def initWindow(self):
        self.menu = Tk()
        self.menu.title("menu")
        self.menu.geometry("600x400")

        # add massage box to contact with the user
        self.messages = Label(self.menu, bg='pink', text=" Lets start! Please choose you're transformation ",
                              anchor='w')
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
        transform_menu.add_command(label="Mirror", command=self.open_canvas)
        transform_menu.add_separator()
        transform_menu.add_command(label="Shearing", command=self.open_canvas)
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
