from tkinter import Tk, Frame, Button, filedialog

class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.create_user_interface()

    def create_user_interface(self):
        self.btn_open = Button(text="Open your image", height = 2, width = 14, command = self.open_image)
        self.btn_open.place(x = 25, y = 60)

    def open_image(self):
        self.filename = filedialog.askopenfilename()

if __name__ == '__main__':
    root = Tk()
    root.title("Graphic Editor")
    root.geometry('800x500+200+100')
    app = Application(root)
    app.mainloop()
