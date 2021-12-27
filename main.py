from tkinter import *
from tkinter import ttk
import sqlite3

class Product:
    db_name = "BaseDeDatos.db"
    def __init__(self,ventana):
        #ventana
        self.wind = ventana
        self.wind.title("Register your product")
        
        #frame
        frame = LabelFrame(self.wind, text = "Register a new Product")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        
        #Labels and entrys
        Label(frame,text="Name: ").grid(row=1,column=0)
        Label(frame,text="Price: ").grid(row=2,column=0)
        self.label_alerts = Label(self.wind,text = "")
        self.entry_name = Entry(frame)
        self.entry_price = Entry(frame)
        self.entry_name.grid(row=1,column=1)
        self.entry_price.grid(row=2,column=1)
        self.label_alerts.grid(row=3,columnspan=2)
        
        #treeview con los productos
        self.tree = ttk.Treeview(self.wind,height=10,column=2)
        self.tree.grid(row=4,column=0,columnspan=2,sticky = W+E)
        self.tree.heading("#0",text="Name", anchor = CENTER)
        self.tree.heading("#1",text="Price", anchor = CENTER)
        self.get_results()
        
        #Buttons
        ttk.Button(self.wind,text="DELETE",width=20,command=self.delete_product).grid(row=5,column=0,sticky = W+E)
        ttk.Button(self.wind,text="EDIT",width=20,command=self.edit_product).grid(row=5,column=1,sticky = W+E)
        ttk.Button(frame,text="Save product",command=self.add_product).grid(row=3,columnspan=2,sticky = W+E)
        
        
    def run_query(self,query,parameters =()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(query, parameters)

            conn.commit()
            result = cursor.fetchall()
        return result
        
    def get_results(self):
        query = 'SELECT * FROM product ORDER BY Name DESC'  
        db_rows = self.run_query(query)
        records = self.tree.get_children()

        for element in records:
            self.tree.delete(element)
            
        for row in db_rows:
            self.tree.insert("",0,text=row[1], values = row[2]) # Las "" indican que no tiene predecesor jerarquicamente. El 0 indica que es el primer elemento.
        
        
    
    def add_product(self):
        if self.validation():
            query = "INSERT INTO product VALUES (NULL,?,?)"
            parameters = (self.entry_name.get(),self.entry_price.get())
            self.run_query(query,parameters)
            self.label_alerts["fg"] = "green"
            self.label_alerts["text"] = "Product {} added successfully".format(self.entry_name.get())
            self.entry_name.delete(0,END)
            self.entry_price.delete(0,END)
        else:
            
            self.label_alerts["fg"] = "red"
            self.label_alerts["text"]= "Please, introduce a product to add to the list." #show a label indicating an error occurs
            
        self.get_results()
        
    def validation(self):
        return len(self.entry_name.get())!=0 and len(self.entry_price.get())!=0
    
    def delete_product(self):
        self.label_alerts["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0] #COMPRUEBA SI el item de la seleccion es valido. Si no se selecciona nada, no lo es.
        except IndexError as e:
            self.label_alerts["fg"] = "red"
            self.label_alerts["text"] = "Please select a record"
            return
        
        name = (self.tree.item(self.tree.selection())["text"])
        query = "DELETE FROM product WHERE Name=?"
        
        self.run_query(query,(name,))
        self.label_alerts["fg"] = "green"
        self.label_alerts["text"] = "Product {} deleted successfully".format(name)
        self.get_results()
    
    def edit_product(self):
        self.label_alerts["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0] #COMPRUEBA SI el item de la seleccion es valido. Si no se selecciona nada, no lo es.
        except IndexError as e:
            self.label_alerts["fg"] = "red"
            self.label_alerts["text"] = "Please select a record"
            return
        name = (self.tree.item(self.tree.selection())["text"])
        old_price = self.tree.item(self.tree.selection())["values"][0]
        old_name = self.tree.item(self.tree.selection())["text"]
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Edit product"
    
        #Old name
        Label(self.edit_wind,text="Old name: ").grid(row=0,column=0)
        Entry(self.edit_wind,state="readonly",textvariable=StringVar(self.edit_wind, value = old_name)).grid(row=0,column=1,sticky=W+E)
        
        #New Name
        Label(self.edit_wind,text="New name: ").grid(row=1,column=0)
        self.entry_new_name = Entry(self.edit_wind)
        self.entry_new_name.grid(row=1,column=1,sticky=W+E)
        
        #Old name
        Label(self.edit_wind,text="Old price: ").grid(row=2,column=0)
        Entry(self.edit_wind,state="readonly",textvariable=StringVar(self.edit_wind, value = old_price)).grid(row=2,column=1,sticky=W+E)
        
        #New Name
        Label(self.edit_wind,text="New price: ").grid(row=3,column=0)
        self.entry_new_price = Entry(self.edit_wind)
        self.entry_new_price.grid(row=3,column=1,sticky=W+E)        
        
        #Label Alert
        self.label_edit = Label(self.edit_wind,text="")
        self.label_edit.grid(row=4,column=0,columnspan=2)
        
        #Button update
        ttk.Button(self.edit_wind,text="Update",command=lambda:self.edit_records(self.entry_new_name.get(),old_name,self.entry_new_price.get(),old_price)).\
        grid(row=5,column=0,columnspan=2)
    
    def edit_records(self,new_name,old_name,new_price,old_price):
        if len(new_name)!=0 and len(new_price)!=0:
            query = "UPDATE product SET Name = ?, price = ? WHERE Name = ? AND Price = ?"        
            parameters = (new_name,new_price,old_name,old_price)
            self.run_query(query,parameters)
            self.edit_wind.destroy()
            self.label_alerts["fg"] = "green"
            self.label_alerts["text"] = "Product {} updated successfully".format(new_name)
            self.get_results()
        else:
            self.label_edit["fg"] = "Red"
            self.label_edit["text"] = "Introduce a Name and price"
        
if __name__ == "__main__":
    window = Tk()
    crud = Product(window)
    window.mainloop()   
