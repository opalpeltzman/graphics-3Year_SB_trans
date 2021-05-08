"""
Authors:
Ido Betesh 307833822
Guy Sharir 310010244
Opal Peltzman 208521385
"""
# problems:
# 1. when trying to read a file for the second time
# 2. mirror when its max value and not min
# 3. rotation
# 4. shearing
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
       deletes all drawing from canvas.
            """
    def clean_canvas(self):
        if self.canvas != 0:
            print("here")
            self.canvas.delete("all")
            print("clean canvas")
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
        if fileName:
            with open(fileName) as f:
                for row in f:
                    points = re.findall(r'\d+[.]+\d|\d+', row)
                    # points = np.array(points)

                    points = list(map(float, points))

                    # new = [int(x * 10) for x in points]
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
        maxWidth = 0
        maxHight = 0

        for line in self.lines:
            for i in range(0, len(line)):
                if i % 2 == 0:  # x values
                    maxWidth = max(line[i], maxWidth)

                if i % 2 == 1:  # x values
                    maxHight = max(line[i], maxHight)

        for curve in self.curves:
            for i in range(0, len(curve)):
                if i % 2 == 0:  # x values
                    maxWidth = max(curve[i], maxWidth)

                if i % 2 == 1:  # x values
                    maxHight = max(curve[i], maxHight)

        for circle in self.circles:
            maxWidth = max(circle[0], maxWidth)
            maxHight = max(circle[1], maxHight)

        n_lines = []
        n_circles = []
        n_curves = []

        y_ratio = 1
        x_ratio = 1

        maxWidth += maxWidth
        maxHight += maxHight

        for line in self.lines:
            tmp = []
            for i in range(0, len(line)):
                if i % 2 == 0:  # x values
                    tmp.append(line[i] / maxWidth * self.size)

                if i % 2 == 1:  # x values
                    tmp.append(self.size - (line[i] / maxHight * self.size))

            n_lines.append(tmp)

        for curve in self.curves:
            tmp = []
            for i in range(0, len(curve)):
                if i % 2 == 0:  # x values
                    tmp.append(curve[i] / maxWidth * self.size)

                if i % 2 == 1:  # x values
                    tmp.append(self.size - (curve[i] / maxHight * self.size))

                n_curves.append(tmp)

        for circle in self.circles:
            n_circles.append([circle[0] / maxWidth * self.size,
                              self.size - (circle[1] / maxHight * self.size),
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
        get user inputs acoording to the transaction 
        and call the correct transformation function.
            """
    def get_user_inputs(self):
        # clean canvas before translations
        self.clean_canvas()
        # {0:scaling, 1:rotation, 2:translation, 3:mirror, 4:shearing}
        if self.flag == 0:
            self.scaling_value = float(self.x_entry.get())
            self.scalling_transformation()
        elif self.flag == 1:
            self.move_x = float(self.x_entry.get())
            self.move_y = -1 * float(self.y_entry.get())
            self.translation()
        elif self.flag == 2:
            self.rotation = float(self.x_entry.get())
            self.rotate()
        elif self.flag == 3:
            self.axis = str(self.x_entry.get())
            self.mirror_transformation()
        elif self.flag == 4:
            self.axis = str(self.x_entry.get())
            self.move_x = float(self.y_entry.get())
            self.shearing()

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


    #################################
    #######  transformations  #######
    #################################
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
        x_value = Label(self.tollbar, text="enter scaling value")
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
        !!!!!!!!!!!!!!!!!!!!!! info
            """
    def scalling_transformation(self):
    # change y to division instead of multiply!!!
        s_lines = []
        s_circles = []
        s_curves = []

        for line in self.lines:
            s_lines.append([x * self.scaling_value for x in line])

        for circle in self.circles:
            s_circles.append([x * self.scaling_value for x in circle])

        for curve in self.curves:
            s_curves.append([x * self.scaling_value for x in curve])
        print(self.lines)
        print(s_lines)
        # self.lines = s_lines
        # self.circles = s_circles
        # self.curves = s_curves

        self.draw_file(s_lines, s_circles, s_curves)

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
        !!!!!!!!!!!!!!!!!!!!!! info
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
        Transformations -
        3.rotate(self):
        !!!!!!!!!!!!!!!!!!!!!! info
            """
    def get_calculated_rotation_x(self, x, y):
        r = math.sqrt(pow(x, 2) + pow(y, 2))
        phi = math.atan2(y, x) * 180 / math.pi

        return r * math.cos(phi)

    def get_calculated_rotation_y(self, x, y):
        r = math.sqrt(pow(x, 2) + pow(y, 2))
        phi = math.atan2(y, x) * 180 / math.pi

        return r * math.sin(phi)

    def rotate(self):
        sinus = math.sin(self.rotation)
        cosinus = math.cos(self.rotation)

        s_lines = []
        s_curves = []
        s_circles = []

        for line in self.lines:
            x1 = line[0]
            y1 = line[1]
            x2 = line[2]
            y2 = line[3]

            g_x1 = self.get_calculated_rotation_x(x1, y1)
            g_y1 = self.get_calculated_rotation_y(x1, y1)

            g_x2 = self.get_calculated_rotation_x(x2, y2)
            g_y2 = self.get_calculated_rotation_y(x2, y2)

            s_lines.append([g_x1 * cosinus - g_y1 * sinus, g_x1 * sinus + g_y1 * cosinus, g_x2 * cosinus - g_y2 * sinus,
                            g_x2 * sinus + g_y2 * cosinus])

        for curve in self.curves:
            x1 = curve[0]
            y1 = curve[1]
            x2 = curve[2]
            y2 = curve[3]
            x3 = curve[4]
            y3 = curve[5]
            x4 = curve[6]
            y4 = curve[7]

            g_x1 = self.get_calculated_rotation_x(x1, y1)
            g_y1 = self.get_calculated_rotation_y(x1, y1)

            g_x2 = self.get_calculated_rotation_x(x2, y2)
            g_y2 = self.get_calculated_rotation_y(x2, y2)

            g_x3 = self.get_calculated_rotation_x(x3, y3)
            g_y3 = self.get_calculated_rotation_y(x3, y3)

            g_x4 = self.get_calculated_rotation_x(x4, y4)
            g_y4 = self.get_calculated_rotation_y(x4, y4)

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

        for circle in self.circles:
            x = circle[0]
            y = circle[1]

            g_x = self.get_calculated_rotation_x(x, y)
            g_y = self.get_calculated_rotation_y(x, y)

            s_circles.append([g_x * cosinus - g_y * sinus,
                              g_x * sinus + g_y * cosinus, circle[2]])

        print(s_lines)

        self.lines = s_lines
        self.circles = s_circles
        self.curves = s_curves

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
        !!!!!!!!!!!!!!!!!!!!! info
            """
    def mirror_transformation(self):
        min_y = 0
        mix_x = 0
        s_lines = []
        s_circles = []
        s_curves = []

        if self.axis == 'X' or self.axis == 'x':
            for line in self.lines:
                s_lines.append([line[0], line[1] * -1, line[2],
                                line[3] * -1])
                if min(s_lines[0]) < min_y:
                    min_y = min(s_lines[0])

            for circle in self.circles:
                if circle[1] * -1 < min_y:
                    min_y = circle[1] * -1
                s_circles.append([circle[0], circle[1] * -1, circle[2]])

            for curve in self.curves:
                s_curves.append([curve[0], curve[1] * -1, curve[2], curve[3] * -1, curve[4], curve[5] * -1, curve[6],
                                 curve[7] * -1])
                if min(s_curves[0]) < min_y:
                    min_y = min(s_curves[0])
            self.move_y = -1 * min_y

        if self.axis == 'Y' or self.axis == 'y':
            for line in self.lines:
                s_lines.append([line[0] * -1, line[1], line[2] * -1,
                                line[3]])
                if min(s_lines[0]) < mix_x:
                    mix_x = min(s_lines[0])

            for circle in self.circles:
                if circle[0] * -1 < mix_x:
                    mix_x = circle[0] * -1
                s_circles.append([circle[0] * -1, circle[1], circle[2]])

            for curve in self.curves:
                s_curves.append(
                    [curve[0] * -1, curve[1], curve[2] * -1, curve[3], curve[4] * -1, curve[5], curve[6] * -1,
                     curve[7]])
                if min(s_curves[0]) < mix_x:
                    mix_x = min(s_curves[0])
            self.move_x = -1 * mix_x

        self.lines = s_lines
        self.circles = s_circles
        self.curves = s_curves

        self.translation()
        self.draw_file(self.lines, self.circles, self.curves)


    """
        shearing_input(self):
        get shearing value from user
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
        !!!!!!!!!!!!!!!!!!!!! info
            """
    def shearing(self):
        xMatrix = [[1, 0, 0],
                   [self.move_x, 1, 0],
                   [0, 0, 1]]

        yMatrix = [[1, self.move_x, 0],
                   [0, 1, 0],
                   [0, 0, 1]]

        sh_lines = []
        sh_circles = []
        sh_curves = []

        for line in self.lines:
            if self.axis == 'x' or self.axis == 'X':
                line_matmul = np.matmul([line[0], line[1], 1], xMatrix)
            else:
                line_matmul = np.matmul([line[0], line[1], 1], yMatrix)
                # print(f"matmul: {line_matmul}")
            sh_lines.append([line_matmul[0],
                            line_matmul[1], line[2], line[3]])

        for circle in self.circles:
            if self.axis == 'x' or self.axis == 'X':
                circle_matmul = np.matmul([circle[0], circle[1], 1], xMatrix)
            else:
                circle_matmul = np.matmul([circle[0], circle[1], 1], yMatrix)
            sh_circles.append([
                circle_matmul[0], circle_matmul[1], circle[2]])

        for curve in self.curves:
            if self.axis == 'x' or self.axis == 'X':
                curve_matmul = np.matmul([curve[0], curve[1], 1], xMatrix)
            else:
                curve_matmul = np.matmul([curve[0], curve[1], 1], yMatrix)
            sh_curves.append([
                curve_matmul[0], curve_matmul[1], curve[2], curve[3], curve[4], curve[5], curve[6], curve[7]])

        self.lines = sh_lines
        self.circles = sh_circles
        self.curves = sh_curves

        self.draw_file(self.lines, self.circles, self.curves)



    #################################
    #######        GUI        #######
    #################################
    def on_closing(self):
        print("canvas window is closed")
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
        transform_menu.add_command(label="Mirror", command=self.mirror_input)
        transform_menu.add_separator()
        transform_menu.add_command(label="Shearing", command=self.shearing_input)
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
    print(math.atan2(0, 1) * 180 / math.pi)
    print(math.atan2(0, -1) * 180 / math.pi)
    # print(math.atan2(1, -1) * 180 / math.pi)
    # print(math.atan2(-1, ) * 180 / math.pi)
    myWindowApp()


if __name__ == '__main__':
    main()