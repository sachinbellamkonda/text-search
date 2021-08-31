import Query
import Indexer
import main
from tkinter import *

class tab(Frame):
    text_input=None
    phrase_input=None
    result_output=None
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        Frame.__init__(self, master)
        self.init_window()
        self.master = master

    def init_window(self):

        self.master.title("Text-Search-Engine")
        self.pack(fill=BOTH, expand=1)

        text_query_label = Label(self, text="Text Query")
        self.text_query_entry = Entry(self)

        text_query_label.grid(row=0, column=1)
        self.text_query_entry.grid(row=0, column=2)

        results_label_text = Label(self, text="Results")
        self.text_results_entry = Text(self, height=10, width=100)

        results_label_text.grid(row=2, column=1)
        self.text_results_entry.grid(row=2, column=2)

        phrase_query_label = Label(self, text="Phrase Query")
        self.phrase_query_entry = Entry(self)

        phrase_query_label.grid(row=4, column=1)
        self.phrase_query_entry.grid(row=4, column=2)

        results_label_phrase=Label(self,text="Results")
        self.phrase_results_entry=Text(self,height=10,width=100)

        results_label_phrase.grid(row=5,column=1)
        self.phrase_results_entry.grid(row=5,column=2)

        search_button1 = Button(self, text="Search", command=self.answer_text_queries)
        search_button1.grid(row=0, column=3)

        search_button2=Button(self,text='Search',command=self.answer_phrase_queries)
        search_button2.grid(row=4,column=3)

        quit_button = Button(self, text="Quit", command=self.client_exit)
        quit_button.grid(row=6, column=1)

    def answer_phrase_queries(self):
        phrase_string = self.phrase_query_entry.get()
        path_to_text_corpus =r"C:\Users\sachin\Desktop\text-search\text_corpus"
        indexer = Indexer.Indexer()
        print("Indexer object created!")
        indexer.build_index(path_to_text_corpus)
        query = Query.Query()
        results = query.phrase_query(phrase_string)
        
        results=list(results)
        #print(results)
        self.print_results_phrase_query(results)
        """count=1
        for score, file_name in results:
            print("Choice number: ", count, " --> File: ", file_name, "Score = ", score)
            count += 1
        """

    def answer_text_queries(self):
        query_string = self.text_query_entry.get()
        path_to_text_corpus =r"C:\Users\sachin\Desktop\text-search\text_corpus"
        indexer = Indexer.Indexer()
        print("Indexer object created!")
        indexer.build_index(path_to_text_corpus)
        query = Query.Query()
        #print("Query instance successfully creater!")
        results = query.text_query(query_string)
        #print("Results obtained!!")
        results = list(results)
        self.print_results_text_query(results)
        """count = 1
        for score, file_name in results:
            print("Choice number: ", count, " --> File: ", file_name, "Score = ", score)
            count += 1
        """

    def print_results_text_query(self, results):
        results_string = ""
        count = 1
        for score, file_name in results:
            results_string += "Choice number: " + str(count) + " --> File: " + file_name + " Score = " + str(score) + "\n";
            count += 1
        results_string += "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        #self.results_entry.delete(0, END)
        self.text_results_entry.insert(INSERT, results_string)
        #self.results_text.set(results_string)

    def print_results_phrase_query(self,results):
        results_string=""
        count=1
        for file in results:
            results_string+="choice number: "+str(count)+" -->file: "+file +"\n"
            count+=1
        results_string+="+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        self.phrase_results_entry.insert(INSERT,results_string)

    def client_exit(self):
        exit()