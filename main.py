from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import math
import huffman
import lzw
import wave


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
        if self.filename:
            self.get_wave_info(self.filename)

    def get_wave_info(self, filename):
        """
        Print some information about the wav file
        """
        info_string = ""
        try:
            with wave.open(filename) as wav_file:
                wav_data_size_bits = wav_file.getnframes() * wav_file.getsampwidth() * 8
                info_string = f"""
Number of channels : {wav_file.getnchannels()}
Framerate: {wav_file.getframerate()}
Number of frames: {wav_file.getnframes()}
Sample width (in bytes): {wav_file.getsampwidth()}
Size of wave data (bits): {wav_data_size_bits}
                """
                wav_file.rewind()
                wav_samples = wav_file.readframes(wav_file.getnframes())

                wav_samples = [
                    wav_samples[i : i + 2] for i in range(0, len(wav_samples), 2)
                ]

                self.labelFrame_huffman = ttk.LabelFrame(self, text="HUFFMAN RESULTS:")
                self.labelFrame_huffman.grid(
                    column=0, row=2, padx=40, pady=40, ipadx=40, ipady=40
                )

                huffman_samples = huffman.get_message(wav_samples)
                huffman_stats = f"""
The resulting huffman encoded wave data is:
                {len(huffman_samples)} bits long.
This results in a:
                {round(1 - len(huffman_samples) / wav_data_size_bits, 2) * 100}% decrease in size
With a ratio of:
                1:{round(len(huffman_samples) / wav_data_size_bits, 2)} Orignal-to-compressed
                """

                self.huffman_label = ttk.Label(self.labelFrame_huffman, text="")
                self.huffman_label.grid(column=1, row=3)
                self.huffman_label.configure(text=huffman_stats)

                self.labelFrame_lzw = ttk.LabelFrame(self, text="LZW RESULTS:")
                self.labelFrame_lzw.grid(
                    column=1, row=2, padx=40, pady=40, ipadx=40, ipady=40
                )

                lzw_samples = len(lzw.get_message(wav_samples))
                lzw_samples *= 16

                lzw_stats = f"""
The resulting lzw encoded wave data is:
                {lzw_samples} bits long, if we use 16 bits for numbers.
This results in a:
                {round((1 - lzw_samples / wav_data_size_bits) * 100, 2)}% decrease in size if we use 16 bits per number
With a ratio of:
                1:{round(lzw_samples  / wav_data_size_bits, 2)} Orignal-to-compressed if we use 16 bits per number
                """

                self.lzw_label = ttk.Label(self.labelFrame_lzw, text="")
                self.lzw_label.grid(column=1, row=3)
                self.lzw_label.configure(text=lzw_stats)

            self.info_label = ttk.Label(self.labelFrame, text="")
            self.info_label.grid(column=1, row=3)
            self.info_label.configure(text=info_string)

        except wave.Error as err:
            print("Could not read wave file")


if __name__ == "__main__":
    root = Root()
    root.mainloop()
