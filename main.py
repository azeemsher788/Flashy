from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
BIG_FONT = ("Bungee", 40, 'normal')
SMALL_FONT = ("Poppins", 25, 'normal')
word_index = -1
card_to_shift = "after#0"
current_card = {}
# TODO 〰〰〰〰〰〰〰〰〰〰 Read file 〰〰〰〰〰〰〰〰〰〰
try:
    data_file = pd.read_csv("data/to_learn.csv")
except FileNotFoundError:
    original_record = pd.read_csv("data/french_words.csv")
    to_learn = original_record.to_dict(orient="records")
else:
    to_learn = data_file.to_dict(orient="records")


# TODO 〰〰〰〰〰〰〰〰〰〰 Shift card 〰〰〰〰〰〰〰〰〰〰

def new_word():
    global current_card, flipping_timer
    window.after_cancel(flipping_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(image_item, image=card_front_img)
    canvas.itemconfig(heading_text, text="French", fill="Black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="Black")
    flipping_timer = window.after(3000, flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(image_item, image=card_back_img)
    canvas.itemconfig(heading_text, text="English", fill="White")
    canvas.itemconfig(word_text, text=current_card["English"], fill="White")


def saving_progress():
    to_learn.remove(current_card)
    df = pd.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    new_word()


# TODO 〰〰〰〰〰〰〰〰〰〰 UI setup 〰〰〰〰〰〰〰〰〰〰
window = Tk()
window.minsize(width=800, height=500)
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=20)
flipping_timer = window.after(3000, flip_card)

right_logo_img = PhotoImage(file="images/right.png")
wrong_logo_img = PhotoImage(file="images/wrong.png")
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
image_item = canvas.create_image(400, 263)
heading_text = canvas.create_text(400, 150, font=SMALL_FONT, text="French")
word_text = canvas.create_text(400, 280, font=BIG_FONT)
canvas.grid(column=0, row=0, columnspan=5)

wrong_button = Button(
    window,
    bg=BACKGROUND_COLOR,
    activebackground=BACKGROUND_COLOR,
    text="Generate",
    image=wrong_logo_img,
    highlightthickness=0,
    borderwidth=0
)
wrong_button.grid(column=1, row=2)
right_button = Button(
    window,
    bg=BACKGROUND_COLOR,
    activebackground=BACKGROUND_COLOR,
    text="Generate",
    image=right_logo_img,
    highlightthickness=0,
    borderwidth=0
)
right_button.grid(column=3, row=2)
# Actions
new_word()
right_button["command"] = saving_progress
wrong_button["command"] = new_word
window.mainloop()
