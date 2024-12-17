import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class CarRentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Închiriere Mașini")
        self.root.geometry("1980x1080")
        self.root.config(bg="#3A4C67")  # Fundal elegant în tonuri închise

        # Căutăm fișierele care conțin datele salvate
        self.cars_file = "cars.json"
        self.history_file = "history.json"

        # Încarcă datele la deschiderea aplicației
        self.cars = self.load_data(self.cars_file, [])
        self.rented_cars = []  # Lista mașinilor închiriate
        self.history = self.load_data(self.history_file, [])
        self.car_id = max([car["id"] for car in self.cars], default=0) + 1  # Generare ID unic pentru mașină
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Închiriere Mașini", font=("Arial", 28, "bold"), bg="#3A4C67", fg="white")
        title_label.pack(pady=30)

        button_frame = tk.Frame(self.root, bg="#3A4C67")
        button_frame.pack(pady=50)

        ttk.Button(button_frame, text="Adaugă Mașină", command=self.add_car_window, style="Rounded.TButton").grid(row=0, column=0, padx=20, pady=10)
        ttk.Button(button_frame, text="Vezi Mașinile Disponibile", command=self.view_available_cars, style="Rounded.TButton").grid(row=0, column=1, padx=20, pady=10)
        ttk.Button(button_frame, text="Închiriază Mașină", command=self.rent_car_window, style="Rounded.TButton").grid(row=1, column=0, padx=20, pady=10)
        ttk.Button(button_frame, text="Istoric Tranzacții", command=self.view_history, style="Rounded.TButton").grid(row=1, column=1, padx=20, pady=10)

        ttk.Button(self.root, text="Ieșire", command=self.exit_app, style="Rounded.TButton").pack(pady=30, side=tk.BOTTOM)

        # Frame pentru a arăta mașinile disponibile
        self.available_cars_frame = tk.Frame(self.root, bg="#3A4C67")
        self.available_cars_frame.pack(pady=20)

        self.style = ttk.Style()
        self.style.configure("Rounded.TButton", font=("Arial", 12, "bold"), padding=10, relief="flat", background="#6F8EAD", foreground="white", width=15)
        self.style.map("Rounded.TButton", background=[("active", "#5C7C99")])  # Culoare activă pentru butoane
        self.style.configure("Treeview", font=("Arial", 10), background="#F4F6F8", rowheight=30)
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#B1C4D4", foreground="#333333")

    def load_data(self, filename, default_data):
        """Încarcă datele din fișier sau returnează datele implicite dacă fișierul nu există."""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return default_data

    def save_data(self, filename, data):
        """Salvează datele într-un fișier."""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def add_car_window(self):
        window = tk.Toplevel(self.root)
        window.title("Adaugă Mașină")
        window.geometry("400x400")
        window.config(bg="#3A4C67")

        tk.Label(window, text="Marcă:", bg="#3A4C67", font=("Arial", 12, "bold"), fg="white").pack(pady=5)
        brand_entry = tk.Entry(window, font=("Arial", 12))
        brand_entry.pack(pady=5, padx=20)

        tk.Label(window, text="Model:", bg="#3A4C67", font=("Arial", 12, "bold"), fg="white").pack(pady=5)
        model_entry = tk.Entry(window, font=("Arial", 12))
        model_entry.pack(pady=5, padx=20)

        tk.Label(window, text="An:", bg="#3A4C67", font=("Arial", 12, "bold"), fg="white").pack(pady=5)
        year_entry = tk.Entry(window, font=("Arial", 12))
        year_entry.pack(pady=5, padx=20)

        tk.Label(window, text="Preț pe zi (RON):", bg="#3A4C67", font=("Arial", 12, "bold"), fg="white").pack(pady=5)
        price_entry = tk.Entry(window, font=("Arial", 12))
        price_entry.pack(pady=5, padx=20)

        def add_car():
            brand = brand_entry.get()
            model = model_entry.get()
            year = year_entry.get()
            price = price_entry.get()
            if brand and model and year.isdigit() and price.isdigit():
                self.cars.append({
                    "id": self.car_id,
                    "brand": brand,
                    "model": model,
                    "year": int(year),
                    "price": int(price),
                    "status": "disponibilă"
                })
                self.car_id += 1
                self.save_data(self.cars_file, self.cars)
                messagebox.showinfo("Succes", "Mașina a fost adăugată!")
                window.destroy()
            else:
                messagebox.showerror("Eroare", "Toate câmpurile trebuie completate corect!")

        ttk.Button(window, text="Adaugă", command=add_car, style="Rounded.TButton").pack(pady=20)

    def view_available_cars(self):
        # Curăță frame-ul anterior
        for widget in self.available_cars_frame.winfo_children():
            widget.destroy()

        # Creăm un Treeview pentru a afișa mașinile disponibile
        tree = ttk.Treeview(self.available_cars_frame, columns=("id", "brand", "model", "year", "price", "status"), show="headings", height=8)
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tree.heading("id", text="ID")
        tree.heading("brand", text="Marcă")
        tree.heading("model", text="Model")
        tree.heading("year", text="An")
        tree.heading("price", text="Preț pe zi (RON)")
        tree.heading("status", text="Status")
        
        for car in self.cars:
            tree.insert("", tk.END, values=(car["id"], car["brand"], car["model"], car["year"], car["price"], car["status"]))

        # Butonul de ștergere a unei mașini
        def delete_car():
            selected_item = tree.selection()
            if selected_item:
                car_id = tree.item(selected_item[0])['values'][0]  # ID-ul mașinii selectate
                # Găsim mașina corespunzătoare ID-ului selectat
                for car in self.cars:
                    if car["id"] == car_id:
                        self.cars.remove(car)  # Ștergem mașina din listă
                        self.save_data(self.cars_file, self.cars)
                        messagebox.showinfo("Succes", "Mașina a fost ștearsă!")
                        self.view_available_cars()  # Reîncarcă lista de mașini disponibile
                        return
            else:
                messagebox.showerror("Eroare", "Vă rugăm să selectați o mașină pentru a o șterge.")

        ttk.Button(self.available_cars_frame, text="Șterge Mașina Selectată", command=delete_car, style="Rounded.TButton").pack(pady=10)

    def rent_car_window(self):
        window = tk.Toplevel(self.root)
        window.title("Închiriere Mașină")
        window.geometry("400x450")
        window.config(bg="#3A4C67")

        tk.Label(window, text="ID Mașină:", bg="#3A4C67", font=("Arial", 12, "bold"), fg="white").pack(pady=10)
        id_entry = tk.Entry(window, font=("Arial", 12))
        id_entry.pack(pady=5, padx=20)

        tk.Label(window, text="Nume Client:", bg="#3A4C67", font=("Arial", 12, "bold"), fg="white").pack(pady=10)
        name_entry = tk.Entry(window, font=("Arial", 12))
        name_entry.pack(pady=5, padx=20)

        tk.Label(window, text="Număr Telefon:", bg="#3A4C67", font=("Arial", 12, "bold"), fg="white").pack(pady=10)
        phone_entry = tk.Entry(window, font=("Arial", 12))
        phone_entry.pack(pady=5, padx=20)

        tk.Label(window, text="Număr zile pentru închiriere:", bg="#3A4C67", font=("Arial", 12, "bold"), fg="white").pack(pady=10)
        days_entry = tk.Entry(window, font=("Arial", 12))
        days_entry.pack(pady=5, padx=20)

        def rent_car_action():
            car_id = id_entry.get()
            name = name_entry.get()
            phone = phone_entry.get()
            days = days_entry.get()
            if car_id and name and phone and days.isdigit():
                car_id = int(car_id)
                days = int(days)
                for car in self.cars:
                    if car["id"] == car_id and car["status"] == "disponibilă":
                        discount = 0
                        if days >= 10:
                            discount = 0.10 * car["price"] * days
                        total_price = car["price"] * days - discount
                        car["status"] = "închiriată"
                        self.rented_cars.append(car)
                        self.history.append({
                            "client_name": name,
                            "client_phone": phone,
                            "car_id": car["id"],
                            "car_details": f"{car['brand']} {car['model']} ({car['year']})",
                            "price_per_day": car["price"],
                            "days": days,
                            "total_price": total_price
                        })
                        self.save_data(self.history_file, self.history)
                        messagebox.showinfo("Succes", "Mașina a fost închiriată!")
                        window.destroy()
                        return
                messagebox.showerror("Eroare", "Mașina nu este disponibilă sau nu a fost găsită.")
            else:
                messagebox.showerror("Eroare", "Toate câmpurile trebuie completate corect!")

        ttk.Button(window, text="Închiriază", command=rent_car_action, style="Rounded.TButton").pack(pady=20)

    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Istoric Tranzacții")
        history_window.geometry("600x400")
        history_window.config(bg="#3A4C67")
        tree = ttk.Treeview(history_window, columns=("client_name", "car_details", "price_per_day", "days", "total_price"), show="headings", height=10)
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tree.heading("client_name", text="Nume Client")
        tree.heading("car_details", text="Detalii Mașină")
        tree.heading("price_per_day", text="Preț pe zi")
        tree.heading("days", text="Zile")
        tree.heading("total_price", text="Preț Total")
        
        for history_item in self.history:
            tree.insert("", tk.END, values=(history_item["client_name"], history_item["car_details"], history_item["price_per_day"], history_item["days"], history_item["total_price"]))

    def exit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CarRentalApp(root)
    root.mainloop()
