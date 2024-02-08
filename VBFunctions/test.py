import tkinter as tk


def on_button_click(label_text):
    print(f"Button clicked: {label_text}")


root = tk.Tk()
root.title("Composite Items with Scrollbar Example")

button = tk.Button(root, text='exit', command=lambda: root.destroy())
button.pack(pady=10)

# Create a canvas
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

# Add a scrollbar to the canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame to contain the items
frame = tk.Frame(canvas, bg='green')
canvas.create_window((0, 0), window=frame, anchor="nw")


# Function to create a composite item with a label and a button
def create_composite_item(label_text):
    composite_frame = tk.Frame(frame)
    composite_frame.pack(fill="x", padx=20, pady=5)

    label = tk.Label(composite_frame, text=label_text)
    label.pack(side="left", padx=20)

    label2 = tk.Label(composite_frame, text=label_text + 'xx')
    label2.pack(side="left", padx=70)

    button = tk.Button(composite_frame, text="Click me", command=lambda: on_button_click(label_text))
    button.pack(side="left")


# Create multiple composite items
for i in range(20):
    create_composite_item(f"Item {i + 1}")

# Update the canvas scroll region
canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))
print(root.winfo_width())
root.mainloop()
