import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import Tk, Label, Button, Entry, Listbox, messagebox
#from mdp import PasswordDialog#
import tkinter.simpledialog

class StockManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock")
        
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="store"
        )
        self.cursor = self.db_connection.cursor()

        
        self.create_gui()
        
        #password_dialog = PasswordDialog(root)
        #if password_dialog.password != "votre_mot_de_passe":
            #tk.messagebox.showerror("Mot de passe incorrect", "Le mot de passe est incorrect. Fermeture de l'application.")
            #root.destroy()
            #return

    def create_gui(self):
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("ID", "Nom", "Description", "Prix", "Quantité", "Catégorie")
        self.tree.heading("#0", text="", anchor="w")
        self.tree.column("#0", anchor="w", width=0)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=100)
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        add_button = tk.Button(self.root, text="Ajouter", command=self.add_product)
        add_button.grid(row=1, column=0, padx=10, pady=5)
        
        delete_button = tk.Button(self.root, text="Supprimer", command=self.delete_product)
        delete_button.grid(row=1, column=1, padx=10, pady=5)
        
        edit_button = tk.Button(self.root, text="Modifier", command=self.edit_product)
        edit_button.grid(row=1, column=2, padx=10, pady=5)

        # Chargement des données
        self.load_data()

    def load_data(self):
        self.cursor.execute("SELECT * FROM product INNER JOIN category ON product.id_category = category.id")
        products = self.cursor.fetchall()

        for row in self.tree.get_children():
            self.tree.delete(row)

        
        for product in products:
            self.tree.insert("", "end", values=product)

    def add_product(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Ajouter un produit")

        name_label = tk.Label(add_window, text="Nom:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        description_label = tk.Label(add_window, text="Description:")
        description_label.grid(row=1, column=0, padx=10, pady=5)
        description_entry = tk.Entry(add_window)
        description_entry.grid(row=1, column=1, padx=10, pady=5)

        price_label = tk.Label(add_window, text="Prix:")
        price_label.grid(row=2, column=0, padx=10, pady=5)
        price_entry = tk.Entry(add_window)
        price_entry.grid(row=2, column=1, padx=10, pady=5)

        quantity_label = tk.Label(add_window, text="Quantité:")
        quantity_label.grid(row=3, column=0, padx=10, pady=5)
        quantity_entry = tk.Entry(add_window)
        quantity_entry.grid(row=3, column=1, padx=10, pady=5)

        category_label = tk.Label(add_window, text="Catégorie:")
        category_label.grid(row=4, column=0, padx=10, pady=5)
        category_entry = tk.Entry(add_window)
        category_entry.grid(row=4, column=1, padx=10, pady=5)

        def add_product_to_db():
            try:
                name = name_entry.get()
                description = description_entry.get()
                price = int(price_entry.get())
                quantity = int(quantity_entry.get())
                category = int(category_entry.get())

                self.cursor.execute("INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)",
                                    (name, description, price, quantity, category))
                self.db_connection.commit()

                self.load_data()

                add_window.destroy()

            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit : {e}")

        
        add_button = tk.Button(add_window, text="Ajouter", command=add_product_to_db)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)

        

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à supprimer.")
            return

        confirmation = tk.messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce produit?")
        if confirmation:
            try:
                product_id = self.tree.item(selected_item)['values'][0]

                self.cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
                self.db_connection.commit()

                self.load_data()

            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit : {e}")


    def edit_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à modifier.")
            return

        product_info = self.tree.item(selected_item)['values']

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Modifier un produit")

        name_label = tk.Label(edit_window, text="Nom:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(edit_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.insert(0, product_info[1])  

        description_label = tk.Label(edit_window, text="Description:")
        description_label.grid(row=1, column=0, padx=10, pady=5)
        description_entry = tk.Entry(edit_window)
        description_entry.grid(row=1, column=1, padx=10, pady=5)
        description_entry.insert(0, product_info[2])  

        price_label = tk.Label(edit_window, text="Prix:")
        price_label.grid(row=2, column=0, padx=10, pady=5)
        price_entry = tk.Entry(edit_window)
        price_entry.grid(row=2, column=1, padx=10, pady=5)
        price_entry.insert(0, product_info[3])  

        quantity_label = tk.Label(edit_window, text="Quantité:")
        quantity_label.grid(row=3, column=0, padx=10, pady=5)
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.grid(row=3, column=1, padx=10, pady=5)
        quantity_entry.insert(0, product_info[4])  

        category_label = tk.Label(edit_window, text="Catégorie:")
        category_label.grid(row=4, column=0, padx=10, pady=5)
        category_entry = tk.Entry(edit_window)
        category_entry.grid(row=4, column=1, padx=10, pady=5)
        category_entry.insert(0, product_info[6])  

        
        def edit_product_in_db():
            try:
                new_name = name_entry.get()
                new_description = description_entry.get()
                new_price = int(price_entry.get())
                new_quantity = int(quantity_entry.get())
                new_category = int(category_entry.get())

                self.cursor.execute("UPDATE product SET name=%s, description=%s, price=%s, quantity=%s, id_category=%s WHERE id=%s",
                                    (new_name, new_description, new_price, new_quantity, new_category, product_info[0]))
                self.db_connection.commit()

                self.load_data()

                edit_window.destroy()

            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Erreur lors de la modification du produit : {e}")

        edit_button = tk.Button(edit_window, text="Modifier", command=edit_product_in_db)
        edit_button.grid(row=5, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockManagementApp(root)
    root.mainloop()
