my_listbox.pack_forget()
            t = i['top']
            my_label = Label(top, text = t)
            my_label.pack()
            def answer():
                my_label.pack_forget()
                button2.pack_forget()
                label2 = Label(top,text = i['bottom'])
                label2.pack()
            button2 = Button(top, text = "Answer", command = answer)
            button2.pack()