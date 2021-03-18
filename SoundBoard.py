from os import listdir, mkdir
from os.path import isfile, join, exists
import tkinter as tk
from tkinter.ttk import *
from functools import partial
from pygame import mixer
import keyboard
import ctypes

soundPlaying = ""
Keys = [82, 79, 80, 81, 75, 76, 77, 71, 72, 73]  # numpad codes 0-9
user32 = ctypes.WinDLL('user32')  # to check on the numlock state


# get all files in sounds directory
def get_files(path):
    if not exists(path):
        mkdir(path)
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles


def start():
    root = tk.Tk()
    root.title("SoundBoard")
    root.minsize(200, 100)
    mixer.init()
    SoundFiles = get_files("sounds/")
    keyboard.add_hotkey(Keys[0], muteAll)
    create_widgets(root, SoundFiles)
    root.mainloop()


def create_widgets(root, SoundFiles):
    style = Style()
    style.configure('TButton', font=('calibri', 10),
                    borderwidth='4')

    if len(SoundFiles) <= 0:
        nofile = tk.Label(
            root, text="No audio files found, please add some audio in sounds folder and try again")
        nofile.grid(column=1)

    label_frame = tk.LabelFrame(root, text='Sounds', relief=tk.GROOVE, bd=2)
    label_frame.pack(expand=1, fill='both', padx=10, pady=10)
    for index, val in enumerate(SoundFiles):
        if index == 9:  # the 9 numbers are mapped
            break
        key = index + 1
        keyboard.add_hotkey(Keys[key], key_pressed,
                            args=[val])

        btn = Button(label_frame, text=str(key) + "- " + val.split('.', 1)[0], style='TButton', command=partial(
            play, ("sounds/" + val)))
        btn.pack(side=tk.TOP, padx=10, pady=10, expand=1)

    quit = Button(root, text="QUIT", style='TButton',
                  command=root.destroy)

    quit.pack(side=tk.TOP, padx=10, pady=10, expand=1, fill=tk.X)

    stat = tk.Label(root, text="Use Numlock to enable and disable the board")
    keyboard.add_hotkey("numlock", numUpdate, args=[stat])
    stat.pack()


def play(path):
    mixer.music.load(path)
    mixer.music.play()


def muteAll():
    mixer.music.stop()


def numUpdate(stat):
    numlock = user32.GetKeyState(0x90)
    if not numlock:
        stat.configure(text="OFF", fg="red")
    else:
        stat.configure(text="ON", fg="green")


def key_pressed(sound):
    global soundPlaying
    numlock = user32.GetKeyState(0x90)
    if not numlock:
        if sound != soundPlaying or not mixer.music.get_busy():
            play("sounds/" + sound)
            soundPlaying = sound
        else:
            soundPlaying = ""
            muteAll()


if __name__ == "__main__":
    start()
