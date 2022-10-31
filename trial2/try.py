import tkinter as tk
from tkinter import *
import json
import os
from functools import partial

root = Tk()
root.title("main page")

with open("master.json", "r") as f:
    file_path = "master.json"
    if os.stat(file_path).st_size == 0:
        master_dict = {}
        with open("master.json", "w") as f:
            json.dump(master_dict,f)
    else:
        master_dict = json.loads(f.read())
# This is the big dictionary, its 'keys' are the name of sets, and the 'values' are lists
# These lists represent flashcard sets, within the lists there are questions represented by dictionaries
def open_making_window():
    top = Toplevel()
    top.title("Create flashcard set")
    mylabel = Label(top, text = "What would you like to name this set: ")
    name = Entry(top, width = 25)
    def submit_name(master_dict):
        #getting the user input for the name of the set
        Name = name.get()
        name.delete(0, END)
        with open("master.json", "r") as f:
            master = json.load(f)
            master_dict[Name] = []
            with open("master.json", "w") as x:
                json.dump(master_dict,x)
               
    action_with_arg = partial(submit_name, master_dict)
    submit = Button(top, text = "Submit", command = action_with_arg)
    mylabel.pack()
    name.pack()
    submit.pack()

def open_editting_window():
    top = Toplevel()
    top.title("Edit a flashcard set")
    my_label = Label(top, text = "Which flashcard set would you like to edit?")
    my_listbox = Listbox(top)
    x = master_dict.keys()
    for i in x:
        my_listbox.insert(END, i)
    def select():
        f_set = my_listbox.get(ANCHOR)
        top.title(f_set)
        def add():
            top = Toplevel()
            top.title("add new card")
            question_dict = {"top":0, "bottom":0, "n":0, "q":0, "EF":2.5, "y":1}
            top1 = Label(top, text = "Enter the question here")
            q = Entry(top, width = 25)
            bottom = Label(top, text = "Enter the answer here")
            a = Entry(top, width=25)
            def submit():
                question_dict["top"] = q.get()
                question_dict["bottom"] = a.get()
                master_dict[f_set].append(question_dict)
                print(master_dict[f_set])
                q.delete(0,END)
                a.delete(0,END)
                with open("master.json", "w") as x:
                    json.dump(master_dict,x)
                top.destroy()
            submit = Button(top, text = "submit", command = submit)
            top1.pack()
            q.pack()
            bottom.pack()
            a.pack()
            submit.pack()
        add_card = Button(top, text = "add card", command = add)
        def delete():
            top = Toplevel()
            top.title("delete a card")
            label = Label(top, text = "Which one would you like to delete?")
            label.pack()
            qset = master_dict[f_set]
            new_listbox = Listbox(top)
            for i in qset:
                new_listbox.insert(END, i["top"])
            new_listbox.pack()
            def select_card():
                card = new_listbox.get(ANCHOR)
                for i in qset:
                    if i["top"] == card:
                        qset.remove(i)
                with open("master.json", "w") as x:
                    json.dump(master_dict,x)
                new_listbox.delete(ANCHOR)
            button = Button(top, text = "Select", command = select_card)
            button.pack()
        delete_card = Button(top, text = "delete card", command = delete)
        add_card.pack()
        delete_card.pack()
    my_button = Button(top, text="Select", command = select)
    my_label.pack()
    my_listbox.pack(padx=15,pady=15)
    my_button.pack()

def study_mode():
    pass

myButton1 = Button(root,text="Study flashcards", height = 5, width = 25)
myButton2 = Button(root, text = "Create new flashcard set", height = 5, width = 25, command = open_making_window)
myButton3 = Button(root, text = "Edit flashcard set", height = 5, width = 25, command = open_editting_window)

myButton1.pack()
myButton2.pack()
myButton3.pack()

root.mainloop()