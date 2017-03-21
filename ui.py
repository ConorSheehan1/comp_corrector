try:
    from tkinter import Tk, Label, StringVar, Entry, Button, END, IntVar, Checkbutton
    from tkinter.filedialog import askopenfilename

    # if python3 tkinter fails, try python 2 Tkinter
except ImportError:
    from Tkinter import Tk, Label, StringVar, Entry, Button, END, IntVar, Checkbutton
    from tkFileDialog import askopenfilename

import os
import glob
import shutil
from src import main


class App(object):
    def __init__(self):
        self.root = Tk()

        # set default dimensions, color and title
        self.grey = "#909296"
        self.yellow = "#f7f574"
        self.green = "#93b185"

        self.root.geometry("600x450")
        self.root.wm_title("CompCorrector")

        self.label = Label(self.root, text="path to zipfile")
        self.label.pack(pady=5)

        # set remove dirs to true by default, why keep empty folders?
        self.rm_dirs = True

        # text entry for zip path
        self.zip_dir = StringVar()
        self.entry_zip_dir = Entry(self.root, textvariable=self.zip_dir, width="400", bg=self.grey)
        self.entry_zip_dir.pack(pady=5)

        # open zip button
        self.buttontext = StringVar()
        self.buttontext.set("CHOOSE ZIP")
        Button(self.root, textvariable=self.buttontext, command=self.open_file, bg=self.yellow).pack(pady=5)

        self.label = Label(self.root, text="list of names")
        self.label.pack(pady=5)

        # text entry for names
        self.names = StringVar()
        self.entry_names = Entry(self.root, textvariable=self.names, width="400", bg=self.grey)
        self.entry_names.pack(pady=5)

        # check-boxes
        self.rm_zips = IntVar()
        self.rm_zips.set(False)
        self.check_rm_zips = Checkbutton(self.root, variable=self.rm_zips, onvalue=True, offvalue=False,
                                         text="remove zips")

        self.compile = IntVar()
        self.compile.set(False)
        self.check_compile = Checkbutton(self.root, variable=self.compile, onvalue=True, offvalue=False,
                                         text="compile files")

        self.safe_mode = IntVar()
        self.safe_mode.set(False)
        self.check_safe_mode = Checkbutton(self.root, variable=self.safe_mode, onvalue=True, offvalue=False,
                                         text="safe mode")

        self.feedback = IntVar()
        self.feedback.set(False)
        self.check_feedback = Checkbutton(self.root, variable=self.feedback, onvalue=True, offvalue=False,
                                         text="feedback.docx")

        # have checkbox checked by default
        self.check_rm_zips.select()
        self.check_compile.select()
        self.check_safe_mode.select()
        self.check_feedback.select()

        # place checkboxes on gui
        self.check_safe_mode.pack()
        self.check_rm_zips.pack()
        self.check_compile.pack()
        self.check_feedback.pack()

        # set open dir button
        self.buttontext2 = StringVar()
        self.buttontext2.set("START")
        Button(self.root, textvariable=self.buttontext2, command=self.do_work, bg=self.green).pack(pady=5)

        # label for errors
        self.error_label = Label(self.root, text="", foreground="red", bg=self.grey)
        self.error_label.pack(pady=5)

        # label for warnings
        self.warning_label = Label(self.root, text="", foreground=self.yellow, bg=self.grey)
        self.warning_label.pack(pady=5)

        # label for completion
        self.completion_label = Label(self.root, text="", bg=self.grey)
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

        if not self.safe_mode and len(glob.glob(os.path.dirname(self.entry_zip_dir.get()) + "/*")) > 1:
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
            self.error_label.configure(text=self.error_label.cget("text") + "Exception parsing names\n")
            print("Exception parsing names")
            # break out of function
            return
        try:
            if self.entry_zip_dir.get() == "":
                # append to label
                self.error_label.configure(text=self.error_label.cget("text") + "You must select a zip file to begin\n")
            else:
                # at this point names are list of strings and directory is correct
                cwd = os.path.dirname(self.entry_zip_dir.get()) + "/"
                zip_path = self.entry_zip_dir.get()

                if self.entry_names.get().strip() == "":
                    self.warning_label.configure(text=self.warning_label.cget("text") +
                                "No names included. All files will be extracted and feedback.docx will be empty\n")

                if self.safe_mode.get():
                    # make dir same name as zip (remove file extension, add slash)
                    safe_dir = os.path.basename(self.entry_zip_dir.get()).split(".")[0]+"/"
                    # create safe dir if it doesn't exist
                    if not os.path.exists(cwd + safe_dir):
                        os.mkdir(cwd + safe_dir)

                    # add safe dir to cwd and zip_path
                    cwd += safe_dir
                    zip_path = cwd + os.path.basename(self.entry_zip_dir.get())
                    print("safe mode enabled", zip_path)

                    # copy zip into safe directory
                    shutil.copy2(self.entry_zip_dir.get(), zip_path)

                # if safe mode is enabled, move zip to safe folder, then run, otherwise run in directory zip already is
                main.unzip_outer(zip_path, names)

                # get directory of zipfile, unzip and move files in subdirectories
                extraction_errors = main.unzip(cwd, rm_zips=self.rm_zips.get())
                if extraction_errors:
                    self.error_label.configure(text=self.error_label.cget("text") +
                                                        "Exception extracting: {}\n".format(extraction_errors))

                missing_names = main.missing_names(cwd, names)
                if missing_names:
                    self.warning_label.configure(text=self.warning_label.cget("text")
                                                      + "The following students seem to be missing files:\n"
                                                      + str(missing_names))

                if self.compile.get():
                    compiled = main.compile_c(cwd, "gcc")
                    if compiled > 0:
                        self.error_label.configure(text=self.error_label.cget("text") +
                                                        "Error compiling {} file(s)\n".format(compiled))
                    if compiled == -1:
                        self.error_label.configure(text=self.error_label.cget("text") +
                                                        "Exception compiling files\n")
                if self.feedback.get():
                    try:
                        main.feedback(cwd, names, missing_names)
                    except:
                        self.error_label.configure(text=self.error_label.cget("text") +
                                                        "Exception creating feedback.docx\n")

                self.completion_label.configure(text="Finished!")
                print("Finished!")
        except:
            # catch exception to allow prompt within ui, then re-raise exception
            self.error_label.configure(text=self.error_label.cget("text") + "Exception extracting files. Check the console\n")
            raise

App()
