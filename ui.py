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

        self.label = Label(self.root, text="Choose a directory \n(should contain subdirectories, which contain files to be graded)")
        self.label.pack(pady=5)

        # set text entry
        self.input_dir = StringVar()
        self.entry_input_dir = Entry(self.root, textvariable=self.input_dir, width="400")
        self.entry_input_dir.pack(pady=5)

        # set open dir button
        self.buttontext = StringVar()
        self.buttontext.set("Open")
        Button(self.root, textvariable=self.buttontext, command=self.open_file, bg="#ffff66").pack(pady=5)

        # check-boxes
        self.rm_zips = IntVar()
        self.rm_zips.set(False)
        self.check_rm_zips = Checkbutton(self.root, variable=self.rm_zips, onvalue=True, offvalue=False,
                                         text="Remove zips after extraction")
        self.check_rm_zips.pack()

        self.rm_dirs = IntVar()
        self.rm_dirs.set(False)
        self.check_rm_dirs = Checkbutton(self.root, variable=self.rm_dirs, onvalue=True, offvalue=False,
                                         text="Remove empty directories")
        self.check_rm_dirs.pack()

        # set open dir button
        self.buttontext2 = StringVar()
        self.buttontext2.set("Start")
        Button(self.root, textvariable=self.buttontext2, command=self.do_work, bg="#93b185").pack(pady=5)

        self.root.mainloop()

    def open_file(self):
        # filename = askopenfilename()
        dirname = askdirectory()
        # flush old text
        self.entry_input_dir.delete(0, END)
        # insert new text
        self.entry_input_dir.insert(0, dirname)
        print(self.entry_input_dir.get())

    def do_work(self):
        try:
            main.rename(self.entry_input_dir.get() + "/", rm_dirs=self.rm_dirs.get(), rm_zips=self.rm_zips.get())
        except ValueError:
            print("The path specified was empty or not a directory")

# Tk().withdraw()
App()