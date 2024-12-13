from tkinter import Tk, Frame, Button, filedialog, Canvas, BOTH, Toplevel, Label, Entry, OptionMenu, StringVar
from PIL import Image, ImageTk

class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.start_x = None
        self.start_y = None
        self.parent = parent
        self.parent.title("Graphic Editor")
        self.parent.attributes("-toolwindow", True)
        self.parent.configure(bg='grey')
        self.create_user_interface()


    def create_user_interface(self):
        self.bind_dict = {"<Button-1>": "", "<B1-Motion>": "", "<ButtonRelease-1>": ""}
        self.open_button = Button(text="Open your image", height=2, command=self.open_image)
        self.open_button.pack(anchor='nw', padx=20, pady=20)
        self.canvas = Canvas(self.parent, bg='white')
        self.canvas.pack(fill = BOTH, expand=1, padx=20, pady=5)
        self.add_text_button = Button(text="add text", height=2, command=self.add_text, bd=0)
        self.add_text_button.configure(bg="green")
        self.add_text_button.pack(padx=10, pady=10)
        self.add_line_button = Button(text="add line", height=2, command=self.add_line, bd=0)
        self.add_line_button.configure(bg = "green")
        self.add_line_button.pack(padx=10, pady=20)
        self.add_shape_button = Button(text = "add shape", height=2, command=self.add_shape, bd = 0)
        self.add_shape_button.configure(bg = "green")
        self.add_shape_button.pack(padx = 10, pady = 20)
        self.points = []

    def open_image(self):
        self.filename = filedialog.askopenfilename(
            title = "Select Image",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"))
        )
        if self.filename:
            self.image = Image.open(self.filename)
            self.resized_image = self.image.resize((1000, 600))
            self.image_tk = ImageTk.PhotoImage(self.resized_image)
            self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image = self.image_tk)
    def add_text(self):
        if (self.bind_dict["<Button-1>"] == "add_text"):
            self.text_window.destroy()
            self.add_text_button.configure(bg="green")
            self.bind_dict["<Button-1>"] = ""
            self.canvas.unbind("<Button-1>")
        elif self.bind_dict["<Button-1>"] == "":
            self.add_text_button.configure(bg="red")
            self.bind_dict["<Button-1>"] = "add_text"
            self.canvas.bind("<Button-1>", self.write_text)
    def add_line(self):
        if self.bind_dict["<Button-1>"] == "add_line":
            self.add_line_button.configure(bg = "green")
            self.bind_dict["<Button-1>"] = ""
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.line_window.destroy()
        elif self.bind_dict["<Button-1>"] == "":
            self.add_line_button.configure(bg = "red")
            self.bind_dict["<Button-1>"] = "add_line"
            self.set_line()
            self.canvas.bind("<Button-1>",self.start_draw_line)
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
    def start_draw_line(self,event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.bind("<ButtonRelease-1>",self.end_draw_line)
    def end_draw_line(self,event):
        line_color = str(self.line_color.get())
        line_size = int(self.line_size.get())
        self.canvas.create_line(self.start_x,self.start_y, event.x, event.y, fill = line_color, width=line_size)
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
        size_label = Label(self.text_window, text = "Choose text size")
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
        self.canvas.create_text(x, y, text=text, fill=text_color, font=("Arial", text_size))
        self.text_window.destroy()
        self.canvas.bind("<Button-1>", self.write_text)

    def add_shape(self):
        if (self.bind_dict["<Button-1>"]==""):
            self.add_shape_button.configure(bg="red")
            self.bind_dict["<Button-1>"] = "add_shape"
            self.set_shape()
            self.points = []
            self.canvas.bind("<Button-1>", self.start_shape)
        elif self.bind_dict["<Button-1>"] == "add_shape":
            self.add_shape_button.configure(bg = "green")
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
        shape_color_menu = OptionMenu(self.shape_window, self.shape_width, "2",*[str(i) for i in range(3,20)])
        shape_color_menu.pack()
    def start_shape(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.bind("<ButtonRelease-1>", self.end_shape)
    def end_shape(self,event):
        if str(self.shape.get()) == "rectangle":
            self.canvas.bind("<Button-1>", self.start_shape)
            self.points =[]
            self.canvas.create_rectangle(self.start_x,self.start_y,event.x,event.y, fill=str(self.shape_color.get()), width=int(self.shape_width.get()))
        elif str(self.shape.get()) == "circle":
            self.canvas.bind("<Button-1>", self.start_shape)
            self.points=[]
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, fill=str(self.shape_color.get()), width=int(self.shape_width.get()))
        elif str(self.shape.get()) == "triangle":
            self.canvas.unbind("<Button-1>")
            if (len(self.points)==0):self.points.append((event.x, event.y))
            self.canvas.bind("<Button-1>",self.get_triangle_points)
            if (len(self.points)==3):
                self.canvas.create_polygon(self.points[0], self.points[1], self.points[2], fill = str(self.shape_color.get()))
                self.points = []
                self.canvas.bind("<Button-1>", self.start_shape)


    def get_triangle_points(self,event):
        self.points.append((event.x, event.y))


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.mainloop()
