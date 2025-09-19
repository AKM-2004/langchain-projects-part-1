import sqlite3 as sq 
import pandas as pd
## connect to sqllite
connection = sq.connect("customer.db")


## create a cursor object to insert record, create table
cursor = connection.cursor()

## create the table 

table_info = """

create table if not exists customer(
Invoice_ID varchar(50) primary key,
City varchar(50),
Gender varchar(50) ,
Product_line varchar(50),
Unit_price integer,
Quantity integer,
Total  integer,
Date date not null ,
Payment varchar(50),
gross_income integer,
Rating integer
);
"""

cursor.execute(table_info)

## importing all the data from the csv to SQL

def save_all_data(file_path):
    df = pd.read_csv(file_path)
    for i in range(df.shape[0]):
        cursor.execute(f"""insert into customer values("{df.iloc[i,:]["Invoice ID"]}","{df.iloc[i,:]["City"]}","{df.iloc[i,:]["Gender"]}","{df.iloc[i,:]["Product line"]}","{df.iloc[i,:]["Unit price"]}","{df.iloc[i,:]["Quantity"]}","{df.iloc[i,:]["Total"]}","{df.iloc[i]["Date"]}","{df.iloc[i]["Payment"]}","{df.iloc[i]["gross income"]}","{df.iloc[i]["Rating"]}")""")
        

save_all_data(".\input_table.csv")


## display all the records
print("The inserted records are ")
data = cursor.execute(""" select * from customer """)

for row in data:
    print(row)


## commit your changes in databases
connection.commit()
connection.close()