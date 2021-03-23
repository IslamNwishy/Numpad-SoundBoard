import sys
sys.path.append('..')
from os import listdir, mkdir
from os.path import isfile, join, exists, isdir
import tkinter as tk
from tkinter.ttk import Button, Style
from functools import partial
from typing import Text
from pygame import mixer
import keyboard
from ctypes import WinDLL


class SoundBoard(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        self.soundPlaying = ""
        self.Keys = [82, 79, 80, 81, 75, 76,
                     77, 71, 72, 73]  # numpad codes 0-9
        self.user32 = WinDLL('user32')  # to check on the numlock state
        self.profiles = {}
        self.ProfileNum = 0
        self.path = "sounds/"
        self.savedBtns = {}
        self.start()

    # get all files in sounds directory

    def get_files(self):
        keyboard.hook(self.print_pressed_keys)
        path = self.path
        if not exists(path):
            mkdir(path)
        self.profileNames = [f for f in listdir(path) if isdir(join(path, f))]
        if len(self.profileNames) > 0:
            for i in self.profileNames:
                newpath = join(path, i)
                self.profiles[i] = [
                    f for f in listdir(newpath) if isfile(join(newpath, f))]
            self.path = join(path, self.profileNames[0] + "/")

        else:
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            self.profileNames = ["Sounds"]
            self.profiles = {self.profileNames[0]: onlyfiles}

    def print_pressed_keys(e):
        print(e)

    def start(self):

        mixer.init()
        self.get_files()

        self.create_widgets()

    def create_widgets(self):
        style = Style()
        style.configure('TButton', font=('calibri', 10),
                        borderwidth='4')

        quit = Button(self, text="QUIT", style='TButton',
                      command=self.master.destroy)
        stat = tk.Label(
            self, text="Use Numlock to enable and disable the board")
        stat.pack(side=tk.BOTTOM)
        quit.pack(side=tk.BOTTOM, padx=10, pady=10, expand=1, fill=tk.X)
        self.savedBtns["numState"] = stat

        if len(self.profiles) > 1:
            controls = tk.LabelFrame(
                self, text="Controls", relief=tk.GROOVE, bd=2)
            controls.pack(side=tk.TOP, expand=1,
                          fill=tk.BOTH, padx=10, pady=20)
            nextbtn = Button(controls, text="Next Profile", style='TButton',
                             command=partial(self._profileControl, True))
            nextbtn.pack(side=tk.RIGHT, padx=10, pady=5, expand=1)
            prevbtn = Button(controls, text="Prev Profile", style='TButton',
                             command=partial(self._profileControl, False))
            prevbtn.pack(side=tk.LEFT, padx=10, pady=10, expand=1)

        self.create_buttons()

    def create_buttons(self):
        keyboard.unhook_all()
        self.mapHotkeys()
        SoundFiles = self.profiles[self.profileNames[self.ProfileNum]]
        self.label_frame = tk.LabelFrame(
            self, text=self.profileNames[self.ProfileNum], relief=tk.GROOVE, bd=2)
        self.label_frame.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)
        if len(SoundFiles) <= 0:
            nofile = tk.Label(
                self.label_frame, text="This profile is empty. Add sound in the profile folder and try again")
            nofile.pack()

        for index, val in enumerate(SoundFiles):
            if index == 9:  # the 9 numbers are mapped
                break
            key = index + 1
            keyboard.hook_key(self.Keys[key], partial(self.key_pressed, val))

            btn = Button(self.label_frame, text=str(key) + "- " + val.split('.', 1)[0], style='TButton', command=partial(
                self.play, (self.path + val)))
            btn.pack(side=tk.TOP, padx=10, pady=10, expand=1)

    def update_window(self):
        self.label_frame.pack_forget()
        self.create_buttons()

    def play(self, path):
        mixer.music.load(path)
        mixer.music.play()

    def muteAll(self, e):
        if e.is_keypad:
            mixer.music.stop()

    def mapHotkeys(self):
        keyboard.hook_key(self.Keys[0], self.muteAll)
        keyboard.hook_key('+', partial(self.profileConrol, True))
        keyboard.hook_key('-', partial(self.profileConrol, False))
        keyboard.add_hotkey("numlock", self.numUpdate, args=[
                            self.savedBtns["numState"]])

    def numUpdate(self, stat):
        numlock = self.user32.GetKeyState(0x90)
        if not numlock:
            stat.configure(text="OFF", fg="red")
        else:
            stat.configure(text="ON", fg="green")

    def _profileControl(self, isNext):
        if isNext:
            self.ProfileNum += 1
            self.ProfileNum %= len(self.profiles)

        else:
            self.ProfileNum -= 1
            self.ProfileNum %= len(self.profiles)

        self.path = join(
            "sounds/", self.profileNames[self.ProfileNum] + "/")
        self.update_window()

    def profileConrol(self, isNext, e):
        if len(self.profiles) > 1 and e.is_keypad and keyboard.is_pressed(e.name):
            self._profileControl(isNext)

    def key_pressed(self, sound, e):
        numlock = self.user32.GetKeyState(0x90)
        if not numlock and e.is_keypad and keyboard.is_pressed(e.name):
            if sound != self.soundPlaying or not mixer.music.get_busy():
                self.play(self.path + sound)
                self.soundPlaying = sound
            else:
                self.soundPlaying = ""
                self.muteAll(e)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SoundBoard")
    root.minsize(250, 100)
    SoundBoard(root)
    root.mainloop()
