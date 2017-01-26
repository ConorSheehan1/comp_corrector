try:
    from tkinter import Tk, Label, StringVar, Entry, Button, END, IntVar, Checkbutton
    from tkinter.filedialog import askopenfilename
# for python 2 (untested)
except ImportError:
    from Tkinter import Tk, Label, StringVar, Entry, Button, END, IntVar, Checkbutton
    from Tkinter.filedialog import askopenfilename

from src import main
import os
import glob


class App(object):
    def __init__(self):
        self.root = Tk()

        # set default dimensions, color and title
        self.root.geometry("600x500")
        self.root.configure(bg="#769ea6")
        self.root.wm_title("CompCorrector")

        self.label = Label(self.root, text="path to zipfile")
        self.label.pack(pady=5)

        # text entry for zip path
        self.zip_dir = StringVar()
        self.entry_zip_dir = Entry(self.root, textvariable=self.zip_dir, width="400")
        self.entry_zip_dir.pack(pady=5)

        # open zip button
        self.buttontext = StringVar()
        self.buttontext.set("CHOOSE ZIP")
        Button(self.root, textvariable=self.buttontext, command=self.open_file, bg="#ffff66").pack(pady=5)

        self.label = Label(self.root, text="list of names")
        self.label.pack(pady=5)

        # text entry for names
        self.names = StringVar()
        self.entry_names = Entry(self.root, textvariable=self.names, width="400")
        self.entry_names.pack(pady=5)

        self.label = Label(self.root, text="compiler")
        self.label.pack(pady=5)

        # text entry for compiler
        self.compiler_name = StringVar()
        self.compiler_name.set("gcc")
        self.compiler_name = Entry(self.root, textvariable=self.compiler_name, width="400", justify="center")
        self.compiler_name.pack(pady=5)

        # check-boxes
        self.rm_zips = IntVar()
        self.rm_zips.set(False)
        self.check_rm_zips = Checkbutton(self.root, variable=self.rm_zips, onvalue=True, offvalue=False,
                                         text="remove zips after extraction")

        self.rm_dirs = IntVar()
        self.rm_dirs.set(False)
        self.check_rm_dirs = Checkbutton(self.root, variable=self.rm_dirs, onvalue=True, offvalue=False,
                                         text="remove empty directories")

        self.compile = IntVar()
        self.compile.set(False)
        self.check_compile = Checkbutton(self.root, variable=self.compile, onvalue=True, offvalue=False,
                                         text="compile files")

        # have checkbox checked by default
        self.check_rm_zips.select()
        self.check_rm_dirs.select()
        self.check_compile.select()

        # place checkboxes on gui
        self.check_rm_zips.pack()
        self.check_rm_dirs.pack()
        self.check_compile.pack()

        # set open dir button
        self.buttontext2 = StringVar()
        self.buttontext2.set("START")
        Button(self.root, textvariable=self.buttontext2, command=self.do_work, bg="#93b185").pack(pady=5)

        # label for errors
        self.error_label = Label(self.root, text="", foreground="red", bg="grey")
        self.error_label.pack(pady=5)

        # label for warnings
        self.warning_label = Label(self.root, text="", foreground="yellow", bg="grey")
        self.warning_label.pack(pady=5)

        # label for completion
        self.completion_label = Label(self.root, text="", bg="grey")
        self.completion_label.pack(pady=5)

        self.root.mainloop()

    def open_file(self):
        # flush error label
        self.warning_label.configure(text="")

        filename = askopenfilename()
        if filename.endswith(".zip"):
            # flush old text
            self.entry_zip_dir.delete(0, END)
            # insert new text
            self.entry_zip_dir.insert(0, filename)
        else:
            # throw error
            self.error_label.configure(text="File must end with '.zip'")

        if len(glob.glob(os.path.dirname(self.entry_zip_dir.get()) + "/*")) > 1:
            self.warning_label.configure(text="Be careful, there's multiple items in the current directory")

    def do_work(self):
        # flush all labels
        self.warning_label.configure(text="")
        self.error_label.configure(text="")
        self.completion_label.configure(text="")

        try:
            names = self.entry_names.get().split("\n")
            # remove ' in all strings
            names = list(map(lambda n: n.replace("'", ""), names))
        except:
            # append error to label
            self.error_label.configure(text=self.error_label.cget("text") + "Error parsing names\n")
        try:
            if self.entry_zip_dir.get() == "":
                # append to label
                self.error_label.configure(text=self.error_label.cget("text") + "You must select a zip file to begin\n")
            else:
                # at this point names are list of strings and directory is correct
                main.unzip_outer(self.entry_zip_dir.get(), names)

                cwd = os.path.dirname(self.entry_zip_dir.get()) + "/"

                # get directory of zipfile, unzip and move files in subdirectories
                main.rename(cwd, rm_dirs=self.rm_dirs.get(),
                            rm_zips=self.rm_zips.get())

                missing_names = main.missing_names(cwd, names)
                if missing_names:
                    print("!!!!!", missing_names, len(missing_names))
                    self.warning_label.configure(text=self.warning_label.cget("text")
                                                      + "The following students seem to be missing files\n"
                                                      + str(missing_names))

                if self.compile:
                    compiled = main.compile(cwd, "gcc")
                    if compiled > 0:
                        self.error_label.configure(text=self.error_label.cget("text") +
                                                        "Error compiling {} file(s)\n".format(compiled))
                    if compiled == -1:
                        self.error_label.configure(text=self.error_label.cget("text") +
                                                        "Exception compiling files\n".format(compiled))

                self.completion_label.configure(text="Finished!")
                print("Finished!")
        except:
            self.error_label.configure(text=self.error_label.cget("text") + "Problem moving files\n")


App()
