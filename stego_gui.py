import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkFont
from stego.image_stego import hide_text_in_image, extract_text_from_image
from stego.audio_stego import hide_text_in_audio, extract_text_from_audio
import os

# ---------------- Functions ----------------

def hide_message():
    filetype = filetype_var.get()
    input_file = filedialog.askopenfilename(
        title="Select input file",
        filetypes=[("Image files", "*.png *.jpg *.bmp"), ("Audio files", "*.wav"), ("All files", "*.*")]
    )
    if not input_file:
        return

    output_file = filedialog.asksaveasfilename(
        title="Save stego file as",
        defaultextension=".png" if filetype == "image" else ".wav"
    )
    if not output_file:
        return

    message = msg_entry.get("1.0", tk.END).strip()
    password = pwd_entry.get().strip()

    try:
        if filetype == "image":
            hide_text_in_image(input_file, output_file, message, password if password else None)
        else:
            hide_text_in_audio(input_file, output_file, message, password if password else None)

        messagebox.showinfo("Success", f"Message hidden in {os.path.basename(output_file)}")

        # Reset input fields after success
        msg_entry.delete("1.0", tk.END)
        pwd_entry.delete(0, tk.END)

        # Clear previous output
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def extract_message():
    filetype = filetype_var.get()
    input_file = filedialog.askopenfilename(
        title="Select stego file",
        filetypes=[("Image files", "*.png *.jpg *.bmp"), ("Audio files", "*.wav"), ("All files", "*.*")]
    )
    if not input_file:
        return

    password = pwd_entry.get().strip()

    try:
        if filetype == "image":
            secret = extract_text_from_image(input_file, password if password else None)
        else:
            secret = extract_text_from_audio(input_file, password if password else None)

        # Remove unwanted characters from audio extraction
        secret = secret.replace("\x00", "").strip()

        # Check if decryption failed
        if password and not secret:
            raise ValueError("Incorrect password")

        # Display extracted message in fixed Text box
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, secret)
        output_text.config(state="disabled")

        # Reset password field
        pwd_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Incorrect password!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def toggle_password():
    if show_pwd_var.get():
        pwd_entry.config(show="")
    else:
        pwd_entry.config(show="*")


# ---------------- GUI Setup ----------------

root = tk.Tk()
root.title("Steganography Tool")
root.geometry("500x600")

# Filetype (radio buttons)
filetype_var = tk.StringVar(value="image")
tk.Label(root, text="Choose File Type:", font=("Arial", 12, "bold")).pack(pady=5)
tk.Radiobutton(root, text="Image", variable=filetype_var, value="image").pack()
tk.Radiobutton(root, text="Audio", variable=filetype_var, value="audio").pack()

# Password entry
tk.Label(root, text="Password (optional):", font=("Arial", 10)).pack(pady=5)
pwd_entry = tk.Entry(root, show="*")
pwd_entry.pack(fill="x", padx=20)

# Show/hide password toggle
show_pwd_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Show Password", variable=show_pwd_var, command=toggle_password).pack(pady=2)

# Message box for hiding
text_font = tkFont.Font(family="Arial", size=14)
tk.Label(root, text="Message (only for Hide):", font=("Arial", 10)).pack(pady=5)
msg_entry = tk.Text(root, height=6, font=text_font)
msg_entry.pack(fill="both", expand=True, padx=20)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Hide Message", command=hide_message, width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Extract Message", command=extract_message, width=15, bg="#2196F3", fg="white").grid(row=0, column=1, padx=10)

# Fixed Text box for extracted message
tk.Label(root, text="Extracted Message:", font=("Arial", 14, "bold")).pack(pady=5)
output_text = tk.Text(root, height=6, font=text_font)
output_text.pack(fill="both", expand=True, padx=20)
output_text.config(state="disabled")

root.mainloop()
