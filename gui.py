import tkinter as tk
from PIL import Image, ImageTk
import neat_test_file
import threading
import sys

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Auto-scroll to the end

    def flush(self):
        pass  # Not needed, but required for sys.stdout compatibility

def run_test(spinner_label, output_text):
    # Show the spinner while the test is running
    spinner_label.after(100, rotate_spinner, spinner_label, 0)

    def task():
        # Redirect stdout to the tkinter Text widget
        sys.stdout = TextRedirector(output_text)

        print("Starting test...")
        genomes = neat_test_file.main()  # Run the function and capture the genomes list
        print("Test completed.")
        print(f"Genomes: {genomes}")
        
        # Remove the spinner after the test completes
        spinner_label.config(text="")

        # Restore sys.stdout to default if you want to
        sys.stdout = sys.__stdout__

    # Run the test in a separate thread
    test_thread = threading.Thread(target=task)
    test_thread.start()

def rotate_spinner(label, index):
    spinner_chars = ['|', '/', '-', '\\']
    label.config(text=spinner_chars[index])
    index = (index + 1) % 4

    if label.cget("text"):
        label.after(200, rotate_spinner, label, index)

def main():
    r = tk.Tk()
    r.title('NEATtactics')
    r.geometry("400x400")

    # Load and resize the image using PIL
    image = Image.open("docs/images/logo.png")
    resized_image = image.resize((400, 400))
    bg = ImageTk.PhotoImage(resized_image)

    # Create a canvas to display the image
    canvas1 = tk.Canvas(r, width=400, height=400)
    canvas1.pack(fill="both", expand=True)

    # Display the resized image as background
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    # Add text on the canvas
    text_var = tk.StringVar()
    text_var.set("Dette er en tekst")
    text_obj = tk.Label(r, textvariable=text_var, bg="white")
    canvas1.create_window(200, 50, window=text_obj)

    # Spinner label (for loading indicator)
    spinner_label = tk.Label(r, text="", font=("Helvetica", 20), bg="white")
    canvas1.create_window(200, 250, window=spinner_label)

    # Text widget to display terminal output
    output_text = tk.Text(r, height=10, width=40, wrap="word")
    canvas1.create_window(200, 350, window=output_text)

    # Add buttons on the canvas
    button_obj = tk.Button(r, text='Stop', width=15, command=r.destroy)
    button2_obj = tk.Button(r, text="Run test", width=15, command=lambda: run_test(spinner_label, output_text))

    # Position buttons on the canvas
    canvas1.create_window(200, 150, window=button_obj)
    canvas1.create_window(200, 200, window=button2_obj)

    r.mainloop()

if __name__ == "__main__":
    main()
