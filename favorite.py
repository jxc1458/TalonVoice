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
prev_command = str(history[-1])

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

@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global history
    gui.text("Favorites")
    gui.line()
    text = (
        history[:] if hist_more else history[-setting_command_history_display.get() :]
    )
    for line in text:
        gui.text(line)

    gui.line()
    gui.text(history[-1])
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
