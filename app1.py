
from flask import Flask, render_template
import tkinter as tk
from tkinter import messagebox

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_python_code')
def run_python_code():
    # Your Python code using Tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Example: Display a Tkinter messagebox
    messagebox.showinfo("Python Code", "Hello from Python!")

    return "Python code executed successfully"

if __name__ == '__main__':
    app.run(debug=True)
