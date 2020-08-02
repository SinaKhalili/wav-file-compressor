from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class Root(Tk):
    """
    This is the root object, which inherits from TK

    The benefit of inheritance is we can write:
    self.button instead of self.root.button
    """

    def __init__(self):
        super(Root, self).__init__()
        self.title("Wav compression analyzer")
        self.minsize(640, 400)

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)

        self.button()

    def button(self):
        self.button = ttk.Button(
            self.labelFrame, text="Browse A File", command=self.file_dialog
        )
        self.button.grid(column=1, row=1)

    def file_dialog(self):
        """
        Opens a file dialog and has the user chose a file

        This then sets some labels afterwards
        """

        self.filename = filedialog.askopenfilename(
            initialdir="./", title="Select A File",
        )
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.filename)


if __name__ == "__main__":
    root = Root()
    root.mainloop()
