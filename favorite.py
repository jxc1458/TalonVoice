from collections import defaultdict
import itertools
import math
from typing import Dict, List, Iterable, Set, Tuple, Union

from talon import Module, Context, actions, imgui, Module, registry, ui, app, speech_system
from talon.grammar import Phrase

mod = Module()
setting_command_history_size = mod.setting("command_history_size", int, default=50)
setting_command_history_display = mod.setting(
    "command_history_display", int, default=10
)

hist_more = False
history = []
fav1 = "1.)"
fav2 = "2.)"
fav3 = "3.)"
fav4 = "4.)"
fav5 = "5.)"

def parse_phrase(word_list):
    return " ".join(word.split("\\")[0] for word in word_list)


def on_phrase(j):
    global history

    try:
        val = parse_phrase(getattr(j["parsed"], "_unmapped", j["phrase"]))
    except:
        val = parse_phrase(j["phrase"])

    if val != "":
        history.append(val)
        history = history[-setting_command_history_size.get() :]


# todo: dynamic rect?

if not history:
    prev_command= "insert command here"
else:
    prev_command=str(history[-1]) 



@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global history
    global prev_command
    global fav1
    global fav2
    global fav3
    global fav4
    global fav5
    gui.text("Favorites")
    # text = (
    #     history[:] if hist_more else history[-setting_command_history_display.get() :]
    # )
    # for line in text:
    #     gui.text(line)
    gui.line()

    
    if not history:
        prev_command= "insert command here"
    else:
        prev_command=str(history[-1]) 

    gui.button(fav1)
    gui.button(fav2)
    gui.button(fav3)
    gui.button(fav4)
    gui.button(fav5)
    gui.line()
    gui.text("loaded command")
    gui.text(prev_command)
    
    gui.spacer()
    if gui.button("close"):
        gui.hide()


speech_system.register("phrase", on_phrase)


@mod.action_class
class Actions:
    def favorites_toggle():
        """Toggles viewing the history"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def store_fav1():
        """stores prev command in fav1"""
        global history
        global prev_command
        global fav1
        fav1 = "1.)" + prev_command
    def store_fav2():
        """stores prev command in fav2"""
        global history
        global prev_command
        global fav2
        fav2 = "2.)" + prev_command
    def store_fav3():
        """stores prev command in fav1"""
        global history
        global prev_command
        global fav3
        fav3 = "3.)" + prev_command
    def store_fav4():
        """stores prev command in fav1"""
        global history
        global prev_command
        global fav4
        fav4 = "4.)" + prev_command
    def store_fav5():
        """stores prev command in fav1"""
        global history
        global prev_command
        global fav5
        fav5 = "5.)" + prev_command                        
    def favorites_enable():
        """Enables the history"""
        gui.show()

    def favorites_disable():
        """Disables the history"""
        gui.hide()

    def favorites_clear():
        """Clear the history"""
        global history
        history = []

    def favorites_more():
        """Show more history"""
        global hist_more
        hist_more = True

    def favorites_less():
        """Show less history"""
        global hist_more
        hist_more = False
