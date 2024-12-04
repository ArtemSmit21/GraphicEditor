from tkinter import Tk, Frame, Button, filedialog, Canvas, BOTH
from PIL import Image, ImageTk

class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Graphic Editor")
        self.parent.attributes("-fullscreen", True)
        self.parent.configure(bg='grey')
        self.create_user_interface()

    def create_user_interface(self):
        self.open_button = Button(text="Open your image", height=2, command=self.open_image)
        self.open_button.pack(anchor='nw', padx=20, pady=20)

        self.canvas = Canvas(self.parent, bg='white')
        self.canvas.pack(fill = BOTH, expand=1, padx=20, pady=5)

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

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.mainloop()
