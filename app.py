import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog

import time
timestr = time.strftime("%Y%m%d- %H%M%S")

from spacy_summarization import text_summarizer
from nltk_summarization import nltk_summarizer
from glove_summarization import summarize
from Text_Summarization.spacy2 import NamedEntityReco

from bs4 import BeautifulSoup
from urllib.request import urlopen

window = Tk()
window.title("Summaryzer GUI")
window.geometry('700x500')

# Style
style = ttk.Style(window)

style.configure('lefttab.TNotebook', tabposition='wn')

# Tabs
tab_control = ttk.Notebook(window, style='lefttab.TNotebook')

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)
tab6 = ttk.Frame(tab_control)


# Add tabs to notebook
tab_control.add(tab1, text=f'{"Home":^20s}')
tab_control.add(tab2, text=f'{"File":^20s}')
tab_control.add(tab3, text=f'{"URL":^20s}')
tab_control.add(tab4, text=f'{"Comparer":^20s}')
tab_control.add(tab5, text=f'{"About":^20s}')
tab_control.add(tab6, text=f'{"NER":^20s}')

# Labels
label1 = Label(tab1, text="Summaryzer", padx=5, pady=5)
label1.grid(row=0, column=0)
label1 = Label(tab2, text="File Processing", padx=5, pady=5)
label1.grid(row=0, column=0)
label1 = Label(tab3, text="URL", padx=5, pady=5)
label1.grid(row=0, column=0)
label1 = Label(tab4, text="Comparer", padx=5, pady=5)
label1.grid(row=0, column=0)
label1 = Label(tab5, text = "About", padx=5, pady=5)
label1.grid(row=0, column=0)
label1 = Label(tab6, text = "Named Entity Recognition", padx=5, pady=5)
label1.grid(row=0, column=0)

tab_control.pack(expand=1, fill="both")

# Functions
def get_summary():
    raw_text = entry.get('1.0', tk.END)
    final_text = summarize(raw_text)
    print(final_text)
    result = '\nSummary: {}'.format(final_text)
    tab1_display.insert(tk.END,result)

def save_summary():
    raw_text = entry.get('1.0', tk.END)
    final_text = summarize(raw_text)
    file_name = 'Yoursummary' + timestr + '.txt'
    with open(file_name, "w") as f:
        f.write(final_text)
    result = '\nName Of File: {}, \nSummary: {}'.format(file_name, final_text)
    tab1_display.insert(tk.END, result)

def ner():
    ner_objects = NamedEntityReco('Text_Summarization/CV.pdf')
    tab6_display.insert(tk.END, ner_objects)

def clear_text():
    entry.delete('1.0', tk.END)

def clear_display_result():
    tab1_display.delete('1.0', tk.END)

# Open files Functions
def open_files():
    file1 = tkinter.filedialog.askopenfilename(filetype=(('Text Files', ".txt"), ('All Files', "*")))
    read_text = open(file1).read()
    displayed_file.insert(tk.END, read_text)

def get_file_summary():
    raw_text = displayed_file.get('1.0', tk.END)
    final_text = summarize(raw_text)
    result = '\nSummary: {}'.format(final_text)
    tab2_display.insert(tk.END, result)

def clear_text_file():
    displayed_file.delete('1.0',tk.END)

def clear_text_results():
    tab2_display.delete('1.0', tk.END)


# URL Functions
def get_text():
	raw_text = str(url_entry.get())
	page = urlopen(raw_text)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
	url_display.insert(tk.END, fetched_text)

def get_url_summary():
	raw_text = url_display.get('1.0', tk.END)
	final_text = summarize(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab3_display.insert(tk.END, result)

def clear_url_entry():
    url_entry.delete( 0, tk.END)

def clear_url_display():
    tab3_display.delete('1.0', tk.END)


# COMPARER FUNCTIONS

def use_spacy():
	raw_text = str(entry1.get('1.0', tk.END))
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSpacy Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END, result)


def use_nltk():
	raw_text = str(entry1.get('1.0', tk.END))
	final_text = nltk_summarizer(raw_text)
	print(final_text)
	result = '\nNLTK Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END, result)


def use_glove():
	raw_text = str(entry1.get('1.0', tk.END))
	final_text = summarize(raw_text)
	print(final_text)
	result = '\nGlove Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END, result)

def clear_compare_text():
	entry1.delete('1.0', END)

def clear_compare_display_result():
	tab1_display.delete('1.0', END)


# Main home Tab
l1 = Label(tab1, text="Enter Text To Summarize", padx=5, pady=5)
l1.grid(row=1,column=0)
entry = ScrolledText(tab1, height=10)
entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Buttons
button1 = Button(tab1, text="Reset", command=clear_text, width=12, bg="green", fg="black")
button1.grid(row=4, column=0, padx=10, pady=10)
button2 = Button(tab1, text="Summarize", command=get_summary, width=12, bg="green", fg="black")
button2.grid(row=4, column=1, padx=10, pady=10)
button3 = Button(tab1, text="Clear Result", command=clear_display_result, width=12, bg="green", fg="black")
button3.grid(row=5, column=0, padx=10, pady=10)
button4 = Button(tab1, text="Save", command=save_summary,width=12, bg="green", fg="black")
button4.grid(row=5, column=1, padx=10, pady=10)

# Display screen for results
tab1_display = ScrolledText(tab1, height=10)
tab1_display.grid(row=7, column=0, columnspan=3, padx=5, pady=5)



# File Processing Tab
l1 = Label(tab2, text="Open File To Summarize", padx=5, pady=5)
l1.grid(row=1, column=1)
displayed_file = ScrolledText(tab2, height=10)
displayed_file.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Buttons
b1 = Button(tab2, text="Open File", command=open_files,width=12, bg="green", fg="black")
b1.grid(row=3, column=0, padx=10, pady=10)
b2 = Button(tab2, text="Reset", command=clear_text_file,width=12, bg="green", fg="black")
b2.grid(row=3, column=1, padx=10, pady=10)
b3 = Button(tab2, text="Summarize", command=get_file_summary,width=12, bg="green", fg="black")
b3.grid(row=3, column=2, padx=10, pady=10)
b4 = Button(tab2, text="Clear results", command=clear_text_results,width=12, bg="green", fg="black")
b4.grid(row=5, column=1, padx=10, pady=10)
b5 = Button(tab2, text="Close", command=window.destroy)
b5.grid(row=5, column=2, padx=10, pady=10)

# Display screen for results
tab2_display = ScrolledText(tab2, height=10)
tab2_display.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Allows you to edit
tab2_display.config(state=NORMAL) 



# URL Tab
l1 = Label(tab3, text="Enter URL To Summarize", padx=5, pady=5)
l1.grid(row=1, column=0)

raw_entry = StringVar()
url_entry = Entry(tab3,  textvariable=raw_entry, width=50)
url_entry.grid(row=1, column=1)

# Buttons
b1 = Button(tab3, text="Reset", command=clear_url_entry,width=12, bg="green", fg="black")
b1.grid(row=4, column=0, padx=10, pady=10)
b2 = Button(tab3, text="Get Text", command=get_text,width=12, bg="green", fg="black")
b2.grid(row=4, column=1, padx=10, pady=10)
b3 = Button(tab3, text="Clear Result", command=clear_url_display,width=12, bg="green", fg="black")
b3.grid(row=5, column=0, padx=10, pady=10)
b4 = Button(tab3, text="Summarize", command=get_url_summary,width=12, bg="green", fg="black")
b4.grid(row=5, column=1, padx=10, pady=10)

# Display screen for results
url_display = ScrolledText(tab3, height=10)
url_display.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

tab3_display = ScrolledText(tab3, height=10)
tab3_display.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# COMPARER TAB
l1 = Label(tab4, text="Enter Text To Summarize")
l1.grid(row=1, column=0)

entry1 = ScrolledText(tab4, height=10)
entry1.grid(row=2, column=0, columnspan=3, padx=5, pady=3)

# BUTTONS
button1 = Button(tab4, text="Reset", command=clear_compare_text,width=12, bg='#03A9F4', fg='#fff')
button1.grid(row=4, column=0, padx=10, pady=10)

button2 = Button(tab4, text="SpaCy", command=use_spacy, width=12, bg='#03A9F4', fg='#fff')
button2.grid(row=4, column=1, padx=10, pady=10)

button3 = Button(tab4, text="Clear Result",command=clear_compare_display_result, width=12, bg='#03A9F4', fg='#fff')
button3.grid(row=5, column=0, padx=10, pady=10)

button4 = Button(tab4, text="NLTK", command=use_nltk, width=12, bg='#03A9F4', fg='#fff')
button4.grid(row=4, column=2, padx=10, pady=10)

button4 = Button(tab4, text="Glove", command=use_glove, width=12, bg='#03A9F4', fg='#fff')
button4.grid(row=5, column=1, padx=10, pady=10)



# variable = StringVar()
# variable.set("SpaCy")
# choice_button = OptionMenu(tab4, variable, "SpaCy", "Gensim", "Sumy", "NLTK")
# choice_button.grid(row=6, column=1)


# Display Screen For Result
tab4_display = ScrolledText(tab4, height=15)
tab4_display.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

# NER TAB
l1 = Label(tab6, text="Open File To Summarize", padx=5, pady=5)
l1.grid(row=1, column=1)

b1 = Button(tab6, text="Get NER", command=ner,width=12, bg="green", fg="black")
b1.grid(row=3, column=0, padx=10, pady=10)
b2 = Button(tab6, text="Reset", command=clear_text_file,width=12, bg="green", fg="black")
b2.grid(row=3, column=1, padx=10, pady=10)
b4 = Button(tab6, text="Clear results", command=clear_text_results,width=12, bg="green", fg="black")
b4.grid(row=5, column=1, padx=10, pady=10)
b5 = Button(tab6, text="Close", command=window.destroy)
b5.grid(row=5, column=2, padx=10, pady=10)

tab6_display = ScrolledText(tab6, height=10)
tab6_display.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Allows you to edit
tab6_display.config(state=NORMAL) 


# About TAB
about_label = Label(
    tab5, text=" ML Project \n Aditya Singh A-09 \n Prathamesh Chaskar A-10\n Shruti Rathod A-32", pady=5, padx=5)
about_label.grid(column=0, row=1)


window.mainloop()
