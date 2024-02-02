import tkinter as tk
from tkinter import simpledialog

class PasswordDialog(tk.simpledialog.Dialog):
    def __init__(self, parent):
        self.password = "1234"
        tk.simpledialog.Dialog.__init__(self, parent, title="Mot de passe")

    def body(self, master):
        tk.Label(master, text="Veuillez entrer le mot de passe :").grid(row=0)
        self.entry = tk.Entry(master, show="*")
        self.entry.grid(row=1)
        return self.entry.grid(row=1)
    
    def cancel_pressed(self):
        self.destroy()
        
    

    def apply(self):
        self.password = self.entry.get()
    