from tkinter import *
from tkinter import messagebox
from testmanager import TestManager
import string

WORDLIST_FILENAME = "words.txt"
timer = None
starting = True
chars = 0
seconds_passed = 0
typed_words = []


# ============================ LOADING WORDS ========================= #

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


words = load_words()

test_manager = TestManager(words)

text = test_manager.choosen_words()


# =========================== COUNTDOWN MECHANISM ======================= #

def countdown(count):
    global timer, seconds_passed, chars, canvas_text
    if count > 0:
        time.config(text=count)
        seconds_passed += 1
        cpm_count, wpm_count = test_manager.calculate_cpm_wpm(chars, seconds_passed)
        cpm.config(text=f"{cpm_count}")
        wpm.config(text=f"{wpm_count}")
        timer = window.after(1000, countdown, count - 1)
    else:
        time.config(text=count)
        correct_cpm, correct_wpm = test_manager.calculate_speed(typed_words, text.split(), chars)
        canvas.itemconfig(canvas_text, text=f"Your correct CPM if {correct_cpm} and your averge WPM is {correct_wpm}")
        canvas.yview_moveto('0.3')
        user_input.delete("1.0", END)
        user_input.config(state="disabled")


# =========================== ADDING TEXT TO CANVAS ===================== #

def add_text():
    global text
    text = test_manager.choosen_words()
    canvas.itemconfig(canvas_text, text=text)


# ================================ KEYS FUNCTIONS =========================== #

def restart():
    global starting, chars, typed_words, seconds_passed
    canvas.yview_moveto("0.0")
    user_input.config(state="normal")
    user_input.delete("1.0", END)
    user_input.insert("1.0", "                         ")
    add_text()
    starting = True
    cpm.config(text="0")
    wpm.config(text="0")
    chars = 0
    seconds_passed = 0
    typed_words = []

    if timer is not None:
        window.after_cancel(timer)
        time.config(text="60")



def space_pressed(e):
    word = user_input.get('0.0', END)
    typed_words.append(word.strip())
    user_input.delete("1.0", END)
    user_input.insert("1.0", "                         ")


def enter_pressed(e):
    canvas.yview_scroll(number=2, what="units")


def any_key(e):
    global starting, chars
    if starting:
        starting = False
        countdown(60)
    if e.char in string.ascii_lowercase:
        chars += 1


# ================================= UI SETUP =============================== #

window = Tk()
window.title("Typing Speed Test")
window.config(padx=20, pady=20)

# Top Row
cpm_label = Label(text="CPM :  ", font=("Arial", 20, "normal"))
cpm = Label(text="0", background="white", font=("Arial", 20, "normal"))
wpm_label = Label(text="WPM :  ", font=("Arial", 20, "normal"))
wpm = Label(text="0", background="white", font=("Arial", 20, "normal"))
time_label = Label(text="Time Left : ", font=("Arial", 20, "normal"))
time = Label(text="60", background="white", font=("Arial", 20, "normal"))
restart = Button(text="Restart", font=("Arial", 20, "normal"), command=restart)

cpm_label.grid(row=0, column=0)
cpm.grid(row=0, column=1)
wpm_label.grid(row=0, column=2)
wpm.grid(row=0, column=3)
time_label.grid(row=0, column=4)
time.grid(row=0, column=5)
restart.grid(row=0, column=6)

# Text Canvas
canvas = Canvas(width=1000, height=150, background="white")
canvas.grid(row=1, columnspan=7, column=0)
canvas_text = canvas.create_text(500, 80, text=text, font=("Courier", 27, "normal"), width=1000)
scroll_y = Scrollbar(orient="vertical", command=canvas.yview)
scroll_y.grid(row=1, column=7, sticky="ns")
canvas.configure(yscrollcommand=scroll_y.set)
canvas.configure(scrollregion=canvas.bbox("all"))
canvas.yview_moveto("0.0")

# Text Entry
user_input = Text(height=1, font=("Courier", 30, "normal"), width=50)
user_input.insert("1.0", "                         ")
user_input.grid(row=2, columnspan=7, column=0)

# Key events binding

window.bind("<space>", space_pressed)
window.bind("<Return>", enter_pressed)
window.bind("<Key>", any_key)
messagebox.showinfo("How to use", "always use space between words and use enter just to scroll the text")

window.mainloop()
