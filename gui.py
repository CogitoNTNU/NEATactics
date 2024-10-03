import tkinter as tk
from PIL import Image, ImageTk
import test_file
import threading

WIDTH = 600
HEIGHT = 600
WINDOW_SIZE = f"{WIDTH}x{HEIGHT}"

def run_test(spinner_label, output_text):
    # Show the spinner while the test is running
    spinner_label.after(100, rotate_spinner, spinner_label, 0)

    # Run the test in a separate thread
    def task():
        genomes = test_file.main()
        spinner_label.config(text="")
        
        # Insert the list of genomes into the Text widget
        output_text.delete(1.0, tk.END)  # Clear the text box
        output_text.insert(tk.END, str(genomes))  # Insert the genomes list

    test_thread = threading.Thread(target=task)
    test_thread.start()

def rotate_spinner(label, index):
    # Simple loading spinner using rotating characters
    spinner_chars = ['|', '/', '-', '\\']
    t = spinner_chars[index] + "Training " + "."*index
    label.config(text=t)
    index = (index + 1) % 4  # Loop through spinner characters

    # Continue rotating if the spinner is still active
    if label.cget("text"):
        label.after(200, rotate_spinner, label, index)

def main():
    r = tk.Tk()
    r.title('NEATtactics')
    r.geometry(WINDOW_SIZE)

    # Load and resize the image using PIL
    image = Image.open("docs/images/logo.png")
    resized_image = image.resize((WIDTH, HEIGHT), Image.ANTIALIAS)  # Resize to fit window
    bg = ImageTk.PhotoImage(resized_image)

    # Create a canvas to display the image
    canvas1 = tk.Canvas(r, width=WIDTH, height=HEIGHT)
    canvas1.pack(fill="both", expand=True)

    # Display the resized image as background
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    # Add text on the canvas
    text_var = tk.StringVar()
    text_var.set("Dette er en tekst")
    text_obj = tk.Label(r, textvariable=text_var, bg="white")  # Set bg to improve visibility
    canvas1.create_window(200, 50, window=text_obj)  # Position text on canvas

    # Spinner label (for loading indicator)
    spinner_label = tk.Label(r, text="", font=("Helvetica", 20), bg="white")
    canvas1.create_window(200, 250, window=spinner_label)

    # Output label to display the genomes list
    output_text = tk.Text(r, height=10, width=40, wrap="word")
    canvas1.create_window(200, 400, window=output_text)


    # Add buttons on the canvas
    button_obj = tk.Button(r, text='Stop', width=15, command=r.destroy)
    button2_obj = tk.Button(r, text="Run test", width=15, command=lambda: run_test(spinner_label, output_text))

    # Position buttons on the canvas
    canvas1.create_window(200, 150, window=button_obj)
    canvas1.create_window(200, 200, window=button2_obj)

    r.mainloop()

if __name__ == "__main__":
    main()
