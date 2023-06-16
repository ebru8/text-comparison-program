import tkinter as tk
from tkinter import filedialog
from difflib import Differ
import os
import threading
import matplotlib.pyplot as plt

def select_file_1():
    file_path = filedialog.askopenfilename(filetypes=(("Text files", "*.yml *.txt *.csv *.xlsx"), ("All files", "*.*")))
    entry_file_1.delete(0, tk.END)
    entry_file_1.insert(tk.END, file_path)

def select_file_2():
    file_path = filedialog.askopenfilename(filetypes=(("Text files", "*.yml *.txt *.csv *.xlsx"), ("All files", "*.*")))
    entry_file_2.delete(0, tk.END)
    entry_file_2.insert(tk.END, file_path)

def compare_files():
    file_path_1 = entry_file_1.get()
    file_path_2 = entry_file_2.get()

    if not file_path_1 or not file_path_2:
        return

    extension_1 = os.path.splitext(file_path_1)[1][1:]
    extension_2 = os.path.splitext(file_path_2)[1][1:]

    valid_extensions = ['yml', 'txt', 'csv', 'xlsx']

    if extension_1 not in valid_extensions or extension_2 not in valid_extensions:
        result_label.config(text="Invalid file format")
        return

    threading.Thread(target=compare_files_threaded, args=(file_path_1, file_path_2)).start()

def compare_files_threaded(file_path_1, file_path_2):
    with open(file_path_1, 'r') as file1, open(file_path_2, 'r') as file2:
        text1 = file1.readlines()
        text2 = file2.readlines()

    differ = Differ()
    diff = list(differ.compare(text1, text2))
    diff_count = sum(1 for line in diff if line.startswith('+') or line.startswith('-'))

    root.after(0, update_result_label, diff_count)
    root.after(0, save_report, diff)

def update_result_label(diff_count):
    result_label.config(text=f"Number of different words: {diff_count}")
    details_button.config(state=tk.NORMAL)

def save_report(diff):
    file_path = os.path.expanduser("~/Desktop/comparison_report.txt")

    with open(file_path, 'w') as file:
        file.writelines(diff)

    result_label.config(text=f"Report saved to: {file_path}")

def show_details():
    file_path_1 = entry_file_1.get()
    file_path_2 = entry_file_2.get()

    if not file_path_1 or not file_path_2:
        return

    with open(file_path_1, 'r') as file1, open(file_path_2, 'r') as file2:
        text1 = file1.readlines()
        text2 = file2.readlines()

    line_count_1 = len(text1)
    line_count_2 = len(text2)

    x = ['File 1', 'File 2']
    y = [line_count_1, line_count_2]

    plt.bar(x, y)
    plt.xlabel('Files')
    plt.ylabel('Line Count')
    plt.title('Line Count Comparison')

    plt.show()

root = tk.Tk()
root.title("Text Comparison Program")

label_file_1 = tk.Label(root, text="File 1:")
label_file_1.pack()

entry_file_1 = tk.Entry(root, width=50)
entry_file_1.pack()

button_file_1 = tk.Button(root, text="Select", command=select_file_1)
button_file_1.pack()

label_file_2 = tk.Label(root, text="File 2:")
label_file_2.pack()

entry_file_2 = tk.Entry(root, width=50)
entry_file_2.pack()

button_file_2 = tk.Button(root, text="Select", command=select_file_2)
button_file_2.pack()

compare_button = tk.Button(root, text="Compare", command=compare_files)
compare_button.pack()

result_label = tk.Label(root)
result_label.pack()

details_button = tk.Button(root, text="Detaylar", command=show_details, state=tk.DISABLED)
details_button.pack()

root.mainloop()