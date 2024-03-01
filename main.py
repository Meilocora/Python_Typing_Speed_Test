import random
from tkinter import *
import math
from contents import contents
# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Courier"
COUNT = 60
timer = None
random_text = ""

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def start_test():
    style_user_input()
    reset_values()
    count_down(COUNT)
    global random_text
    random_text = random.choice(contents)
    example_text.insert("1.0", random_text)

def stop_timer():
    global timer
    window.after_cancel(timer)
    unstyle_user_input()

def style_user_input():
    user_text.config(state="normal", bg="#BEFFA8", fg="#282F4F", borderwidth=4)
    user_text.focus()

def unstyle_user_input():
    user_text.config(state="disabled", bg="white", fg="black", borderwidth=2)

def reset_values():
    global timer
    if timer:
        window.after_cancel(timer)
    example_text.delete("1.0", "end")
    canvas.itemconfig(wpm_count, text="0")
    canvas.itemconfig(correct_count, text="0")
    user_text.delete(0, "end")


def count_down(COUNT):
    count_min = math.floor(COUNT/60)
    count_sec = COUNT % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if COUNT > 0:
        global timer
        timer = window.after(1000, count_down, COUNT-1)
    else:
        show_final_score()
        unstyle_user_input()

def callback(var):
   content= var.get()
   check_userinput(content)

def check_userinput(content):
    start = 0
    end = 0
    correct_counter = 0
    for num in range(len(content.split())):
        start, end = get_indeces(num)
        example_text.tag_add("focused", start, end)
        if content.split()[num] == random_text.split()[num]:
            example_text.tag_add("correct", start, end)
            correct_counter += 1
        if len(content.split()[num]) == len(random_text.split()[num]) and content.split()[num] != random_text.split()[num]:
            example_text.tag_add("wrong", start, end)
        if num-1 != -1 and content.split()[num-1] != random_text.split()[num-1]:
            start_before, end_before = get_indeces(num-1)
            example_text.tag_add("wrong", start_before, end_before)
    canvas.itemconfig(correct_count, text=correct_counter)
    seconds = int(timer.split("#")[1])
    if correct_counter != 0:
        wpm = int(correct_counter / (seconds / 60))
    else:
        wpm = 0
    canvas.itemconfig(wpm_count, text=wpm)
    if len(content.split()) == len(random_text.split()):
        stop_timer()

def get_indeces(number):
    start = 0
    for num in range(number):
        start += len(random_text.split()[num]) + 1
    end = start + len(random_text.split()[number])
    return [f"1.{start}", f"1.{end}"]

def show_final_score():
    correct_counter = int(canvas.itemcget(correct_count, "text"))
    wpm_final = int(correct_counter / (COUNT/60))
    canvas.itemconfig(wpm_count, text=wpm_final)
    return

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Typing Speed Tester")
window.config(padx=30, pady=30)

main_label = Label(text="Typing Speed Tester", font=(FONT_NAME, 35, "bold"), pady=20)
main_label.grid(row=0, column=1)

canvas = Canvas(width=800, height=100)
correct_label = canvas.create_text(150, 20, text="Correct", font=(FONT_NAME, 24, "bold"))
correct_count = canvas.create_text(150, 55, text="0", font=(FONT_NAME, 24, "bold"))
timer_label = canvas.create_text(400, 20, text="Time left", font=(FONT_NAME, 24, "bold"))
timer_text = canvas.create_text(400, 55, text="00:00", font=(FONT_NAME, 24, "bold"))
wpm_label = canvas.create_text(650, 20, text="WPM", font=(FONT_NAME, 24, "bold"))
wpm_count = canvas.create_text(650, 55, text="0", font=(FONT_NAME, 24, "bold"))
canvas.grid(column=0, row=1, columnspan=3)

start_btn = Button(text="Start", highlightthickness=0, width=10, font=(FONT_NAME, 16, "bold"), command=start_test)
start_btn.grid(column=1, row=2)

spacer1 = Label(text='', padx=20)
spacer1.grid(row=3, column=0, columnspan=3)

example_text = Text(width=80, height=10, bg="grey", fg="white", font=(FONT_NAME, 12, "normal"), wrap="word")
example_text.grid(column=0, row=4, columnspan=3)

spacer2 = Label(text='', padx=20)
spacer2.grid(row=5, column=0, columnspan=3)

var = StringVar()
var.trace("w", lambda name, index,mode, var=var: callback(var))
user_text = Entry(textvariable=var, width=80, font=(FONT_NAME, 12, "bold"), state="disabled")
user_text.grid(column=0, row=6, columnspan=3)

# ---------------------------- TAGS ------------------------------- #
example_text.tag_configure('focused', font=(FONT_NAME, 12, "bold"), foreground="white")
example_text.tag_configure('wrong', foreground="#F72F2F")
example_text.tag_configure('correct', foreground="#17F428")

window.mainloop()