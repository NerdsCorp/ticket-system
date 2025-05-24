import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from printer import print_ticket
from arduino_comm import open_gate
from db import log_entry, log_exit
from onscreen_keyboard import OnScreenKeyboard
import qrcode

class TicketSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Parking Ticket System")
        self.geometry("480x320")
        self.attributes('-fullscreen', True)

        # Ticketless Entry
        tk.Label(self, text="Ticketless Entry (Phone):", font=("Arial", 16)).pack(pady=10)
        f1 = tk.Frame(self)
        f1.pack(pady=5)
        self.phone_entry = tk.Entry(f1, font=("Arial", 16), justify="center", width=14)
        self.phone_entry.pack(side="left")
        tk.Button(f1, text="Keyboard", font=("Arial", 12), command=lambda: self.open_keyboard(self.phone_entry)).pack(side="left", padx=5)
        tk.Button(self, text="Enter (Ticketless)", font=("Arial", 14), width=20, command=self.entry_ticketless).pack(pady=5)

        # Ticketed Entry
        tk.Label(self, text="Or", font=("Arial", 12)).pack(pady=2)
        tk.Button(self, text="Print Ticket & Enter", font=("Arial", 14), width=20, command=self.entry_ticketed).pack(pady=5)

        # Exit
        tk.Label(self, text="Exit (Phone or Ticket#):", font=("Arial", 16)).pack(pady=10)
        f2 = tk.Frame(self)
        f2.pack(pady=5)
        self.exit_entry = tk.Entry(f2, font=("Arial", 16), justify="center", width=14)
        self.exit_entry.pack(side="left")
        tk.Button(f2, text="Keyboard", font=("Arial", 12), command=lambda: self.open_keyboard(self.exit_entry)).pack(side="left", padx=5)
        tk.Button(self, text="Exit", font=("Arial", 14), width=20, command=self.exit_gate).pack(pady=5)

        self.qr_label = tk.Label(self)
        self.qr_label.pack(pady=5)
        self.ticket_code_label = tk.Label(self, font=("Arial", 14))
        self.ticket_code_label.pack(pady=2)

        tk.Button(self, text="Shutdown", font=("Arial", 10), command=self.shutdown, bg="red", fg="white").pack(side="bottom", fill="x")

    def open_keyboard(self, entry_widget):
        OnScreenKeyboard(self, entry_widget)

    def entry_ticketless(self):
        number = self.phone_entry.get()
        if not number.isdigit() or len(number) < 8:
            messagebox.showerror("Error", "Enter a valid phone number")
            return
        ticket_code = log_entry(phone=number, method="ticketless")
        open_gate(entry=True)
        self.display_ticket_code(ticket_code)
        self.phone_entry.delete(0, 'end')

    def entry_ticketed(self):
        ticket_code = log_entry(method="ticketed")
        print_ticket(ticket_code)
        open_gate(entry=True)
        self.display_ticket_code(ticket_code)

    def exit_gate(self):
        number = self.exit_entry.get()
        tid = log_exit(phone_or_ticket=number)
        if tid:
            open_gate(entry=False)
            messagebox.showinfo("Exit granted", f"Exit granted for {number}")
            self.exit_entry.delete(0, 'end')
        else:
            messagebox.showerror("Not found", "No entry found!")

    def display_ticket_code(self, ticket_code):
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(ticket_code)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img = img.resize((120, 120))
        self.qr_imgtk = ImageTk.PhotoImage(img)
        self.qr_label.configure(image=self.qr_imgtk)
        self.ticket_code_label.configure(text=f"Ticket Code: {ticket_code}")
        messagebox.showinfo("Ticket Issued", f"Present this QR code or enter Ticket Code:\n{ticket_code}")

    def shutdown(self):
        import os
        os.system("sudo shutdown now")

if __name__ == "__main__":
    app = TicketSystemApp()
    app.mainloop()