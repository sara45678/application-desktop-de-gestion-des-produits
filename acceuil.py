from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter as tk
from PIL import Image, ImageTk
import pypyodbc
from PIL import ImageTk,Image
import os

root=Tk()
root.title('Accueil')
root.geometry('1350x765+80+40')
img=ImageTk.PhotoImage(Image.open("dr.png"))
label=Label(image=img)
label.place(x=-5,y=-5)
root.resizable(False,False)

def authenticate():
    password = password_entry.get()

    if password == "sagemcom123":
        # Mot de passe correct, navigation vers la page de connexion
        global root
        root.destroy()  # Fermer la fenêtre actuelle (sign in)
        import Signin
    else:
        messagebox.showerror("Error", "Invalid password")
















        


Gestion_frame=Frame(root,bd=1,relief=GROOVE,bg="white")
Gestion_frame.place(x=360,y=10,width=600,height=740)
image = Image.open("sagemcom.png")
photo = ImageTk.PhotoImage(image)
label = tk.Label(Gestion_frame, image=photo)
label.place(x=60,y=-2,width=490,height=550)
password=Label(Gestion_frame, text="Put the password" ,fg='#5959AB', bg='white',font=('Arial ',20,' bold '))
password.place(x=190,y=550)
password_entry=Entry(Gestion_frame,width=30,fg='black',show="*",border=1.5,bg="white",font=('Microsoft YaHei UI Light',11))
password_entry.place(x=208,y=600,width=200)
password_btn = Button(Gestion_frame,text="Go on",font=("time new roman",15),bd=1,bg="#38B0DE" ,command=authenticate)
password_btn.place(x=235,y=650 ,width=150)
root.mainloop()