import tkinter as tk

class Labelframe1(tk.LabelFrame):
    def __init__(self, master, callback):
        super().__init__(master, text="Labelframe 1")
        self.callback = callback

        self.button = tk.Button(self, text="Afficher Labelframe 2", command=self.show_next_labelframe)
        self.button.pack(padx=10, pady=10)

    def show_next_labelframe(self):
        self.button.destroy()
        self.callback()

class Labelframe2(tk.LabelFrame):
    def __init__(self, master, callback):
        super().__init__(master, text="Labelframe 2")
        self.callback = callback

        self.button = tk.Button(self, text="Afficher Labelframe 3", command=self.show_next_labelframe)
        self.button.pack(padx=10, pady=10)

    def show_next_labelframe(self):
        self.button.destroy()
        self.callback()

class Labelframe3(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Labelframe 3")
        # Ajoutez ici le contenu spécifique au Labelframe 3 si nécessaire

def main():
    root = tk.Tk()
    app = Application(root)
    root.geometry("300x200")
    root.mainloop()

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Application Tkinter")

        self.labelframe1 = Labelframe1(master, self.show_labelframe2)
        self.labelframe1.pack(padx=10, pady=10)

    def show_labelframe2(self):
        self.labelframe1.destroy()

        self.labelframe2 = Labelframe2(self.master, self.show_labelframe3)
        self.labelframe2.pack(padx=10, pady=10)
        self.master.geometry("400x300")

    def show_labelframe3(self):
        self.labelframe2.destroy()

        labelframe3 = Labelframe3(self.master)
        labelframe3.pack(padx=10, pady=10)
        self.master.geometry("500x400")

if __name__ == "__main__":
    main()