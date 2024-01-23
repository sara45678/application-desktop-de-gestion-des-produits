from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkcalendar import *
import pypyodbc
from PIL import ImageTk,Image
import os

root=Tk()
root.title('Sign in')
root.geometry('1350x765+80+40')
img=ImageTk.PhotoImage(Image.open("dr.png"))
label=Label(image=img)
label.place(x=-5,y=-5)


root.resizable(False,False)








def connect():
    username = entryuser.get()
    password = entrypass.get()
    
    if username == "" or password == "":
        messagebox.showerror("Error", "Fill in the fields", parent=root)
    else:
        try:
            # Code de connexion à la base de données et vérification des informations d'identification
            conn_str = "DRIVER={SQL Server};SERVER=Sarra\SQLEXPRESS;DATABASE=SagemProductionManagment;Trusted_Connection=yes;"
            conn = pypyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            sql = "SELECT * FROM Users WHERE Username = ? AND Password = ?"
            values = (username, password)
            cursor.execute(sql, values)
            
            user = cursor.fetchone()  # Récupérer la première ligne correspondante
            if user:
                if root.winfo_exists():
                 messagebox.showinfo("Success", "User logged in successfully", parent=root)
                
                 root.destroy()
                 import objective
                 objective.show_interface()
                 conn.close()
            else:
                messagebox.showerror("Error", "Invalid username or password", parent=root)
        except Exception as es:
            messagebox.showerror("Error", f"Connection error: {str(es)}", parent=root)





def goto_signup():
     global root
     root.destroy()  # Fermer la fenêtre actuelle (sign in)
     import Signup
    




def bouton_clique():
     print("Le bouton a été cliqué!")

Gestion_frame=Frame(root,bd=1,relief=GROOVE,bg="white")
Gestion_frame.place(x=360,y=50,width=600,height=650)




heading=Label(Gestion_frame,text='Sign in to your account',fg='#38B0DE',bg='white',font=('Arial Black ',35,' bold '))
heading.place(x=40,y=50)

username=Label(Gestion_frame, text="Username" ,fg='#5959AB', bg='white',font=('Arial ',15,' bold '))
username.place(x=40,y=160)
entryuser=Entry(Gestion_frame ,width=30,fg='#5959AB',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11))
entryuser.place(x=40,y=200,width=250)

Password=Label(Gestion_frame, text="Password" , bg='white',font=('Arial ',15,' bold '),fg="#5959AB")
Password.place(x=40,y=240)
entrypass=Entry(Gestion_frame,width=30,fg='#5959AB',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11),show='*')
entrypass.place(x=40,y=280 ,width=250)


var_check=IntVar()
chk=Checkbutton(Gestion_frame,variable=var_check,onvalue=1,offvalue=0,text="I agree to the terms and conditions",font=("times new roman",12),bg='white')
chk.place(x=40,y=340)
style_accent_button = ttk.Style()
style_accent_button.configure('Accent.TButton', foreground='black', background='#007BFF', font=('Arial', 18,'bold'))

bouton_accent = ttk.Button(Gestion_frame, text="connect",cursor="hand2", style='Accent.TButton', command=connect)
bouton_accent.place(x=220,y=420 ,width=200,height=40)
dl=Label(Gestion_frame, text="Create new account" , bg='white',font=("times new roman",13,' bold '))
dl.place(x=40,y=520)
btn_style = ttk.Style()
btn_style.configure('Accent.TButton', foreground='black',bd=0, background='#38B0DE', font=('Arial', 10,'bold'))
btn = ttk.Button(Gestion_frame, text="Create",cursor="hand2", style='Accent.TButton', command=goto_signup)
btn.place(x=200,y=520 , height=25)


root.mainloop()