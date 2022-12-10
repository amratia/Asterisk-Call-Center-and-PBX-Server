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
window.geometry("509x339")




tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Add Agents')
tabControl.add(tab2, text ='Logs')

tabControl.pack(expand = 1, fill ="both")



#background image#############################
img= ImageTk.PhotoImage(Image.open("/home/shamel/Desktop/istockphoto-1348081840-170667a.jpg"))
#img = PhotoImage(file="/home/shamel/Desktop/istockphoto-1348081840-170667a.jpg")
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


window.title("CallCenter")

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
drop = OptionMenu( tab1 , clicked , *options ).place(x=270,y=105)

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
                 with open(r'sip.conf', 'r+') as f:
                    data=f.read()
                    if ("["+NewName+"]") in data:
                        msg='Name is Taken'

                        
                    else:

                        f =open("sip.conf","a")
                        f.write("[" + NewName +"]\n")
                        f.write("type="+NewType +"\n")
                        f.write("context="+Context +"\n")
                        f.write("secret="+NewSecret +"\n")
                        f.write("host="+Host +"\n")
                        f.write("disallow="+Disallow+"\n")
                        f.write("allow="+Allow +"\n")
                        f.write("mailbox="+NewMailBox +"@VoiceMail\n\n")
#Extensions.conf
                        with open(r'extensions.conf', 'r+') as f:
                            data = f.read()
                            if ("[Agent]") in data:
                             data = data.replace("[Agent]", "[Agent]\n" + "exten => "+NewExtension +",Dial(SIP/"+NewName+")\n" + "same => n,Hangup()\n\n")
                        
                        with open(r'extensions.conf', 'w') as file:
                            file.write(data)

                        with open(r'extensions.conf', 'r+') as f:
                            data = f.read()
                            if ("[Manager]") in data:
                                data = data.replace("[Manager]", "[Manager]\n"+ "exten => "+NewExtension +",Dial(SIP/"+NewName+")\n" + "same => n,Hangup()\n\n")
                        
                        with open(r'extensions.conf', 'w') as file:
                            file.write(data)

                        with open(r'extensions.conf', 'r+') as f:
                            data = f.read()
                            if ("[CEO]") in data:
                                data = data.replace("[CEO]", "[CEO]\n"+ "exten => "+NewExtension +",Dial(SIP/"+NewName+")\n" + "same => n,Hangup()\n\n")
                        
                        with open(r'extensions.conf', 'w') as file:
                            file.write(data) 

                        with open(r'extensions.conf', 'r+') as f:
                            data = f.read()
                            if ("[Tech-Sup]") in data:
                                data = data.replace("[Tech-Sup]", "[Tech-Sup]\n"+ "exten => "+NewExtension +",Dial(SIP/"+NewName+")\n" + "same => n,Hangup()\n\n")
                        with open(r'extensions.conf', 'w') as file:
                            file.write(data)  

#Queues.conf

                        if (clicked.get()=="EN Q"):
                            print("HelloWorld")
                            with open(r'queues.conf', 'r+') as f:
                              data = f.read()
                              if ("[en]") in data:
                                    data = data.replace("[en]", "[en]\n"+ "member => SIP/"+NewName+"\n" )
                            with open(r'queues.conf', 'w') as file:
                              file.write(data)  
                        elif (clicked.get()=="AR Q"):
                            print("HelloWorld")
                            with open(r'queues.conf', 'r+') as f:
                              data = f.read()
                              if ("[ar]") in data:
                                    data = data.replace("[ar]", "[ar]\n"+ "member => SIP/"+NewName+"\n" )
                            with open(r'queues.conf', 'w') as file:
                              file.write(data)  
                        elif (clicked.get()=="FR Q"):
                            print("HelloWorld")
                            with open(r'queues.conf', 'r+') as f:
                              data = f.read()
                              if ("[fr]") in data:
                                    data = data.replace("[fr]", "[fr]\n"+ "member => SIP/"+NewName+"\n" )
                            with open(r'queues.conf', 'w') as file:
                              file.write(data)  




                      
                       
                        f.close()
                        Name.set("")
                        Type.set("")
                        Secret.set("")
                        Extension.set("")
                        MailBox.set("")
                        msg = 'Success!'


            except Exception as ep:
                messagebox.showerror('error', ep)

    messagebox.showinfo('message', msg)


    

    


#Header1 = Label(tab1,text = "Please, Put your info to be Registered in the SIP file",font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=150,y=10)




name_label = Label(tab1, text = '[Name]', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=120,y=30)
name_entry = Entry(tab1,textvariable = Name, font=('calibre',10,'normal'),bg="black",foreground="white").place(x=210,y=30)


type_label = Label(tab1, text = 'type=', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=120,y=70)
type_entry = Entry(tab1,textvariable = Type, font=('calibre',10,'normal'),bg="black",foreground="white").place(x=210,y=70)

Queue_label = Label(tab1, text = 'QueueName', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=120,y=110)

secret_label = Label(tab1, text = 'secret=', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=120,y=150)
secret_entry = Entry(tab1,textvariable = Secret, font=('calibre',10,'normal'),show='*',bg="black",foreground="white").place (x=210,y=150)


mailbox_label = Label(tab1, text = 'mailbox=', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=120,y=190)
mailbox_entry = Entry(tab1,textvariable = MailBox, font=('calibre',10,'normal'),bg="black",foreground="white").place(x=210,y=190)

exten_label = Label(tab1, text = 'Extension', font=('calibre',10, 'bold'),bg="white",foreground="black").place(x=120,y=230)
exten_entry = Entry(tab1,textvariable = Extension, font=('calibre',10,'normal'),bg="black",foreground="white").place(x=210,y=230)

submit_button=Button(tab1,text = 'Submit', command = submit,bg="white").place(x=410,y=280)





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

b1=tk.Button(tab2, text="Call Log",bg="black",foreground="white",command=openCallLogFunc)
b2=tk.Button(tab2, text="Complaints Log",bg="black",foreground="white",command=openComplaintsFunc)
b3=tk.Button(tab2, text="Queue Log",bg="black",foreground="white",command=openQueue_Func)
b1.place(x=215,y=90)
b2.place(x=190,y=130)
b3.place(x=210,y=170)


window.mainloop()
