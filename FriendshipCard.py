import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

def show_message():
    messagebox.showinfo("💖 Message", "A true friend is someone who reaches for your hand and touches your heart 🤝💗")

def on_enter(e):
    btn.config(bg="#ff69b4", fg="white")

def on_leave(e):
    btn.config(bg="#ffc0cb", fg="black")

def create_heart():
    heart = tk.Label(root, text="💖", bg="#fdf6fa", font=("Arial", 16))
    x = random.randint(50, 550)
    heart.place(x=x, y=0)
    animate_heart(heart, 0)

def animate_heart(heart, y):
    if y < 420:
        heart.place(y=y+3)
        root.after(60, lambda: animate_heart(heart, y+3))
    else:
        heart.destroy()

def start_heart_animation():
    create_heart()
    root.after(800, start_heart_animation)

# Main window
root = tk.Tk()
root.title("💝 Friendship Card")
root.geometry("600x460")
root.configure(bg="#fdf6fa")  # Soft floral background

# Card Frame
outer_frame = tk.Frame(root, bg="#ffe0ec", bd=0)
outer_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=330)

card = tk.Frame(outer_frame, bg="white", bd=0, highlightbackground="#ffaad4", highlightthickness=5)
card.place(relx=0.5, rely=0.5, anchor="center", width=480, height=310)

# Title
title = tk.Label(card, text="💞 Happy Friendship Day 💞", font=("Segoe Script", 22, "bold"), bg="white", fg="#d63384")
title.pack(pady=(20, 5))

# Load Handshake Image
try:
    img = Image.open("handshake.png").resize((80, 80))
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(card, image=photo, bg="white")
    img_label.image = photo
    img_label.pack(pady=(0, 10))
except Exception as e:
    img_label = tk.Label(card, text="🤝", font=("Arial", 40), bg="white")
    img_label.pack(pady=(0, 10))

# Message
message = tk.Label(card, text="Together we share, care, and grow.\nThanks for your friendship 🌸", 
                   font=("Georgia", 13), bg="white", fg="#6f42c1", justify="center")
message.pack(pady=5)

# Button
btn = tk.Button(card, text="🎁 Open Message", font=("Arial", 12, "bold"),
                bg="#ffc0cb", fg="black", bd=0, padx=20, pady=8, relief="raised", cursor="hand2", command=show_message)
btn.pack(pady=15)
btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

# Footer
footer = tk.Label(root, text="Created with ❤️ using Python", font=("Verdana", 9, "italic"), bg="#fdf6fa", fg="#b95e96")
footer.pack(side="bottom", pady=8)

# Start hearts
start_heart_animation()

# Run app
root.mainloop()
