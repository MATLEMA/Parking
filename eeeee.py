import tkinter as tk

def on_select(event):
    # Effacer les anciens widgets (boutons et labels)
    for widget in frame_widgets.winfo_children():
        widget.destroy()

    # Récupérer l'élément sélectionné dans la Listbox
    selected_item = listbox.get(listbox.curselection())
    
    # Afficher de nouveaux widgets en fonction de l'élément sélectionné
    label = tk.Label(frame_widgets, text=f"Produit sélectionné : {selected_item}")
    label.pack()

    # Ajouter d'autres widgets (boutons, labels) en fonction de vos besoins

# Créer la fenêtre principale
root = tk.Tk()
root.title("Sélection de produit")

# Créer une Listbox
listbox = tk.Listbox(root)
listbox.pack()

# Ajouter des éléments à la Listbox
produits = ["Produit 1", "Produit 2", "Produit 3"]
for produit in produits:
    listbox.insert(tk.END, produit)

# Associer la fonction on_select à l'événement de sélection dans la Listbox
listbox.bind("<<ListboxSelect>>", on_select)

# Créer un cadre pour les widgets à côté de la Listbox
frame_widgets = tk.Frame(root)
frame_widgets.pack()

# Lancer la boucle principale Tkinter
root.mainloop()