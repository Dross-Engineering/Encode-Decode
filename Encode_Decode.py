"""
░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░


░▒▓███████▓▒░░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓███████▓▒░░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░

Created by Hugo T 2024
"""

import random
import tkinter as tk
import re
import time
import string
from PIL import Image, ImageTk
import sys
import secrets

def encode(text, seed):
    seed = ''.join(str(ord(char)) for char in seed)     # Converts seed to a numeric code using HEX
    seed = str(int(seed)//11)                           # Divides seed by 11 to equalise integer distribution
    rand_offset = secrets.randbelow(25)/100             # Creates a random offset percentage below 35%
    pad_length1 = 7+secrets.randbelow(11+int(round((rand_offset+0.03)*len(text))))  # Creates pad 1
    pad_length2 = 5+secrets.randbelow(16+int(round((rand_offset+0.05)*len(text))))  # creates pad 2
    padded_text_raw = pad_length1 * "`/" + text + pad_length2 * "`/"  # pads text with '  '
    random.seed(seed)               # Sets random seed for random module. Key for reversing the encoding

    padded_text = ''
    for char in padded_text_raw:    # Converts new lines (\n) characters to ``@ so they survive the encoding step
        if char == '\n':
            char = '`%'
        padded_text += char

    encoded_text = ''
    for char in padded_text:        # Randomly maps each char to another valid char (Unicode 94-126) based on
        encoded_char = ord(char) + random.randint(0, 94)  # Random mapping changes for each char to prevent
        if encoded_char > 126:                                  # patterns being used to crack the cypher
            encoded_char -= 94
        encoded_text += chr(encoded_char)

    random.seed(str(int(seed) // 11))   # changing the random seed by dividing by a prime number

    encoded_text = list(encoded_text)   # Converting to list to allow for shuffling
    random.shuffle(encoded_text)        # Encoded text is shuffled, this will remove any potential remaining pattern
    shuffled_text = ''.join(encoded_text)
    return shuffled_text


def decode(encoded_text, seed):
    seed = ''.join(str(ord(char)) for char in seed)
    seed = str(int(seed)//11)
    random.seed(str(int(seed) // 11))
    original_order = list(range(len(encoded_text)))
    shuffled_order = original_order[:]
    random.shuffle(shuffled_order)
    unshuffled_text = ''.join([encoded_text[shuffled_order.index(i)] for i in original_order])

    random.seed(seed)
    decoded_text = ''
    for char in unshuffled_text:
        decoded_char = ord(char) - random.randint(0, 94)
        if decoded_char < 32:
            decoded_char += 94
        decoded_text += chr(decoded_char)
    decoded_text = decoded_text.replace('`%', '\n')
    return decoded_text.strip("`/")


def on_encode_button():
    text = text_entry.get("1.0", tk.END).strip()
    seed = seed_var.get().strip()
    encoded_text = encode(text, seed)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "ENCODED TEXT: \n" + encoded_text)


def on_decode_button():
    text = text_entry.get("1.0", tk.END).strip()
    seed = seed_var.get().strip()
    decoded_text = decode(text, seed)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "DECODED TEXT: \n" + decoded_text)


def update_seed_report(*args):  # determines quality of seed and length and updates message
    s = str(seed_var.get())
    score = 0
    # Check for character types
    has_lower = re.search(r'[a-z]', s) is not None
    has_upper = re.search(r'[A-Z]', s) is not None
    has_digit = re.search(r'\d', s) is not None
    has_symbol = re.search(r'[\W_]', s) is not None

    if has_lower:
        score += 1
    if has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_symbol:
        score += 1

    # Determine quality based on score
    if score <= 2 or len(seed_var.get()) < 9:
        seed_quality = "Bad"
    elif score <= 3 or len(seed_var.get()) < 16:
        seed_quality = "Poor"
    elif score == 4 and len(seed_var.get()) < 25:
        seed_quality = "Good"
    else:
        seed_quality = "Great"

    seed_details_label.config(text=f"Seed Length: {len(seed_var.get())}  |  Seed Quality: {seed_quality}")


def generate_seed():
    random.seed(time.time())
    characters = string.ascii_letters + string.digits + string.punctuation  # Letters, numbers, and special characters
    random_string = ''.join(secrets.choice(characters) for _ in range(256))
    seed_var.set(random_string)


def copy_seed():
    seed_text = seed_var.get()
    root.clipboard_clear()
    root.clipboard_append(seed_text)
    root.update()  # Keeps the clipboard content after the script ends


# Building the GUI ----------------------------------------------------

root = tk.Tk()
root.title("ENCODE/DECODE")     # Setting gui title

# Setting the gui icon
if getattr(sys, 'frozen', False):
    icon_path = sys._MEIPASS + "/icon.ico"
else:
    icon_path = "icon.ico"
icon_image = Image.open(icon_path)
tk_icon = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, tk_icon)

# Create a frame with padding
pad_frame = tk.Frame(root, padx=20, pady=15)
pad_frame.pack(fill=tk.BOTH, expand=True)

# Text entry
text_label = tk.Label(pad_frame, text="Enter Text:")
text_label.grid(row=0, column=0, sticky="w")
text_entry = tk.Text(pad_frame, height=5)
text_entry.grid(row=1, column=0, sticky="nsew")

# Seed entry
seed_var = tk.StringVar()
seed_var.trace_add("write", update_seed_report)
seed_label = tk.Label(pad_frame, text="Enter Seed Number:")
seed_label.grid(row=3, column=0, sticky="w")
seed_entry = tk.Entry(pad_frame, width=40, textvariable=seed_var, show='*')
seed_entry.grid(row=4, column=0, sticky="w")

# Add the "Generate" button next to the seed entry box
generate_button = tk.Button(pad_frame, text="Generate", command=generate_seed)
generate_button.grid(row=4, column=0, padx=(250, 0), sticky="w")

# Copy Seed Button
copy_button = tk.Button(pad_frame, text="Copy Seed", command=copy_seed)
copy_button.grid(row=4, column=0, sticky="w", padx=(315, 0))

# Seed Indicators
seed_details_label = tk.Label(pad_frame, text="Seed Length: 0  |  Seed Quality: Bad")
seed_details_label.grid(row=5, column=0, sticky='w')

# Encode and Decode buttons
generate_button = tk.Button(pad_frame, text="Encode", command=on_encode_button)
generate_button.grid(row=6, column=0, padx=(0, 0), pady=(2, 3), sticky="w")

generate_button = tk.Button(pad_frame, text="Decode", command=on_decode_button)
generate_button.grid(row=6, column=0, padx=(55, 0), pady=(2, 3), sticky="w")

# Output text
output_text = tk.Text(pad_frame, height=5)
output_text.grid(row=7, column=0, columnspan=2, sticky="nsew")

# Configure weights for resizing
pad_frame.grid_rowconfigure(1, weight=1)  # Text entry row
pad_frame.grid_rowconfigure(4, weight=0)  # Seed entry row
pad_frame.grid_rowconfigure(7, weight=1)  # Output text row
pad_frame.grid_columnconfigure(0, weight=1)  # Main column

root.geometry("450x400")
root.mainloop()
