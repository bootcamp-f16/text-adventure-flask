import os
import sys

draw_contents = []

def clear_screen():
    os.system('clear')

def draw(contents_to_print=None):
    global draw_contents
    if contents_to_print is not None:
        draw_contents.append(contents_to_print)

def prompt():
    print("")
    return input(">>> ")

def exit(code=0):
    sys.exit(code)
