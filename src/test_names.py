from tkinter import Tk, Label, StringVar, Entry, Button, END, IntVar, Checkbutton, LEFT, X
from tkinter.filedialog import askopenfilename, askdirectory
from src import main


class App(object):
    def __init__(self):
        self.root = Tk()

        # set default dimensions, color and title
        self.root.geometry("500x200")
        self.root.configure(bg="#769ea6")
        self.root.wm_title("CompCorrector")

        self.label = Label(self.root, text="List of names")
        self.label.pack(pady=5)

        # set text entry
        self.input_dir = StringVar()
        self.entry_input_dir = Entry(self.root, textvariable=self.input_dir, width="400")
        self.entry_input_dir.pack(pady=5)

        # set open dir button
        self.buttontext = StringVar()
        self.buttontext.set("Open")
        Button(self.root, textvariable=self.buttontext, command=self.sort_names, bg="#ffff66").pack(pady=5)

        self.root.mainloop()

    def sort_names(self):
        print(str(self.entry_input_dir.get()).split("\n"))

# Tk().withdraw()
App()
