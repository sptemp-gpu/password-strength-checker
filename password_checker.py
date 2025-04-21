import tkinter as tk
from tkinter import messagebox
import re
import requests
import hashlib
import random
import string

# Function to load images/icons
def load_image(image_path):
    try:
        return tk.PhotoImage(file=image_path)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# Load icons for UI (provide correct paths to icons)
lock_icon = load_image("lock_icon.png")  # Ensure you have the correct path to your image
check_icon = load_image("check_icon.png")
warning_icon = load_image("warning_icon.png")

# Function to check password length
def check_length(password, min_length=8):
    return len(password) >= min_length

# Function to check password complexity (lowercase, uppercase, digit, special character)
def check_complexity(password):
    return (re.search(r"[a-z]", password) and
            re.search(r"[A-Z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[\W_]", password))

# Function to check if password is in a common password list
def check_common_password(password):
    common_passwords = [
        '123456', 'password', '123456789', '12345', '12345678', 'qwerty', 'abc123', 'password1', '123123'
    ]
    return password in common_passwords

# Function to check if password has been involved in a breach (using Have I Been Pwned API)
def check_breach(password):
    try:
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        
        if response.status_code == 200:
            hashes = response.text.splitlines()
            for hash in hashes:
                if hash.split(':')[0] == suffix:
                    return True  # Password is breached
        return False  # Password is not breached
    except requests.exceptions.RequestException as e:
        print(f"Error checking breach status: {e}")
        return False  # Treat as safe if request fails

# Function to check password strength
def check_strength(password):
    if check_common_password(password):
        return "This password is too common. Please choose a different one.", warning_icon
    
    if check_breach(password):
        return "This password has been involved in a data breach. Please choose a different one.", warning_icon

    if not check_length(password):
        return "Password is too short. It should be at least 8 characters long.", warning_icon
    
    if not check_complexity(password):
        return "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.", warning_icon
    
    return "Password is strong.", check_icon

# Function to provide real-time suggestions for password improvement
def suggest_password(password):
    suggestions = []
    
    if len(password) < 12:
        suggestions.append("Consider making your password at least 12 characters long.")
    if not re.search(r"[a-z]", password):
        suggestions.append("Add at least one lowercase letter.")
    if not re.search(r"[A-Z]", password):
        suggestions.append("Add at least one uppercase letter.")
    if not re.search(r"[0-9]", password):
        suggestions.append("Add at least one number.")
    if not re.search(r"[\W_]", password):
        suggestions.append("Add at least one special character (e.g., !, @, #, $).")
    
    return "\n".join(suggestions)

# Function to update password strength label and suggestions in real-time
def update_strength():
    password = password_entry.get()
    strength, icon = check_strength(password)
    suggestions = suggest_password(password)
    
    strength_label.config(text=strength, fg="green" if "strong" in strength else "red")
    suggestions_label.config(text=suggestions)
    strength_icon_label.config(image=icon)

# Function to generate a random strong password
def generate_password():
    length = random.randint(12, 16)  # Password length between 12 and 16 characters
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    
    password_entry.delete(0, tk.END)  # Clear any current text in the entry
    password_entry.insert(0, password)  # Insert the generated password

# Create the main window
root = tk.Tk()
root.title("Password Strength Checker")

# Configure window size and background color
root.geometry("400x450")
root.configure(bg="#f0f0f0")

# Create and place components with styling
password_label = tk.Label(root, text="Enter your password:", font=("Arial", 12), bg="#f0f0f0")
password_label.pack(pady=10)

icon_label = tk.Label(root, image=lock_icon, bg="#f0f0f0")  # Icon label
icon_label.pack()

password_entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))
password_entry.pack(pady=5)

strength_label = tk.Label(root, text="Password strength will appear here.", fg="red", font=("Arial", 12), bg="#f0f0f0")
strength_label.pack(pady=20)

strength_icon_label = tk.Label(root, image=warning_icon, bg="#f0f0f0")  # Icon for strength feedback
strength_icon_label.pack()

suggestions_label = tk.Label(root, text="Suggestions will appear here.", fg="blue", font=("Arial", 12), bg="#f0f0f0")
suggestions_label.pack(pady=10)

generate_button = tk.Button(root, text="Generate Strong Password", command=generate_password, font=("Arial", 12), bg="#4CAF50", fg="white")
generate_button.pack(pady=10)

# Bind the entry widget to update strength in real-time as the user types
password_entry.bind("<KeyRelease>", lambda event: update_strength())

# Start the Tkinter event loop
root.mainloop()
