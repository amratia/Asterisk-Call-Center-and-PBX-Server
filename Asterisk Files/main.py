from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk                    
from tkinter import ttk
from tkinter import messagebox
import pygame
import sys
import os
import subprocess


window= Tk()
window.geometry("1920x1080")


tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
#tab2 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Add Agents')
#tabControl.add(tab2, text ='Extensions')
tabControl.add(tab2, text ='Logs')

tabControl.pack(expand = 1, fill ="both")



#background image#############################
img = PhotoImage(file="/home/shamel/Downloads/Call-Center-Software-featured.png")
label = Label(
    tab1,
    image=img
)



label3 = Label(
    tab2,
    image=img
)



label.place(x=0, y=0)
#label2.place(x=0,y=0)
label3.place(x=0, y=0)

#################################################

#pygame.mixer.init()


window.title("Sayyad's CallCenter")

Name=StringVar()
Type=StringVar()
Context="Agent"
Secret=StringVar()
Host="dynamic"
Disallow="all"
Allow="ulaw"
MailBox=StringVar()
Extension=StringVar()



options = [
 "AR Q","EN Q", "FR Q"
]
  
clicked = StringVar()
  
clicked.set( "AR Q" )
  
# Create Dropdown menu
drop = OptionMenu( tab1 , clicked , *options ).place(x=350,y=150)

# Create button, it will change label text


def submit():
    NewName=Name.get()
    NewType=Type.get()
    #NewContext="Agent"
    NewSecret=Secret.get()
    NewExtension=Extension.get()


  

    NewMailBox=MailBox.get()
    label.config( text = clicked.get() )

    msg = ''

    if (len(NewName) == 0 or len(NewType) == 0 or  len(NewSecret) == 0  or len(NewMailBox)== 0):
            msg = 'At least one label field is empty'
    else:
            try:
                
                if (NewType != "friend" and NewType != "peer" and NewType != "user"):
                    msg = "Wrong Type"
                else:
#SIP.conf          
                 with open(r'sayyad.txt', 'r+') as f:
                    data=f.read()
                    if ("["+NewName+"]") in data:
                        msg='Name is Taken'

                        
                    else:

                        f =open("sayyad.txt","a")
                        f.write("[" + NewName +"]\n")
                        f.write("type="+NewType +"\n")
                        f.write("context="+Context +"\n")
                        f.write("secret="+NewSecret +"\n")
                        f.write("host="+Host +"\n")
                        f.write("disallow="+Disallow+"\n")
                        f.write("allow="+Allow +"\n")
                        f.write("mailbox="+NewMailBox +"@VoiceMail\n\n")
#Extensions.conf
                        with open(r'sayyad.txt', 'r+') as f:
                            data = f.read()
                            if ("[Agent]") in data:
                             data = data.replace("[Agent]", "[Agent]\n" + "exten => "+NewExtension +",Dial(SIP/"+NewName+")\n" + "same => n,Hangup()\n\n")
                        
                        with open(r'sayyad.txt', 'w') as file:
                            file.write(data)

                        with open(r'sayyad.txt', 'r+') as f:
                            data = f.read()
                            if ("[Manager]") in data:
                                data = data.replace("[Manager]", "[Manager]\n"+ "exten => "+NewExtension +",Dial(SIP/"+NewName+")\n" + "same => n,Hangup()\n\n")
                        
                        with open(r'sayyad.txt', 'w') as file:
                            file.write(data)

                        with open(r'sayyad.txt', 'r+') as f:
                            data = f.read()
                            if ("[CEO]") in data:
                                data = data.replace("[CEO]", "[CEO]\n"+ "exten => "+NewExtension +",Dial(SIP/"+NewName+")\n" + "same => n,Hangup()\n\n")
                        
                        with open(r'sayyad.txt', 'w') as file:
                            file.write(data) 

                        with open(r'sayyad.txt', 'r+') as f:
                            data = f.read()
                            if ("[Tech-Sup]") in data:
                                data = data.replace("[Tech-Sup]", "[Tech-Sup]\n"+ "exten => "+NewExtension +",Dial(SIP/"+NewName+")\n" + "same => n,Hangup()\n\n")
                        with open(r'sayyad.txt', 'w') as file:
                            file.write(data)  

#Queues.conf

                        if (clicked.get()=="EN Q"):
                            print("HelloWorld")
                            with open(r'sayyad.txt', 'r+') as f:
                              data = f.read()
                              if ("[en]") in data:
                                    data = data.replace("[en]", "[en]\n"+ "member => SIP/"+NewName+"\n" )
                            with open(r'sayyad.txt', 'w') as file:
                              file.write(data)  
                        elif (clicked.get()=="AR Q"):
                            print("HelloWorld")
                            with open(r'sayyad.txt', 'r+') as f:
                              data = f.read()
                              if ("[ar]") in data:
                                    data = data.replace("[ar]", "[ar]\n"+ "member => SIP/"+NewName+"\n" )
                            with open(r'sayyad.txt', 'w') as file:
                              file.write(data)  
                        if (clicked.get()=="FR Q"):
                            print("HelloWorld")
                            with open(r'sayyad.txt', 'r+') as f:
                              data = f.read()
                              if ("[fr]") in data:
                                    data = data.replace("[fr]", "[fr]\n"+ "member => SIP/"+NewName+"\n" )
                            with open(r'sayyad.txt', 'w') as file:
                              file.write(data)  




                      
                       
                        f.close()
                        Name.set("")
                        Type.set("")
                        #Context.set("")
                        Secret.set("")
                        Extension.set("")
                        MailBox.set("")
                        msg = 'Success!'
                        #pygame.mixer.music.load("waa.mp3")
                        #pygame.mixer.music.play()

            except Exception as ep:
                messagebox.showerror('error', ep)

    messagebox.showinfo('message', msg)


    

    


Header1 = Label(tab1,text = "Please, Put your info to be Registered in the SIP file",font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=150,y=10)




name_label = Label(tab1, text = '[Name]', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=200,y=70)
name_entry = Entry(tab1,textvariable = Name, font=('calibre',10,'normal'),bg="black",foreground="white").place(x=300,y=70)


type_label = Label(tab1, text = 'type=', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=200,y=110)
type_entry = Entry(tab1,textvariable = Type, font=('calibre',10,'normal'),bg="black",foreground="white").place(x=300,y=110)

Queue_label = Label(tab1, text = 'QueueName', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=200,y=150)

secret_label = Label(tab1, text = 'secret=', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=200,y=190)
secret_entry = Entry(tab1,textvariable = Secret, font=('calibre',10,'normal'),show='*',bg="black",foreground="white").place (x=300,y=190)


mailbox_label = Label(tab1, text = 'mailbox=', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=200,y=230)
mailbox_entry = Entry(tab1,textvariable = MailBox, font=('calibre',10,'normal'),bg="black",foreground="white").place(x=300,y=230)

exten_label = Label(tab1, text = 'Extension', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=200,y=270)
exten_entry = Entry(tab1,textvariable = Extension, font=('calibre',10,'normal'),bg="black",foreground="white").place(x=300,y=270)

submit_button=Button(tab1,text = 'Submit', command = submit,bg="white").place(x=300,y=340)





#TAB - 2

def openCallLogFunc():
    filename1 ="/var/log/asterisk/cdr-csv/Master.csv"
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, filename1])
    #Keep_both_files_in_the_same_Folder

def openComplaintsFunc():
    filename2 ="/etc/asterisk/Complaint.csv"
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, filename2])
    #Keep_both_files_in_the_same_Folder

def openQueue_Func():
    filename3 ="/etc/asterisk/Queue.csv"
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, filename3])
    #Keep_both_files_in_the_same_Folder

b1=tk.Button(tab2, text="Call Log",bg="white",command=openCallLogFunc)
b2=tk.Button(tab2, text="Complaints Log",bg="white",command=openComplaintsFunc)
b3=tk.Button(tab2, text="Queue Log",bg="white",command=openQueue_Func)
b1.place(x=310,y=120)
b2.place(x=310,y=170)
b3.place(x=310,y=220)




















"""
Header1.grid(row=0, column=1)

#name_label.grid(row=2,column=1)
name_entry.grid(row=2,column=2)

#type_label.grid(row=4,column=1)
type_entry.grid(row=4,column=2)

context_label.grid(row=6,column=1)
context_entry.grid(row=6,column=2)

secret_label.grid(row=8,column=1)
secret_entry.grid(row=8,column=2)

host_label.grid(row=10,column=1)
host_entry.grid(row=10,column=2)


disallow_label.grid(row=12,column=1)
disallow_entry.grid(row=12,column=2)

allow_label.grid(row=14,column=1)
allow_entry.grid(row=14,column=2)

mailbox_label.grid(row=16,column=1)
mailbox_entry.grid(row=16,column=2)


submit_button.grid(row=18,column=2)
"""
window.mainloop()

