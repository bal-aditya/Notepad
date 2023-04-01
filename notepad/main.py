import re
from tkinter import *
from tkinter.ttk import *
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter.scrolledtext import ScrolledText
import sqlite3
root = Tk()
root.title('Balus Notepad')
root.resizable(0, 0)
root.iconbitmap('D:\greem.ico')
notepad = ScrolledText(root, width = 90, height = 40,bg='#e6e7f1')
fileName = ' '

conn=sqlite3.connect('todolistdb.db')
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS todotable (task text)""")
def cmdNew():    
    global fileName
    if len(notepad.get('1.0', END+'-1c'))>0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmdSave()
        else:
            notepad.delete(0.0, END)
    root.title("Notepad")

def cmdDeleteTasks():
    conn=sqlite3.connect('todolistdb.db')
    c=conn.cursor()
    c.execute('delete from todotable where rowid in (select rowid from todotable limit 1)')
    conn.commit()
    conn.close()
def cmdOpen():    
    fd = filedialog.askopenfile(parent = root, mode = 'r')
    t = fd.read()     #t is the text read through filedialog
    notepad.delete(0.0, END)
    notepad.insert(0.0, t)
    
def cmdSave():    
    fd = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt')
    if fd!= None:
        data = notepad.get('1.0', END)
    try:
        fd.write(data)
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")
     
def cmdSaveAs():     
    fd = filedialog.asksaveasfile(mode='w', defaultextension = '.txt')
    t = notepad.get(0.0, END)     
    try:
        fd.write(t.rstrip())
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")

def cmdExit():     
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        root.destroy()

def cmdCut():    
    notepad.event_generate("<<Cut>>")

def cmdCopy():     
    notepad.event_generate("<<Copy>>")

def cmdPaste():    
    notepad.event_generate("<<Paste>>")

def cmdClear():     
    notepad.event_generate("<<Clear>>")
       
def cmdFind():     
    notepad.tag_remove("Found",'1.0', END)
    find = simpledialog.askstring("Find", "Find what:")
    if find:
        idx = '1.0' 
    while 1:
        idx = notepad.search(find, idx, nocase = 1, stopindex = END)
        if not idx:
            break
        lastidx = '%s+%dc' %(idx, len(find))
        notepad.tag_add('Found', idx, lastidx)
        idx = lastidx
    notepad.tag_config('Found', foreground = 'white', background = 'blue')
    notepad.bind("<1>", click)

def click(event):     
    notepad.tag_config('Found',background='white',foreground='black')

def cmdSelectAll():    
    notepad.event_generate("<<SelectAll>>")
    
def cmdTimeDate():    
    now = datetime.now()
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    label = messagebox.showinfo("Time/Date", dtString)

def cmdAbout():     
    label = messagebox.showinfo("About Notepad", "Notepad by - \nBalu")
def cmdFont():
    font=StringVar()
    font.set("Font")
    fontmenu=OptionMenu(root,font,"Arial","Times New Roman","Courier New")
    fontmenu.pack()
def todolist():
    #conn=sqlite3.connect('todolistdb.db')
    #c=conn.cursor()
    def cmdAddTask():
        task = simpledialog.askstring("Add Task", "Enter Task:")
        if task:
            #notepad.insert(INSERT,task)
            #conn=sqlite3.connect('todolistdb.db')
            #c=conn.cursor()
            c.execute("insert into todotable values (:task)",{'task':task})
        conn.commit()

           # conn.close()

    def cmdShowTasks():
       
        c.execute('select *,oid from todotable')
        allstuff=c.fetchall()
        for i in range(len(allstuff)):
            notepad2.insert(INSERT,i+1)
            notepad2.insert(INSERT,"\t")
            notepad2.insert(INSERT,allstuff[i][0])
            notepad2.insert(INSERT,"\n")
        notepad2.configure(state='disabled')
        conn.commit()
        
    def cmdClearAll():
        #conn=sqlite3.connect('todolistdb.db')
        #c=conn.cursor()
        c.execute('delete from todotable')
        conn.commit()

    n=Toplevel(root)
    n.title('To Do List')
    n.geometry('300x200')
    n.resizable(0, 0)
    notepad2 = ScrolledText(n, width = 90, height = 40,bg='#e6e7f1')
    todolistmenu=Menu(n)
    n.configure(menu=todolistmenu)
    todolistmenu.add_command(label='Show Tasks',command=cmdShowTasks)
    todolistmenu.add_command(label='Add Task',command=cmdAddTask)
    
    todolistmenu.add_command(label='Delete Tasks',command=cmdDeleteTasks)
    todolistmenu.add_command(label='Clear All',command=cmdClearAll)
    font=StringVar()
    font.set("Font")
    fontmenu=OptionMenu(n,font,"Arial","Times New Roman","Courier New")
    fontmenu.pack()


    notepad2.pack()
    n.mainloop()


notepadMenu = Menu(root)
#todolistmenu=Menu(n)
root.configure(menu=notepadMenu)
fileMenu = Menu(notepadMenu, tearoff = False)
notepadMenu.add_cascade(label='File', menu = fileMenu)
fileMenu.add_command(label='New', command = cmdNew)
fileMenu.add_command(label='Open...', command = cmdOpen)
fileMenu.add_command(label='Save', command = cmdSave)
fileMenu.add_command(label='Save As...', command = cmdSaveAs)
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command = cmdExit)

editMenu = Menu(notepadMenu, tearoff = False)
notepadMenu.add_cascade(label='Edit', menu = editMenu)

editMenu.add_command(label='Cut', command = cmdCut)
editMenu.add_command(label='Copy', command = cmdCopy)
editMenu.add_command(label='Paste', command = cmdPaste)
editMenu.add_command(label='Delete', command = cmdClear)
editMenu.add_separator()
editMenu.add_command(label='Find...', command = cmdFind)
editMenu.add_separator()
editMenu.add_command(label='Select All', command = cmdSelectAll)
editMenu.add_command(label='Time/Date', command = cmdTimeDate)

root.configure(bg='grey')

helpMenu = Menu(notepadMenu, tearoff = False)
notepadMenu.add_cascade(label='Help', menu = helpMenu)

helpMenu.add_command(label='About Notepad', command = cmdAbout)
notepadMenu.add_command(label='ToDo', command = todolist)
fontmenu=Menu(notepadMenu,tearoff=False)
notepadMenu.add_cascade(label='Font',menu=fontmenu,command=cmdFont)
#fontmenu.add_command(label='Font',command=cmdFont)

#todolist = Menu(notepadMenu, tearoff = False)
#notepadMenu.add_cascade(label='ToDo', menu = todolist,command=todolist)
"""todolist.add_command(label='Add Task', command = cmdAddTask)
todolist.add_command(label='Tasks', command = cmdShowTasks)
todolist.add_command(label='Clear All', command = cmdClearAll)
todolist.add_command(label='Delete Task', command = cmdDeleteTasks)"""
conn.commit()
notepad.pack()
root.mainloop()