from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkcalendar import *
import pypyodbc
from PIL import ImageTk,Image
import os

root=Tk()
root.title('Sign up')
root.geometry('1350x765+80+40')
img=ImageTk.PhotoImage(Image.open("dr.png"))
label=Label(image=img)
label.place(x=-5,y=-5)
root.resizable(False,False)

def login(username,Email,password1,phone,adress,cin):
    username=entryuser.get()
    Email=entryemail.get()
    password1=entrypass.get()
    phone=entryphone.get()
    adress=entryadress.get()
    cin=entrycin.get()
   

def create():
    if entryuser.get()=="" or entryemail.get()=="" or entrypass.get()=="" or entryphone.get()=="" or entryadress.get()=="" or entrycin.get()=="": 
        messagebox.showerror("error","fill in the fields",parent=root)
    elif var_check.get()==0:
        messagebox.showerror("error","Be sure to accept the fields and terms",parent=root)
    else:
        try:
            conn_str = "DRIVER={SQL Server};SERVER=Sarra\SQLEXPRESS;DATABASE=SagemProductionManagment;Trusted_Connection=yes;"
            conn = pypyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            # Votre code d'insertion des données dans la base de données
            # par exemple :
            sql = "INSERT INTO Users (Username, Email, Password, Phone, Address, CIN) VALUES (?,?,?,?,?,?)"
            values = (entryuser.get(), entryemail.get(), entrypass.get(), entryphone.get(), entryadress.get(), entrycin.get())
            cursor.execute(sql, values)
            conn.commit()
            
            messagebox.showinfo("Success", "User registered successfully", parent=root)
        except Exception as es:
            messagebox.showerror("Error", f"Connection error: {str(es)}", parent=root)


def goto_signup():
     global root
     root.destroy()  # Fermer la fenêtre actuelle (sign in)
     import Signup
   







def goto_signin():
    global root
    root.destroy()  # Fermer la fenêtre actuelle (sign up)
    import Signin





   
         

def bouton_clique():
     print("Le bouton a été cliqué!")

Gestion_frame=Frame(root,bd=1,relief=GROOVE,bg="white")
Gestion_frame.place(x=380,y=40,width=580,height=700)




heading=Label(Gestion_frame,text='Sign up to your account',fg='#38B0DE',bg='white',font=('Arial Black ',35,' bold '))
heading.place(x=20,y=50)

username=Label(Gestion_frame, text="Username" ,fg='black', bg='white',font=('Arial ',15,' bold '))
username.place(x=40,y=148)
entryuser=Entry(Gestion_frame,width=30,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11))
entryuser.place(x=140,y=150,width=250)

Email=Label(Gestion_frame, text="Email" ,fg='black', bg='white',font=('Arial ',15,' bold '))
Email.place(x=40,y=200)
entryemail=Entry(Gestion_frame,width=30,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11))
entryemail.place(x=140,y=200,width=250)

Password=Label(Gestion_frame, text="Password" , bg='white',font=('Arial ',15,' bold '))
Password.place(x=40,y=260)
entrypass=Entry(Gestion_frame,width=30,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11),show='*')
entrypass.place(x=140,y=260 ,width=250)


Phone=Label(Gestion_frame, text="Phone" ,fg='black', bg='white',font=('Arial ',15,' bold '))
Phone.place(x=40,y=320)
entryphone=Entry(Gestion_frame,width=30,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11))
entryphone.place(x=140,y=320,width=250)

Adress=Label(Gestion_frame, text="Adress" ,fg='black', bg='white',font=('Arial ',15,' bold '))
Adress.place(x=40,y=390)
entryadress=Entry(Gestion_frame,width=30,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11))
entryadress.place(x=140,y=390,width=250)

Cin=Label(Gestion_frame, text="CIN" ,fg='black', bg='white',font=('Arial ',15,' bold '))
Cin.place(x=40,y=450)
entrycin=Entry(Gestion_frame,width=30,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11))
entrycin.place(x=140,y=450,width=250)



var_check=IntVar()
chk=Checkbutton(Gestion_frame,variable=var_check,onvalue=1,offvalue=0,text="I agree to the terms and conditions",font=("times new roman",12),bg='white')
chk.place(x=40,y=520)



style_accent_button = ttk.Style()
style_accent_button.configure('Accent.TButton', foreground='black', background='#007BFF', font=('Arial', 13,'bold'))

bouton_accent = ttk.Button(Gestion_frame, text="Create",cursor="hand2", style='Accent.TButton', command=create)
bouton_accent.place(x=120,y=580 ,width=150,height=35)
btn = ttk.Button(Gestion_frame, text="Cancel",cursor="hand2", style='Accent.TButton', command=goto_signin)
btn.place(x=300,y=580 ,width=150,height=35)
root.mainloop()



