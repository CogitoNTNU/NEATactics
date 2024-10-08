import tkinter as tk
from tkinter import ttk
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

def toggle_fullscreen(event=None):
    r.attributes("-fullscreen", True)

def exit_fullscreen(event=None):
    r.attributes("-fullscreen", False)

def main():
    global r  # Make the root window accessible in toggle_fullscreen/exit_fullscreen
    r = tk.Tk()
    r.title('NEATtactics')

    # Set fullscreen attributes
    r.attributes("-fullscreen", True)
    r.bind("<F11>", toggle_fullscreen)  # Press F11 to enter fullscreen
    r.bind("<Escape>", exit_fullscreen)  # Press Esc to exit fullscreen

    # Load and resize the background image while maintaining the aspect ratio
    image = Image.open("docs/images/logo.png")
    screen_width = r.winfo_screenwidth()
    screen_height = r.winfo_screenheight()

    img_aspect_ratio = image.width / image.height
    screen_aspect_ratio = screen_width / screen_height

    if img_aspect_ratio > screen_aspect_ratio:
        new_width = screen_width
        new_height = int(screen_width / img_aspect_ratio)
    else:
        new_height = screen_height
        new_width = int(screen_height * img_aspect_ratio)

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    bg = ImageTk.PhotoImage(resized_image)

    # Create a canvas to display the image
    canvas1 = tk.Canvas(r, width=screen_width, height=screen_height)
    canvas1.pack(fill="both", expand=True)

    # Center the background image
    canvas1.create_image((screen_width // 2, screen_height // 2), image=bg, anchor="center")

    # Create a frame for the UI components to keep things organized (make it transparent)
    ui_frame = tk.Frame(r, bg="", highlightthickness=0)
    canvas1.create_window(screen_width // 2, screen_height // 2, window=ui_frame, anchor="center")

    # Add a label for the title with background color matching theme
    title_label = tk.Label(ui_frame, text="NEATtactics", font=("Helvetica", 24, "bold"), bg="#2b2b2b", fg="white")
    title_label.pack(pady=20)

    # Spinner label (for loading indicator)
    spinner_label = tk.Label(ui_frame, text="", font=("Helvetica", 16), bg="#2b2b2b", fg="white")
    spinner_label.pack(pady=10)

    # Text widget to display terminal output with colors matching the theme
    output_text = tk.Text(ui_frame, height=10, width=50, wrap="word", font=("Helvetica", 10),
                          bg="#333333", fg="white", borderwidth=2, relief="sunken")
    output_text.pack(pady=10)

    # Add buttons with better styling using ttk and matching color theme
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat", background="#444444")
    
    button_obj = ttk.Button(ui_frame, text='Stop', command=r.destroy, style="TButton")
    button2_obj = ttk.Button(ui_frame, text="Run test", command=lambda: run_test(spinner_label, output_text), style="TButton")

    # Apply button colors
    button_obj.configure(style="TButton")
    button2_obj.configure(style="TButton")

    # Pack buttons with padding for better spacing
    button_obj.pack(pady=10)
    button2_obj.pack(pady=10)

    r.mainloop()

if __name__ == "__main__":
    main()
