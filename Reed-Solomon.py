"""
Team: REED-SOLOMON ENCODERS

Rolls:  
 	
2203119, 2203121, 2203126

"""


# do:  `pip install numpy tkinter` inside your terminal if you are getting `no module named SOMETHIGN` error

import tkinter as tk
from tkinter import messagebox
import numpy as np

parity_matrix = None # Global parity generator matrix
parity_matrix_check = False # Is the matrix generated?

def generate_parity_matrix():
    global parity_matrix, parity_matrix_check
    try:
        n = int(get_n.get())
        k = int(get_k.get())
        q = int(q_entry.get())
        if not is_prime(q):
            messagebox.showerror("Error", f"q = {q} is not a prime number.")
            return
        
        alpha = [i for i in range(n)]

        generated_matrix = []
        for i in range(k):
            temp = []
            for j in range(n):
                temp.append(pow(alpha[j], i, q))
            generated_matrix.append(temp)

        parity_matrix = np.array(generated_matrix) % q
        
        display_matrix()
        parity_matrix_check = True
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values for n, k, and q.")

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True
    
def display_matrix():
    for widget in matrix_frame.winfo_children():
        widget.destroy()
    
    rows, cols = parity_matrix.shape
    for i in range(rows):
        for j in range(cols):
            label = tk.Label(matrix_frame, text=str(parity_matrix[i, j]), borderwidth=1, relief="solid", width=5)
            label.grid(row=i, column=j)

def swap_columns():
    global parity_matrix_check
    try:
        col1 = int(col1_index.get())-1 ## one indexing
        col2 = int(col2_index.get())-1 ## one indexing
        
        if parity_matrix_check == False:
            messagebox.showerror("Error", "Generate parity generator matrix first.")
            return
        if col1 < 0 or col2 < 0 or col1 >= parity_matrix.shape[1] or col2 >= parity_matrix.shape[1]:
            messagebox.showerror("Error", "Invalid column indices. Add \"1-indexed\" indices.")
            return
        
        parity_matrix[:, [col1, col2]] = parity_matrix[:, [col2, col1]]
        display_matrix()
        
        try:
            message = list(map(int , get_message.get().split()))
            k = int(get_k.get())
            q = int(q_entry.get())
            if len(message) != k:
                return
            
            encoded = np.dot(message, parity_matrix) % q
            display_codeword(encoded)
        except:
            return

    except ValueError:
        messagebox.showerror("Error", "Please enter valid column indices.")

def encode_message():
    try:
        message = list(map(int , get_message.get().split()))
        k = int(get_k.get())
        q = int(q_entry.get())
        if len(message) != k:
            messagebox.showerror("Error", "Message length must match k.")
            return
        
        for m in message:
            if(m >= q):
                messagebox.showerror("Error", f"Message is not in accordance with the field. They should be modulo {q}.")
                return
        
        encoded_word = np.dot(message, parity_matrix) % q
        display_codeword(encoded_word)
    except ValueError:
        messagebox.showerror("Error", "Invalid message input. Please enter space-separated integers.")

def display_codeword(codeword):
    codeword_display.config(text=" ".join(map(str, codeword)))

####################################################  GUI  ####################################################

root = tk.Tk()
root.title("Reed-Solomon Encoder")

# Input n q k
tk.Label(root, text="n = q (Code length = prime):").grid(row=0, column=0)
get_n = q_entry = tk.Entry(root)
get_n.grid(row=0, column=1)

tk.Label(root, text="k (Message length):").grid(row=1, column=0)
get_k = tk.Entry(root)
get_k.grid(row=1, column=1)

# Generate matrix 
matrix_generate_button = tk.Button(root, text="Generate Parity Matrix", command=generate_parity_matrix)
matrix_generate_button.grid(row=2, columnspan=2)

# Parity matrix 
matrix_frame = tk.Frame(root)
matrix_frame.grid(row=3, columnspan=2)

# Column swapper
swap_button = tk.Button(root, text="Swap and Encode", command=swap_columns)
swap_button.grid(row=4, columnspan=2)

tk.Label(root, text="Column 1:").grid(row=5, column=0)
col1_index = tk.Entry(root, width=5)
col1_index.grid(row=5, column=1)

tk.Label(root, text="Column 2:").grid(row=6, column=0)
col2_index = tk.Entry(root, width=5)
col2_index.grid(row=6, column=1)

# Message input
tk.Label(root, text="Message (space-separated values):").grid(row=7, column=0)
get_message = tk.Entry(root, width=30)
get_message.grid(row=7, column=1)


# Encode button
encode_button = tk.Button(root, text="Encode Message", command=encode_message)
encode_button.grid(row=8, columnspan=2)

# Encoded codeword 
codeword_label = tk.Label(root, text="Encoded Codeword:")
codeword_label.grid(row=9, column=0)
codeword_display = tk.Label(root, text="", relief="solid", width=40)
codeword_display.grid(row=9, column=1)

root.mainloop()