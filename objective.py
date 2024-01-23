from tkinter import *
from tkinter import messagebox,Button,DoubleVar,Scale,Tk,Spinbox
import tkinter.ttk as ttk
from tkcalendar import *
from datetime import date
import pypyodbc
import datetime
import calendar
from pypyodbc import Cursor
from PIL import ImageTk,Image
import os
import holidays

root=Tk()
root.title('Objective')
root.geometry('1350x765+80+40')
root.resizable(False,False)
img=ImageTk.PhotoImage(Image.open("dr.png"))
label=Label(image=img)
label.place(x=-5,y=-5)

def add_produit():
    if idPro.get() == "" or TypePro.get() == "" or Année.get() == "" or Mois.get() == "" or objective.get() == "" or nbre_jour.get() == "":
        messagebox.showerror("Error", "You have not filled in all the fields", parent=root)
    else:
        try:
            conn_str = "DRIVER={SQL Server};SERVER=Sarra\SQLEXPRESS;DATABASE=SagemProductionManagment;Trusted_Connection=yes;"
            conn = pypyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Code d'insertion des champs dans la base de données
            sql = "INSERT INTO Production (TypePro, Année, Mois, objective, nbre_jour) VALUES (?, ?, ?, ?, ?)"
            values = (TypePro.get(), Année.get(), Mois.get(), objective.get(), nbre_jour.get())
            cursor.execute(sql, values)

            conn.commit()
            afficheresultat()
            messagebox.showinfo("Success", "Record added successfully", parent=root)

            # Calcul des moyennes
            moyenne_mois, moyenne_jour = calculate_moyennes()

            # Ajout des moyennes à l'affichage
            tab_resultat.insert("", "end", values=(idPro.get(), Année.get(), Mois.get(), objective.get(), nbre_jour.get(), moyenne_mois, moyenne_jour))

        except Exception as es:
            messagebox.showerror("Error", f"Database connection error: {str(es)}", parent=root)

def calculate_moyennes():
    moyenne_mois = float(objective.get()) / float(Mois.get())
    moyenne_jour = float(objective.get()) / float(nbre_jour.get())
    return moyenne_mois, moyenne_jour



def update_produit():
    if idPro.get() == "" or TypePro.get() == "" or Année.get() == "" or Mois.get() == "" or objective.get() == "" or nbre_jour.get() == "":
        messagebox.showerror("Error", "You have not filled in all the fields", parent=root)
    else:
        try:
            conn_str = "DRIVER={SQL Server};SERVER=Sarra\SQLEXPRESS;DATABASE=SagemProductionManagment;Trusted_Connection=yes;"
            conn = pypyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Code de mise à jour des champs dans la base de données
            sql = "UPDATE Production SET TypePro = ?, Année = ?, Mois = ?, objective = ?, nbre_jour = ? WHERE idPro = ?"
            values = (TypePro.get(), Année.get(), Mois.get(), objective.get(), nbre_jour.get(), idPro.get())
            cursor.execute(sql, values)

            conn.commit()
            afficheresultat()
            messagebox.showinfo("Success", "Record updated successfully", parent=root)

        except Exception as es:
            messagebox.showerror("Error", f"Database connection error: {str(es)}", parent=root)


def delete_produit():
    if idPro.get() == "":
        messagebox.showerror("Error", "No record selected", parent=root)
    else:
        try:
            conn_str = "DRIVER={SQL Server};SERVER=Sarra\SQLEXPRESS;DATABASE=SagemProductionManagment;Trusted_Connection=yes;"
            conn = pypyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Code de suppression de l'enregistrement dans la base de données
            sql = "DELETE FROM Production WHERE idPro = ?"
            values = (idPro.get(),)
            cursor.execute(sql, values)

            conn.commit()
            afficheresultat()
            messagebox.showinfo("Success", "Record deleted successfully", parent=root)

            # Effacer les champs
            idPro.set("")
            TypePro.set("")
            Année.set("")
            Mois.set("")
            objective.set("")
            nbre_jour.set("")

        except Exception as es:
            messagebox.showerror("Error", f"Database connection error: {str(es)}", parent=root)









def calculate_working_days():
    year = int(Année.get())
    month = int(Mois.get())
    
    # Get the actual number of days in the selected month
    _, total_days = calendar.monthrange(year, month)
    
    # Assuming weekends are on Saturdays and Sundays
    weekend_days = [calendar.SATURDAY, calendar.SUNDAY]
    
    # Get the holidays for Tunisia
    tn_holidays = holidays.TN(years=year)
    
    # Calculate the number of working days by excluding weekends and holidays
    working_days = 0
    for day in range(1, total_days + 1):
        date = datetime.date(year, month, day)
        if is_weekday(date) and not is_holiday(date, tn_holidays):
            working_days += 1

    # Update the value of the "Number of the day" Spinbox
    nbre_jour.set(working_days)

# Function to check if a date is a weekday (Monday to Friday)
def is_weekday(date):
    return date.weekday() < 5  # Monday is 0, Sunday is 6

# Function to check if a date is a holiday
def is_holiday(date, country_holidays):
    return date in country_holidays






def afficheresultat():
      conn_str = "DRIVER={SQL Server};SERVER=Sarra\SQLEXPRESS;DATABASE=SagemProductionManagment;Trusted_Connection=yes;"
      conn = pypyodbc.connect(conn_str)
      cursor = conn.cursor()
      cursor.execute("select* from Production")
      rows=cursor.fetchall()
      if len(rows)!=0:
          tab_resultat.delete(*tab_resultat.get_children())
          for row in rows:
              tab_resultat.insert("",END,values=row)
      conn.commit()
      conn.close()


def save_current_date():
    try:
        conn_str = "DRIVER={SQL Server};SERVER=Sarra\SQLEXPRESS;DATABASE=SagemProductionManagment;Trusted_Connection=yes;"
        conn = pypyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Obtenir la date du jour
        current_date = date.today()

        # Code d'insertion de la date du jour dans la colonne Datedujour de la table Production
        sql = "UPDATE Production SET Datedujour = ?"
        values = (current_date,)
        cursor.execute(sql, values)

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Current date saved successfully")

    except Exception as es:
        messagebox.showerror("Error", f"Database connection error: {str(es)}")





def logout():
    # Afficher une boîte de dialogue de confirmation
    if messagebox.askokcancel("Logout", "Are you sure you want to logout?"):
        # Enregistrer automatiquement la date du jour dans la base de données
        save_current_date()
        
        # Fermer la fenêtre principale de l'application
        root.destroy()



def select_row(event):
    item = tab_resultat.focus()
    values = tab_resultat.item(item, "values")
    if values:
        idPro.set(values[0])
        Année.set(values[1])
        Mois.set(values[2])
        objective.set(values[3])
        nbre_jour.set(values[4])

def afficher_info_type():
    selected_type = affiche_type.get()
    tab_resultat.delete(*tab_resultat.get_children())  # Effacer les données actuelles du tableau

    conn_str = "DRIVER={SQL Server};SERVER=Sarra\SQLEXPRESS;DATABASE=SagemProductionManagment;Trusted_Connection=yes;"
    conn = pypyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Production WHERE TypePro=?", (selected_type,))
    rows = cursor.fetchall()
    for row in rows:
        tab_resultat.insert("", "end", values=row)

    conn.close()








def rechercher_info():
    keyword = rech.get()
    tab_resultat.delete(*tab_resultat.get_children())  # Effacer les données actuelles du tableau

    conn_str = "DRIVER={SQL Server};SERVER=Sarra\SQLEXPRESS;DATABASE=SagemProductionManagment;Trusted_Connection=yes;"
    conn = pypyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Production WHERE idPro LIKE ? OR Année LIKE ? OR Mois LIKE ? OR objective LIKE ? OR nbre_jour LIKE ?",
                   (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    rows = cursor.fetchall()
    for row in rows:
        tab_resultat.insert("", "end", values=row)

    conn.close()








#les variables
Année = IntVar()
idPro=IntVar()
Mois=IntVar()
objective=IntVar()
nbre_jour=StringVar() 
TypePro=StringVar()
aff_type=StringVar
aff=int
#formulaire
Gestion_frame=Frame(root,bd=5,relief=GROOVE,bg="white")
Gestion_frame.place(x=20,y=80,width=530,height=600)

Gestion_Title=Label(Gestion_frame,text="Production information",font=("arial black",30,"bold"),bg="white",fg="#38B0DE")
Gestion_Title.place(x=5,y=40)
# Id
id_1=Label(Gestion_frame,text="ID",bg="white",fg="black",font=("arial",12,"bold"))
id_1.place(x=25,y=130)

entry_id_1=Entry(Gestion_frame,width=30,textvariable=idPro,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11))
entry_id_1.place(x=18,y=152,width=200)


Type_production=Label(Gestion_frame,text="Type_Production",bg="white",fg="black",font=("arial",12,"bold"))
Type_production.place(x=18,y=182)
T_Pro=ttk.Combobox(Gestion_frame,textvariable=TypePro,font=("time new roman",11))
T_Pro["values"]=("BBM","AVS","BBS","BBE")
T_Pro.place(x=18,y=212,width=200)
T_Pro.current(0)
A_1=Label(Gestion_frame,text="Year",bg="white",fg="black",font=("arial",12,"bold"))
A_1.place(x=18,y=242)
entry_A_1=Spinbox(Gestion_frame,width=30,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11),textvariable=Année, from_=1980, to=2050)
entry_A_1.place(x=18,y=272,width=200 )

M_1=Label(Gestion_frame,text="Month",bg="white",fg="black",font=("arial ",12,"bold"))
M_1.place(x=18,y=300)
entry_M_1=Spinbox(Gestion_frame,width=30,fg='black',textvariable=Mois,border=1.5,bg="white",font=('Microsoft YaHei UI Light',11),from_=1, to=12)
entry_M_1.place(x=18,y=330 ,width=200)
btn_style = ttk.Style()
btn_style.configure('Accent.TButton', foreground='black',bd=0, background='#38B0DE', font=('time new roman', 15))
btn = ttk.Button(Gestion_frame, text="Calculate",cursor="hand2", style='Accent.TButton', command=calculate_working_days)
btn.place(x=365,y=330 , height=30,width=120)
O_1=Label(Gestion_frame,text="Objective",bg="white",fg="black",font=("arial",12,"bold"))
O_1.place(x=18,y=360)
entry_O_1=Entry(Gestion_frame,width=30,textvariable=objective,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11))
entry_O_1.place(x=18,y=390 ,width=200)
NB_j=Label(Gestion_frame,text="Number of the day",bg="white",fg="black",font=("arial",12,"bold"))
NB_j.place(x=18,y=420)
entry_NB_j=Spinbox(Gestion_frame,width=30,textvariable=nbre_jour,fg='black',border=1.5,bg="white",font=('Microsoft YaHei UI Light',11),from_=1, to=1000)
entry_NB_j.place(x=18,y=450,width=200)
btn_add=Button(Gestion_frame,text="Add",font=("times new roman",15),bd=10,relief=GROOVE,bg="#38B0DE",command=add_produit)
btn_add.place(x=15,y=510,width=120)
btn_update=Button(Gestion_frame,text="Update",font=("times new roman",15),bd=10,relief=GROOVE,bg="#38B0DE",command=update_produit)
btn_update.place(x=190,y=510,width=120)
btn_delete=Button(Gestion_frame,text="Delete",font=("times new roman",15),bd=10,relief=GROOVE,bg="#38B0DE",command=delete_produit)
btn_delete.place(x=365,y=510,width=120)
#recherche
Details_Frame=Frame(root,bd=5,relief=GROOVE,bg="white")
Details_Frame.place(x=565,y=80,width=770,height=600)
affiche_type=ttk.Combobox(Details_Frame,font=("time new roman",20),textvariable=aff_type,state="readonly")
affiche_type["value"]=("BBM","AVS","BBS","BBE")
affiche_type.current(0)
affiche_type.place(x=30,y=30,width=100)
btn_aff=Button(Details_Frame,text="show",font=("time new roman",15),bd=1,bg="#38B0DE",textvariable=aff,command=afficher_info_type)
btn_aff.place(x=150,y=30)
rech=Entry(Details_Frame,font=("time new roman",15),relief=GROOVE,border=2)
rech.place(x=400,y=35,width=150)
btn_rech=Button(Details_Frame,text="Search",font=("time new roman",15),bd=1,bg="#38B0DE",command=rechercher_info)
btn_rech.place(x=580,y=30)
resultat_frame=Frame(Details_Frame,bd=2,relief=GROOVE,bg="white")
resultat_frame.place(x=15,y=90,width=730,height=490)
#tableau
scroll_x=Scrollbar(resultat_frame,orient=HORIZONTAL)
scroll_y=Scrollbar(resultat_frame,orient=VERTICAL)
tab_resultat=ttk.Treeview(resultat_frame,columns=("idPro","Année","Mois","objective","nbre_jour","moyenne_mois", "moyenne_jour"))
tab_resultat.config(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.config(command=tab_resultat.xview)
scroll_y.config(command=tab_resultat.yview)

scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
tab_resultat.heading("idPro", text="ID")
tab_resultat.heading("Année", text="Year")
tab_resultat.heading("Mois", text="Month")
tab_resultat.heading("objective", text="Objective")
tab_resultat.heading("nbre_jour", text="Number of the day")
tab_resultat.heading("moyenne_mois", text="Average per month")
tab_resultat.heading("moyenne_jour", text="Average per day")

tab_resultat["show"]="headings"
tab_resultat.column("idPro", width=50)
tab_resultat.column("Année", width=100)
tab_resultat.column("Mois", width=100)
tab_resultat.column("objective", width=100)
tab_resultat.column("nbre_jour", width=130)
tab_resultat.column("moyenne_mois", width=130)
tab_resultat.column("moyenne_jour", width=130)

tab_resultat.pack()
tab_resultat.bind("<ButtonRelease-1>", add_produit)
tab_resultat.bind("<ButtonRelease-1>",select_row)
afficheresultat()
btn_rech=Button(root,text="Logout",font=("time new roman",15),bd=1,bg="#38B0DE",command=logout)
btn_rech.place(x=1240,y=30)



sel = StringVar()
cal = DateEntry(root, selectmode='day', textvariable=sel,bd=1)
cal.place(x=1100,y=30,height=38,width=100)
















root.mainloop()
