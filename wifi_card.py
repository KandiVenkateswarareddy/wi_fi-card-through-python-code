import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import os

def update_qr_code(*args):
    ssid = ssid_entry.get()
    password = password_entry.get()
    
    if not ssid or not password:
        qr_label.config(image='')
        return
    
    # QR code data format: WIFI:T:WPA;S:<SSID>;P:<PASSWORD>;;
    qr_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill="black", back_color="white")
    
    # Convert QR code image for Tkinter
    qr_image = qr_image.resize((150, 150), Image.Resampling.LANCZOS)  # Smaller size to match image
    qr_photo = ImageTk.PhotoImage(qr_image)
    
    # Update the label with the new QR code
    qr_label.config(image=qr_photo)
    qr_label.image = qr_photo  # Keep a reference to avoid garbage collection
    
    # Save QR code for printing
    global qr_image_path
    qr_image.save("wifi_qr.png")
    qr_image_path = "wifi_qr.png"

def print_wifi_card():
    if 'qr_image_path' not in globals():
        messagebox.showwarning("Print Error", "Generate a QR code first!")
        return
    
    try:
        # Open the saved QR image
        img = Image.open(qr_image_path)
        img.show()  # Opens in default viewer for printing
    except Exception as e:
        messagebox.showerror("Print Error", f"Failed to print: {str(e)}")

# Create the main window
window = tk.Tk()
window.title("WiFi Card Generator")
window.geometry("300x400")
window.configure(bg="#000000")  # Black background

# Frame for WiFi Login
frame = tk.Frame(window, bg="#000000", padx=10, pady=10)
frame.pack(expand=True)

# WiFi Login Label
tk.Label(frame, text="WiFi Login", font=("Arial", 14), fg="#1E90FF", bg="#000000").grid(row=0, column=0, columnspan=2, pady=5)

# Network name
tk.Label(frame, text="Network name", fg="#1E90FF", bg="#000000").grid(row=1, column=0, sticky="e", pady=2)
ssid_entry = tk.Entry(frame, bg="#000000", fg="#1E90FF", insertbackground="#1E90FF")
ssid_entry.grid(row=1, column=1, pady=2)
ssid_entry.bind('<KeyRelease>', update_qr_code)  # Update QR code on key release

# Password
tk.Label(frame, text="Password", fg="#1E90FF", bg="#000000").grid(row=2, column=0, sticky="e", pady=2)
password_entry = tk.Entry(frame, show="*", bg="#000000", fg="#1E90FF", insertbackground="#1E90FF")
password_entry.grid(row=2, column=1, pady=2)
password_entry.bind('<KeyRelease>', update_qr_code)  # Update QR code on key release

# QR Code Label
qr_label = tk.Label(frame, bg="#000000")
qr_label.grid(row=3, column=0, columnspan=2, pady=10)

# Instruction
tk.Label(frame, text="Point your phone's camera at the QR code to connect to WiFi", 
         fg="#1E90FF", bg="#000000", wraplength=250).grid(row=4, column=0, columnspan=2, pady=5)

# Buttons Frame
button_frame = tk.Frame(frame, bg="#000000")
button_frame.grid(row=5, column=0, columnspan=2, pady=10)

# Generate Button (hidden as QR updates in real-time)
# generate_button = tk.Button(button_frame, text="Generate QR Code", command=update_qr_code, bg="#1E90FF", fg="#000000")
# generate_button.pack(side=tk.LEFT, padx=5)

# Print Button
print_button = tk.Button(button_frame, text="Print WiFi Card", command=print_wifi_card, bg="#1E90FF", fg="#000000")
print_button.pack(side=tk.LEFT, padx=5)

# Initial call to clear QR label
update_qr_code()

# Start the application
window.mainloop()

# Clean up temporary file on exit
if 'qr_image_path' in globals():
    try:
        os.remove(qr_image_path)
    except:
        pass