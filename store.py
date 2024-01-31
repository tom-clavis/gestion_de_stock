import mysql.connector
from tkinter import Tk, Label, Button, Entry, Listbox, messagebox

class GestionStock:
    def __init__(self,root):
        self.root = root
        self.root.title("Gestion de Stock")
        
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="store"
        )
        self.cursor = self.conn.cursor()
        
        self.label = Label(root, text="Liste des Produits en Stock")
        self.label.pack()

        self.product_listbox = Listbox(root)
        self.product_listbox.pack()

        self.category_var = StringVar()
        self.category_var.set("Toutes les Catégories")

        self.category_option = OptionMenu(root, self.category_var, "Toutes les Catégories")
        self.category_option.pack()

        self.add_button = Button(root, text="Ajouter Produit", command=self.add_product)
        self.add_button.pack()

        self.remove_button = Button(root, text="Supprimer Produit", command=self.remove_product)
        self.remove_button.pack()

        self.modify_button = Button(root, text="Modifier Produit", command=self.modify_product)
        self.modify_button.pack()

        
        self.load_categories()
        self.load_products()
        
    
    def load_categories(self):
        self.category_var.set("Toutes les Catégories")
        self.cursor.execute("SELECT name FROM category")
        categories = [category[0] for category in self.cursor.fetchall()]
        self.category_option['menu'].delete(0, 'end')
        self.category_option['menu'].add_command(label="Toutes les Catégories", command=lambda: self.filter_products(None))
        for category in categories:
            self.category_option['menu'].add_command(label=category, command=lambda cat=category: self.filter_products(cat))

    def filter_products(self, category):
        self.product_listbox.delete(0, 'end')
        if category is None or category == "Toutes les Catégories":
            self.cursor.execute("SELECT id, name, price, quantity FROM product")
        else:
            self.cursor.execute("SELECT id, name, price, quantity FROM product WHERE id_category = (SELECT id FROM category WHERE name = %s)", (category,))
        products = self.cursor.fetchall()
        for product in products:
            self.product_listbox.insert('end', f"{product[1]} - Prix: {product[2]} - Stock: {product[3]} (ID: {product[0]})")
            
    