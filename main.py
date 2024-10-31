BACKGROUND_COLOR = "#B1DDC6"

from tkinter import *
from tkinter import messagebox
import pandas
import random


word_count,right_words,wrong_words = 0,0,0
toggle = True
iter2 = None
iter3 = None
iter4 = None


def reset_game():
    global iter2, iter3, iter4, word_count , right_words,wrong_words

    random.shuffle(list_records)
    screen.after_cancel(str(iter2))
    screen.after_cancel(str(iter3))
    screen.after_cancel(str(iter4))
    right_button.config(state='disabled')
    wrong_button.config(state='disabled')
    flashcard.itemconfig(title, text="Title", font=["Times New Roman", 40, 'bold'])
    flashcard.itemconfig(word, text='Word', font=['Arial', 25, 'italic'])
    messagebox.showinfo(title='Info', message='Shuffling')
    flashcard.itemconfig(done_word, text=f'✅:{right_words} words')
    flashcard.itemconfig(learn, text=f'❌:{wrong_words} words')
    start_button.config(image=start)

def right_func():
    global right_words
    right_words+=1
    flashcard.itemconfig(done_word,text=f'✅:{right_words} words')
    starting()
def wrong_func():
    global wrong_words
    wrong_words+=1
    flashcard.itemconfig(learn,text=f'❌:{wrong_words} words')
    starting()


def start_or_stop():
    global toggle,word_count,right_words,wrong_words
    if toggle:
        starting()
        start_button.config(image=reset)
        toggle = False
    else:
        word_count, right_words, wrong_words = 0, 0, 0
        reset_game()

        toggle = True


def starting():
    global word_count, iter2, iter3

    right_button.config(state='normal')
    wrong_button.config(state='normal')

    screen.after_cancel(str(iter2))
    screen.after_cancel(str(iter3))
    screen.after_cancel(str(iter4))
    change_word()


def change_word():
    global word_count, iter2
    word_count += 1
    flashcard.itemconfig(background, image=image_front)
    flashcard.itemconfig(title, text="French")
    try:
        flashcard.itemconfig(word, text=list_records[word_count]['French'])
        iter2 = screen.after(3000, func=flip_card)
    except:
        global right_words,wrong_words,toggle
        toggle=not(toggle)
        random.shuffle(list_records)
        word_count = 0
        messagebox.showinfo(title='Session ends',message=f"You know:{right_words} words\nYou need to learn:{wrong_words}word\n")
        right_words,wrong_words=0,0
        reset_game()

def flip_card():
    global word_count, iter3
    flashcard.itemconfig(background, image=image_back)
    flashcard.itemconfig(title, text="English")
    flashcard.itemconfig(word, text=list_records[word_count]['English'])
    iter3 = screen.after(3000, flip_back)


def flip_back():
    global word_count, iter4
    flashcard.itemconfig(background, image=image_front)
    flashcard.itemconfig(title, text="French")
    flashcard.itemconfig(word, text=list_records[word_count]['French'])
    iter4 = screen.after(3000, flip_card)


screen = Tk()
bg = PhotoImage(file="images/card_back.png")
screen.config(bg=BACKGROUND_COLOR)
screen.minsize(width=900, height=750)
screen.configure(pady=50, padx=50)
#All images
image_back = PhotoImage(file='images/card_back.png')
image_front = PhotoImage(file='images/card_front.png')
right = PhotoImage(file='images/right.png')
wrong = PhotoImage(file='images/wrong.png')
start = PhotoImage(file='images/button_final.png')
reset = PhotoImage(file='images/file.png')
#--------------------------------------------------
french_words = pandas.read_csv("data/french_words.csv")
list_records = french_words.to_dict(orient='records')
random.shuffle(list_records)

flashcard = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
background = flashcard.create_image(400, 263, image=image_front)
title = flashcard.create_text(400, 160, text="Title", font=["Times New Roman", 40, 'bold'])
word = flashcard.create_text(390, 270, text='word', font=['Arial', 25, 'italic'])
done_word=flashcard.create_text(650,450,text=f'✅:{right_words} words',font=['Arial', 25, 'bold'])
learn=flashcard.create_text(200,450,text=f'❌:{wrong_words} words',font=['Arial', 25, 'bold'])
flashcard.grid(row=0, column=0, columnspan=3)

#Buttons
right_button = Button(image=right, bg='Green', padx=50, command=right_func, state='disabled')
right_button.grid(row=1, column=2)

start_button = Button(image=start, bg='black', padx=0, command=start_or_stop)
start_button.grid(row=1, column=1)

wrong_button = Button(image=wrong, bg='Red', padx=50, command=wrong_func, state='disabled')
wrong_button.grid(row=1, column=0)

#-------------------------------------------------------------UI DONE--------------------------
screen.mainloop()
