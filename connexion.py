import pypyodbc as odbc #pip install pypyodbc
from sqlalchemy import create_engine
Driver_Name ='SQL SERVER'
Server_Name ='Sarra\SQLEXPRESS'
Database_Name ='SagemProductionManagment'
conn_str= f"""
  Driver={{{Driver_Name}}};
  Server={Server_Name};
  Database{Database_Name} ;
  trust_conn=yes;
"""
cnxn = create_engine(conn_str)
print(cnxn)
