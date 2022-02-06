
from tkinter import Tk,Frame,ttk,Label,Text,Button,PhotoImage,VERTICAL,Scrollbar,END,Toplevel,StringVar
import sqlite3
import os
from random import randint
import keyboard
from threading import Thread
from time import sleep

class GUI(Frame):
    def __init__(self,parent):
        self.parent = parent

        self.variables()
    def variables(self):
        self.screen_resolition = "630x295"
        self.add_frame = Frame(self.parent)
        self.add_frame_for_treeview = Frame(self.parent)
        self.database = database
        self.database.create_database()
        self.st1 = StringVar()
        self.st2 = StringVar()
        self.st3 = StringVar()

        self.parent.geometry(self.screen_resolition)
        
        self.open_add_page()

    def open_add_page(self):
        self.delete_frames()
        self.add_frame.place(x=0,y=0)
        self.add_frame_for_treeview.place(x=5,y=60)
        self.text_label = Label(self.add_frame,text="Word",height=1, width=10)
        self.text_label.grid(row=0,column=0,padx=3,pady=3)
        self.text_mean_label = Label(self.add_frame,text="Word Mean",height=1, width=20)
        self.text_mean_label.grid(row=0,column=1,padx=3,pady=3)
        self.text_example_sentence_label = Label(self.add_frame,text="Using the word in a sentence",height=1, width=30)
        self.text_example_sentence_label.grid(row=0,column=2,padx=3,pady=3)

        self.text = Text(self.add_frame,height=1, width=10)
        self.text.grid(row=1,column=0,padx=3,pady=3)
        self.text_mean = Text(self.add_frame,height=1, width=20)
        self.text_mean.grid(row=1,column=1,padx=3,pady=3)
        self.text_example_sentence = Text(self.add_frame,height=1, width=30)
        self.text_example_sentence.grid(row=1,column=2,padx=3,pady=3)
        self.text_add = Button(self.add_frame,text="Add",font=("Helvatica",8),command=self.write_database)
        self.text_add.grid(row=1,column=3,columnspan=1,padx=3,pady=3)
        self.text_random = Button(self.add_frame,text="Get Word",font=("Helvatica",8),command=self.lets_learn)
        self.text_random.grid(row=1,column=4,columnspan=1,padx=3,pady=3)


        columns = ('word', 'word_mean', 'word_example_sentence')

        self.tree = ttk.Treeview(self.add_frame_for_treeview, columns=columns, show='headings')

        self.tree.heading('word', text='Word')
        self.tree.heading('word_mean', text='Word Mean')
        self.tree.heading('word_example_sentence', text='Example')
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.column("word", anchor="center") 
        self.tree.column("word_mean", anchor="center") 
        self.tree.column("word_example_sentence", anchor="center") 

        for word in self.database.read_database():
            self.tree.insert('', END, values=word)

        scrollbar = Scrollbar(self.add_frame_for_treeview, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

    def delete_frames(self):
        self.add_frame.place_forget()
        self.add_frame_for_treeview.place_forget()
    def write_database(self):
        word = self.text.get("1.0","end")
        mean = self.text_mean.get("1.0","end")
        example = self.text_example_sentence.get("1.0","end")
        if '"' in str(example):
            example = str(example).replace('"', "")
        if not self.database.check_word(word):
            self.tree.insert('', END, values=(word,mean,example))
        self.database.write_database([word,mean,example])
        self.text.delete('1.0', END)
        self.text_mean.delete('1.0', END)
        self.text_example_sentence.delete('1.0', END)

    def lets_learn(self):
        self.top= Toplevel(self.parent)
        self.top.title("Lets learn")
        self.top.geometry("800x160")
        self.label1= Label(self.top,textvariable = self.st1,font=("Helvatica",15))
        self.label1.place(x=20,y=20)
        self.label2= Label(self.top,textvariable = self.st2,font=("Helvatica",15))
        self.label2.place(x=20,y=60)
        self.label3= Label(self.top,textvariable = self.st3,font=("Helvatica",15))
        self.label3.place(x=20,y=100)
        thread = Thread(target = self.get_random_word )
        thread.start()
    def get_random_word(self):
        exit = False
        word = self.database.read_database()
        space_counter = 0
        begin = True
        while not exit:
            if (space_counter == 0):
                random_word_num = randint(0,len(word)-1)
            if keyboard.is_pressed('space') or begin:
                begin = False
                if space_counter == 0:
                    self.st1.set(word[random_word_num][0])
                    self.st2.set("")
                    self.st3.set("")
                elif space_counter == 1:
                    self.st2.set(word[random_word_num][1])
                elif space_counter == 2:
                    self.st3.set(word[random_word_num][2])
                space_counter += 1
                sleep(0.2)
            if keyboard.is_pressed('escape'):
                exit = True
                self.top.destroy()
            if space_counter > 2:
                space_counter = 0




    def donothing(self):
        pass

class database:
    def create_database(path="file\\"):
        if not os.path.isdir(path):
            os.mkdir(path)

        connect = sqlite3.connect(path+"dataes.db")
        cursor = connect.cursor()
        command = '''
          CREATE TABLE IF NOT EXISTS words
          (word TEXT PRIMARY KEY, 
          mean TEXT,
          example_sentence TEXT)
          '''
        cursor.execute(command)
        connect.commit()
        connect.close()
        

    def write_database(text,path="file\\"):
        connect = sqlite3.connect(path+"dataes.db")
        cursor = connect.cursor()
        command = '''
        INSERT OR IGNORE INTO words (word, mean, example_sentence) VALUES ('{0}', '{1}', '{2}')
          '''.format(text[0],text[1],text[2])
        cursor.execute(command)
        connect.commit()
        connect.close()
    def read_database(path="file\\"):
        connect = sqlite3.connect(path+"dataes.db")
        cursor = connect.cursor()
        command = "SELECT * from words"
        result = cursor.execute(command).fetchall()
        connect.commit()
        connect.close()
        return result
    def check_word(word,path="file\\"):
        connect = sqlite3.connect(path+"dataes.db")
        cursor = connect.cursor()
        command = "SELECT * from words"
        result = cursor.execute(command).fetchall()
        connect.commit()
        connect.close()
        for i in result:
            if word in i:
                return True
        return False







if __name__ == "__main__":
    root = Tk()
    sinif = GUI(root)
    root.mainloop()