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

        self.label = Label(self.root, text="Choose a directory")
        self.label.pack()

        # set text entry
        self.input_dir = StringVar()
        self.entry_input_dir = Entry(self.root, textvariable=self.input_dir, width="400")
        self.entry_input_dir.pack()

        # set open dir button
        self.buttontext = StringVar()
        self.buttontext.set("Open")
        Button(self.root, textvariable=self.buttontext, command=self.open_file).pack()

        self.rm_zips = IntVar()
        self.rm_zips.set(False)
        self.button_rm_zips = Checkbutton(self.root, variable=self.rm_zips, onvalue=True, offvalue=False,
                                          text="Remove zips after extraction")
        self.button_rm_zips.pack(side=LEFT)

        self.rm_dirs = IntVar()
        self.rm_dirs.set(False)
        self.button_rm_dirs = Checkbutton(self.root, variable=self.rm_dirs, onvalue=True, offvalue=False,
                                          text="Remove empty directories after moving files")
        self.button_rm_dirs.pack(side=LEFT)


        self.root.mainloop()

    def open_file(self):
        # filename = askopenfilename()
        dirname = askdirectory()
        # flush old text
        self.entry_input_dir.delete(0, END)
        # insert new text
        self.entry_input_dir.insert(0, dirname)
        print(self.entry_input_dir.get())

# Tk().withdraw()
App()
# main.rename("C:/Users/conor/Documents/GitHub/CompCorrector/outer/test/", rm=True)