import os
from random import randint
from tkinter import Tk, Frame, Button, filedialog, Canvas, BOTH, Toplevel, Label, Entry, OptionMenu, StringVar, LEFT, \
    messagebox
from PIL import Image, ImageTk, ImageGrab

from BasicFunctions import BasicFunctions

class Application(Frame, BasicFunctions):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.start_x = None
        self.start_y = None
        self.parent = parent
        self.parent.title("Graphic Editor")
        self.parent.attributes("-fullscreen", True)
        self.parent.configure(bg='grey')
        self.create_user_interface()

    def create_user_interface(self):
        self.bind_dict = {"<Button-1>": "", "<B1-Motion>": "", "<ButtonRelease-1>": ""}
        self.image = Image.new('RGBA', (1500, 1000), (255, 255, 255))
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.points = []
        self.undo_stack = []
        self.undo_stack.append((self.image.copy(), []))
        self.redo_stack = []
        self.action_redo_stack = []
        self.current_actions = []

        open_icon = ImageTk.PhotoImage(file="..buttons/open.png")
        self.open_button = Button(self.parent, image=open_icon, height=48, command=self.open_image)
        self.open_button.image = open_icon
        self.open_button.pack(anchor='nw', padx=20, pady=20)

        self.canvas = Canvas(self.parent, bg='white', height=250, width=250)
        self.canvas.pack(fill=BOTH, expand=1, padx=20, pady=20)

        add_text_icon = ImageTk.PhotoImage(file="..buttons/add_text.png")
        self.add_text_button = Button(self.parent, image=add_text_icon, command=self.add_text,
                                      bg='white')
        self.add_text_button.image = add_text_icon
        self.add_text_button.pack(side=LEFT, padx=20)

        add_line_icon = ImageTk.PhotoImage(file="..buttons/line.png")
        self.add_line_button = Button(self.parent, image=add_line_icon, command=self.add_line,
                                      bg='white')
        self.add_line_button.image = add_line_icon
        self.add_line_button.pack(side=LEFT, padx=20)

        add_shape_icon = ImageTk.PhotoImage(file="..buttons/shape.png")
        self.add_shape_button = Button(self.parent, image=add_shape_icon, command=self.add_shape,
                                       bg='white')
        self.add_shape_button.image = add_shape_icon
        self.add_shape_button.pack(side=LEFT, padx=20)

        undo_icon = ImageTk.PhotoImage(file="..buttons/undo.png")
        self.undo_button = Button(self.parent, image=undo_icon, command=self.undo,
                                  bg='white')
        self.undo_button.image = undo_icon
        self.undo_button.pack(side=LEFT, padx=20)

        redo_icon = ImageTk.PhotoImage(file="..buttons/redo.png")
        self.redo_button = Button(self.parent, image=redo_icon, command=self.redo,
                                  bg='white')
        self.redo_button.image = redo_icon
        self.redo_button.pack(side=LEFT, padx=20)

        back_icon = ImageTk.PhotoImage(file="..buttons/back.png")
        self.set_image_background = Button(self.parent, image=back_icon, command=self.config_image_bg,
                                           bg='white')
        self.set_image_background.image = back_icon
        self.set_image_background.pack(side=LEFT, padx=20, pady=5)

        save_icon = ImageTk.PhotoImage(file="..buttons/save.png")
        self.save_button = Button(self.parent, image=save_icon, command=self.save_file, bg='white')
        self.save_button.image = save_icon
        self.save_button.pack(side=LEFT, padx=20, pady=5)

    def open_image(self):
        self.filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"))
        )
        if self.filename:
            self.image = Image.open(self.filename)
            self.image.convert("RGBA")
            self.resized_image = self.image.resize((1500, 1000))
            self.image_tk = ImageTk.PhotoImage(self.resized_image)
            self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, image=self.image_tk)
            self.undo_stack.append(self.image.copy() if self.image else None, [])
            self.redo_stack.clear()

    def save_file(self):
        path = os.getcwd() + "/outputFiles"
        if os.path.exists(path):
            filename = f'image_{randint(0, 100)}.png'
            x = self.canvas.winfo_rootx() + 10
            y = self.canvas.winfo_rooty() + 40
            w = x + self.canvas.winfo_width() + 370
            h = y + self.canvas.winfo_height() + 150
            ImageGrab.grab().crop((x, y, w, h)).save(path + "/" + filename)
            self.show_info(filename, path)
        else:
            os.mkdir(path)
            self.save_file()

    def show_info(self, filename, path):
        messagebox.showinfo("Сохранение", "Файл с именем: " + filename + " сохранен в папку: " + path)

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append((self.undo_stack[-1][0].copy(), self.undo_stack[-1][1]))
            self.undo_stack.pop()
            self.image, self.current_actions = self.undo_stack[-1]
            if not (self.undo_stack):
                self.undo_stack.append((self.image.copy(), []))
            self.update_undo_canvas()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append((self.redo_stack[-1][0].copy(), self.redo_stack[-1][1]))
            self.image, self.current_actions = self.redo_stack.pop()
            self.update_redo_canvas()

    def update_undo_canvas(self):
        self.canvas.delete("all")
        if self.image:
            self.resized_image = self.image.resize((1500, 1000))
            self.image_tk = ImageTk.PhotoImage(self.resized_image)
            self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, image=self.image_tk)
        if self.undo_stack:
            for entry in self.undo_stack:
                if len(entry[1]) != 0:
                    type = entry[1][0]
                    if (type == "text"):
                        type, x, y, text, text_color, text_size = entry[1]
                        self.canvas.create_text(x, y, text=text, fill=text_color, font=("Arial", text_size))
                    elif (type == "line"):
                        type, start_x, start_y, end_x, end_y, line_color, line_size = entry[1]
                        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=line_color, width=line_size)
                    elif (type == "shape"):
                        shape_type = entry[1][1]
                        if (shape_type == "rectangle"):
                            type, shape_type, start_x, start_y, end_x, end_y, shape_color, shape_size = entry[1]
                            self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=shape_color,
                                                         width=shape_size)
                        if (shape_type == "circle"):
                            type, shape_type, start_x, start_y, end_x, end_y, shape_color, shape_size = entry[1]
                            self.canvas.create_oval(start_x, start_y, end_x, end_y, fill=shape_color, width=shape_size)
                        if (shape_type == "triangle"):
                            type, shape_type, x1, y1, x2, y2, x3, y3, shape_color = entry[1]
                            self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=shape_color)

    def update_redo_canvas(self):
        self.canvas.delete("all")
        if self.image:
            self.resized_image = self.image.resize((1500, 1000))
            self.image_tk = ImageTk.PhotoImage(self.resized_image)
            self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, image=self.image_tk)
        if self.undo_stack:
            for entry in self.undo_stack:
                if len(entry[1]) != 0:
                    type = entry[1][0]
                    if (type == "text"):
                        type, x, y, text, text_color, text_size = entry[1]
                        self.canvas.create_text(x, y, text=text, fill=text_color, font=("Arial", text_size))
                    elif (type == "line"):
                        type, start_x, start_y, end_x, end_y, line_color, line_size = entry[1]
                        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=line_color, width=line_size)
                    elif (type == "shape"):
                        shape_type = entry[1][1]
                        if (shape_type == "rectangle"):
                            type, shape_type, start_x, start_y, end_x, end_y, shape_color, shape_size = entry[1]
                            self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=shape_color,
                                                         width=shape_size)
                        if (shape_type == "circle"):
                            type, shape_type, start_x, start_y, end_x, end_y, shape_color, shape_size = entry[1]
                            self.canvas.create_oval(start_x, start_y, end_x, end_y, fill=shape_color, width=shape_size)
                        if (shape_type == "triangle"):
                            type, shape_type, x1, y1, x2, y2, x3, y3, shape_color = entry[1]
                            self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=shape_color)
        if self.current_actions:
            type = self.current_actions[0]
            if (type == "text"):
                type, x, y, text, text_color, text_size = self.current_actions
                self.canvas.create_text(x, y, text=text, fill=text_color, font=("Arial", text_size))
            elif (type == "line"):
                type, start_x, start_y, end_x, end_y, line_color, line_size = self.current_actions
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=line_color, width=line_size)
            elif (type == "shape"):
                shape_type = self.current_actions[1]
                if (shape_type == "rectangle"):
                    type, shape_type, start_x, start_y, end_x, end_y, shape_color, shape_size = self.current_actions
                    self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=shape_color,
                                                 width=shape_size)
                if (shape_type == "circle"):
                    type, shape_type, start_x, start_y, end_x, end_y, shape_color, shape_size = self.current_actions
                    self.canvas.create_oval(start_x, start_y, end_x, end_y, fill=shape_color, width=shape_size)
                if (shape_type == "triangle"):
                    type, shape_type, x1, y1, x2, y2, x3, y3, shape_color = self.current_actions
                    self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=shape_color)

    def set_image_bg(self):
        if self.image:
            self.undo_stack.clear()
            self.redo_stack.clear()
            self.image = self.image.convert('RGBA')
            self.image = Image.alpha_composite(self.image, Image.new("RGBA", self.image.size,
                                                                     self.bg_color_dict[str(self.bg_color.get())]))
            self.image_tk = ImageTk.PhotoImage(self.image.resize((1500, 1000)))
            self.canvas.create_image(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, image=self.image_tk)
            self.undo_stack.append((self.image.copy(), ()))
            self.bg_window.destroy()

    def config_image_bg(self):
        if self.image:
            self.bg_color_dict = {"black": (0, 0, 0, 128), "white": (255, 255, 255, 128), "red": (255, 0, 0, 128),
                                  "blue": (0, 0, 255, 128), "green": (0, 255, 0, 128)}
            self.bg_window = Toplevel()
            self.bg_window.geometry("300x300")
            bg_color_label = Label(self.bg_window, text="Choose background color")
            bg_color_label.pack()
            self.bg_color = StringVar()
            self.bg_color.set("black")
            bg_color_menu = OptionMenu(self.bg_window, self.bg_color, "black", "red", "blue", "green", "white")
            bg_color_menu.pack()
            set_button = Button(self.bg_window, height=2, text="Set", command=self.set_image_bg)
            set_button.pack(padx=5, pady=5)

    def add_text(self):
        if (self.bind_dict["<Button-1>"] == "add_text"):
            self.text_window.destroy()
            self.add_text_button.configure(bg="white")
            self.bind_dict["<Button-1>"] = ""
            self.canvas.unbind("<Button-1>")
        elif self.bind_dict["<Button-1>"] == "":
            self.add_text_button.configure(bg="red")
            self.bind_dict["<Button-1>"] = "add_text"
            self.canvas.bind("<Button-1>", self.write_text)

    def add_line(self):
        if self.bind_dict["<Button-1>"] == "add_line":
            self.add_line_button.configure(bg="white")
            self.bind_dict["<Button-1>"] = ""
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.line_window.destroy()
        elif self.bind_dict["<Button-1>"] == "":
            self.add_line_button.configure(bg="red")
            self.bind_dict["<Button-1>"] = "add_line"
            self.set_line()
            self.canvas.bind("<Button-1>", self.start_draw_line)

    def set_line(self):
        self.line_window = Toplevel()
        self.line_window.geometry("300x300")
        line_color_label = Label(self.line_window, text="Choose line color")
        line_color_label.pack()
        self.line_color = StringVar()
        self.line_color.set("black")
        line_color_menu = OptionMenu(self.line_window, self.line_color, "black", "red", "blue", "green")
        line_color_menu.pack()
        line_size_label = Label(self.line_window, text="Choose line width")
        line_size_label.pack()
        self.line_size = StringVar()
        self.line_size.set("2")
        line_size_menu = OptionMenu(self.line_window, self.line_size, "2", "4", "6", "8", "10", "12")
        line_size_menu.pack()

    def start_draw_line(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.bind("<ButtonRelease-1>", self.end_draw_line)

    def end_draw_line(self, event):
        line_color = str(self.line_color.get())
        line_size = int(self.line_size.get())
        self.current_actions = ("line", self.start_x, self.start_y, event.x, event.y, line_color, line_size)
        self.undo_stack.append((self.image.copy(), self.current_actions))
        self.redo_stack.clear()
        self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=line_color, width=line_size)

    def write_text(self, event):
        self.canvas.unbind("<Button-1>")
        self.text_window = Toplevel()
        self.text_window.geometry("300x300")
        text_label = Label(self.text_window, text="Write text")
        text_label.pack()
        text_entry = Entry(self.text_window)
        text_entry.pack()

        color_label = Label(self.text_window, text="Choose text color")
        color_label.pack()
        self.text_color = StringVar()
        self.text_color.set("black")
        text_color_menu = OptionMenu(self.text_window, self.text_color, "black", "red", "blue", "green")
        text_color_menu.pack()
        size_label = Label(self.text_window, text="Choose text size")
        size_label.pack()
        self.text_size = StringVar()
        self.text_size.set("12")
        text_size_menu = OptionMenu(self.text_window, self.text_size, "10", "12", "14", "16")
        text_size_menu.pack()
        add_button = Button(self.text_window, text="Add text",
                            command=lambda: self.perform_text(text_entry.get(), event))

        add_button.pack()

    def perform_text(self, text, event):
        x, y = event.x, event.y
        text_color = str(self.text_color.get())
        text_size = int(self.text_size.get())
        self.current_actions = ("text", x, y, text, text_color, text_size)
        self.undo_stack.append((self.image.copy(), self.current_actions))
        self.redo_stack.clear()
        self.canvas.create_text(x, y, text=text, fill=text_color, font=("Arial", text_size))
        self.canvas.create_text(x, y, text=text, fill=text_color, font=("Arial", text_size))
        self.text_window.destroy()
        self.canvas.bind("<Button-1>", self.write_text)

    def add_shape(self):
        if (self.bind_dict["<Button-1>"] == ""):
            self.add_shape_button.configure(bg="red")
            self.bind_dict["<Button-1>"] = "add_shape"
            self.set_shape()
            self.points = []
            self.canvas.bind("<Button-1>", self.start_shape)
        elif self.bind_dict["<Button-1>"] == "add_shape":
            self.add_shape_button.configure(bg="white")
            self.bind_dict["<Button-1>"] = ""
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.shape_window.destroy()

    def set_shape(self):
        self.shape_window = Toplevel()
        self.shape_window.geometry("300x300")
        shape_select_label = Label(self.shape_window, text="Choose shape")
        shape_select_label.pack()
        self.shape = StringVar()
        self.shape.set("rectangle")
        shape_select_menu = OptionMenu(self.shape_window, self.shape, "rectangle", "circle", "triangle")
        shape_select_menu.pack()
        self.shape_color = StringVar()
        self.shape_color.set("black")
        shape_color_menu = OptionMenu(self.shape_window, self.shape_color, "black", "red", "green", "blue")
        shape_color_menu.pack()
        self.shape_width = StringVar()
        self.shape_width.set("2")
        shape_color_menu = OptionMenu(self.shape_window, self.shape_width, "2", *[str(i) for i in range(3, 20)])
        shape_color_menu.pack()

    def start_shape(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.bind("<ButtonRelease-1>", self.end_shape)

    def end_shape(self, event):
        if str(self.shape.get()) == "rectangle":
            self.canvas.bind("<Button-1>", self.start_shape)
            self.points = []
            self.current_actions = (
                "shape", "rectangle", self.start_x, self.start_y, event.x, event.y, str(self.shape_color.get()),
                int(self.shape_width.get()))
            self.undo_stack.append((self.image.copy(), self.current_actions))
            self.redo_stack.clear()
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, fill=str(self.shape_color.get()),
                                         width=int(self.shape_width.get()))
        elif str(self.shape.get()) == "circle":
            self.canvas.bind("<Button-1>", self.start_shape)
            self.points = []
            self.current_actions = (
                "shape", "circle", self.start_x, self.start_y, event.x, event.y, str(self.shape_color.get()),
                int(self.shape_width.get()))
            self.undo_stack.append((self.image.copy(), self.current_actions))
            self.redo_stack.clear()
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, fill=str(self.shape_color.get()),
                                    width=int(self.shape_width.get()))
        elif str(self.shape.get()) == "triangle":
            self.canvas.unbind("<Button-1>")
            if (len(self.points) == 0): self.points.append((event.x, event.y))
            self.canvas.bind("<Button-1>", self.get_triangle_points)
            if (len(self.points) == 3):
                self.current_actions = (
                    "shape", "triangle", self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1],
                    self.points[2][0], self.points[2][1], str(self.shape_color.get()))
                self.undo_stack.append((self.image.copy(), self.current_actions))
                self.redo_stack.clear()
                self.canvas.create_polygon(self.points[0], self.points[1], self.points[2],
                                           fill=str(self.shape_color.get()))
                self.points = []
                self.canvas.bind("<Button-1>", self.start_shape)

    def get_triangle_points(self, event):
        self.points.append((event.x, event.y))

root = Tk()
app = Application(root)
app.mainloop()
