import tkinter as tk

# Global variable to track dark/light mode
is_dark_mode = True

# Function to update expression
def update_expression(value):
    current = expression_label['text']
    new_text = current + str(value)
    expression_label.config(text=new_text)

# Function to evaluate the expression
def evaluate_expression():
    try:
        current = expression_label['text']
        # Replace 'x' and '÷' with '*' and '/' for evaluation
        current = current.replace('x', '*').replace('÷', '/')
        result = str(eval(current))  # Evaluate the expression
        expression_label.config(text=result)
    except Exception as e:
        expression_label.config(text="Error")

# Function to clear the expression
def clear_expression():
    expression_label.config(text="")

# Function to delete the last character
def delete_last():
    current = expression_label['text']
    expression_label.config(text=current[:-1])

# Function to toggle dark/light mode with images
def toggle_dark_light_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    update_mode(is_dark_mode)

# Function to update colors and button images based on dark or light mode
def update_mode(dark_mode=True):
    bg_color = "#2C2C2C" if dark_mode else "#FFFFFF"
    text_color = "white" if dark_mode else "black"
    button_bg = "#505050" if dark_mode else "#D3D9E5"
    operator_bg = "#FF9500" if dark_mode else "#ADD8E6"
    del_btn_bg = "#D4D4D2" if dark_mode else "#ADD8E6"

    window.configure(bg=bg_color)
    expression_label.configure(bg=bg_color, fg=text_color)
    buttons_frame.configure(bg=bg_color)

    for button_text, button in button_widgets.items():
        if button_text in {'+', '-', 'x', '÷', '='}:
            button[0].itemconfig(button[1], fill=operator_bg, outline=operator_bg)
        elif button_text == '⌫' or button_text == 'C':
            button[0].itemconfig(button[1], fill=del_btn_bg, outline=del_btn_bg)
        else:
            button[0].itemconfig(button[1], fill=button_bg, outline=button_bg)
        button[0].config(bg=bg_color)

    # Update the dark/light mode button image
    if is_dark_mode:
        mode_button.config(image=light_mode_image)
    else:
        mode_button.config(image=dark_mode_image)

# Create window
window = tk.Tk()
window.title("iOS Replica Calculator")
window.geometry("360x650")
window.configure(bg="#2C2C2C")
window.resizable(False, False)

# Create label to display the expression
expression_label = tk.Label(window, text="", anchor='e', bg="#2C2C2C", fg="white", font=("Helvetica", 40), padx=10, pady=20)
expression_label.pack(expand=True, fill="both", pady=(40, 0))

# Create frame for buttons
buttons_frame = tk.Frame(window, bg="#2C2C2C")
buttons_frame.pack(expand=True, fill="both", pady=(10, 0))

# Create a dictionary to store button widgets for easy updating
button_widgets = {}

# Function to create a circular button
def create_circle_button(frame, text, row, column, command=None, bg_color="#505050", text_color="white"):
    canvas = tk.Canvas(frame, width=80, height=80, bg="#2C2C2C", highlightthickness=0)
    canvas.grid(row=row, column=column, padx=5, pady=5)
    
    # Create the circle
    circle = canvas.create_oval(10, 10, 70, 70, fill=bg_color, outline=bg_color)

    # Add text on top of the circle
    canvas.create_text(40, 40, text=text, fill=text_color, font=("Helvetica", 24))

    # Bind click events
    if command:
        canvas.bind("<Button-1>", lambda e: command())
    
    # Save the canvas and circle to update colors later
    button_widgets[text] = (canvas, circle)

# Load images for dark and light modes
dark_mode_image = tk.PhotoImage(file="path/to/dark_mode_image.png")  # Replace with your image path
light_mode_image = tk.PhotoImage(file="path/to/light_mode_image.png")  # Replace with your image path

# Create a button for dark/light mode toggle with an image
mode_button = tk.Button(buttons_frame, image=light_mode_image, command=toggle_dark_light_mode, bg="#505050", borderwidth=0)
mode_button.grid(row=0, column=3, padx=5, pady=5)

# Updated button layout with colors for operators
buttons = [
    ['⌫', 'C', '%', ''],
    ['7', '8', '9', 'x'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['0', '.', '=', '']
]

# Create buttons with circular design, color the operators in light blue
for row_index, row in enumerate(buttons):
    for col_index, button_text in enumerate(row):
        if button_text in {'+', '-', 'x', '÷'}:
            create_circle_button(buttons_frame, button_text, row_index, col_index,
                                 lambda value=button_text: update_expression(value),
                                 bg_color="#FF9500", text_color="white" if is_dark_mode else "black")
        elif button_text == '⌫':
            create_circle_button(buttons_frame, button_text, row_index, col_index,
                                 delete_last, bg_color="#D4D4D2", text_color="black")
        elif button_text == 'C':
            create_circle_button(buttons_frame, button_text, row_index, col_index,
                                 clear_expression, bg_color="#D4D4D2", text_color="black")
        elif button_text == '=':
            create_circle_button(buttons_frame, button_text, row_index, col_index,
                                 evaluate_expression, bg_color="#FF9500", text_color="white" if is_dark_mode else "black")
        else:
            create_circle_button(buttons_frame, button_text, row_index, col_index,
                                 lambda value=button_text: update_expression(value),
                                 bg_color="#505050", text_color="white")

# Initialize the mode after all UI components are created
update_mode(is_dark_mode)

# Run the Tkinter main loop
window.mainloop()