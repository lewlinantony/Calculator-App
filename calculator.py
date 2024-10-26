import tkinter as tk

# Global variable to track mode
is_dark_mode = True

# SVG data for moon and sun icons
MOON_SVG = """
<svg viewBox="0 0 24 24" width="24" height="24">
    <path fill="white" d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/>
</svg>
"""

SUN_SVG = """
<svg viewBox="0 0 24 24" width="24" height="24">
    <circle fill="black" cx="12" cy="12" r="5"/>
    <path fill="black" d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72 1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
</svg>
"""

def update_expression(value):
    current = expression_label['text']
    new_text = current + str(value)
    expression_label.config(text=new_text)

def evaluate_expression():
    try:
        current = expression_label['text']
        current = current.replace('x', '*').replace('÷', '/')
        result = str(eval(current))
        expression_label.config(text=result)
    except Exception as e:
        expression_label.config(text="Error")

def clear_expression():
    expression_label.config(text="")

def delete_last():
    current = expression_label['text']
    expression_label.config(text=current[:-1])

def toggle_dark_light_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    update_mode(is_dark_mode)

def update_mode(dark_mode=True):
    bg_color = "#2C2C2C" if dark_mode else "#FFFFFF"
    text_color = "white" if dark_mode else "black"
    button_bg = "#505050" if dark_mode else "#D3D9E5"
    operator_bg = "#FF9500" if dark_mode else "#ADD8E6"
    del_btn_bg = "#D4D4D2" if dark_mode else "#ADD8E6"

    window.configure(bg=bg_color)
    expression_label.configure(bg=bg_color, fg=text_color)
    buttons_frame.configure(bg=bg_color)

    # Update the mode button icon
    mode_button = button_widgets.get('mode', None)
    if mode_button:
        canvas, circle, text_item = mode_button
        # Update the icon on the mode button
        canvas.delete("icon")  # Remove old icon
        if not dark_mode:
            canvas.create_text(40, 40, text="🌙", font=("Segoe UI Symbol", 24), fill="white", tags="icon")
        else:
            canvas.create_text(40, 40, text="☀️", font=("Segoe UI Symbol", 24), fill="black", tags="icon")

    # Update other buttons
    for button_text, button in button_widgets.items():

        canvas, circle, text_item = button
        if button_text in {'+', '-', 'x', '÷', '='}:
            canvas.itemconfig(circle, fill=operator_bg, outline=operator_bg)
            canvas.itemconfig(text_item, fill="white" if dark_mode else "black")
        elif button_text == '⌫' or button_text == 'C':
            canvas.itemconfig(circle, fill=del_btn_bg, outline=del_btn_bg)
            canvas.itemconfig(text_item, fill="black")
        else:
            canvas.itemconfig(circle, fill=button_bg, outline=button_bg)
            canvas.itemconfig(text_item, fill="white" if dark_mode else "black")
        canvas.config(bg=bg_color)

window = tk.Tk()
window.title("iOS Replica Calculator")
window.geometry("360x650")
window.configure(bg="#2C2C2C")
window.resizable(False, False)

expression_label = tk.Label(window, text="", anchor='e', bg="#2C2C2C", fg="white", font=("Helvetica", 40), padx=10, pady=20)
expression_label.pack(expand=True, fill="both", pady=(40, 0))

buttons_frame = tk.Frame(window, bg="#2C2C2C")
buttons_frame.pack(expand=True, fill="both", pady=(10, 0))

button_widgets = {}

def create_circle_button(frame, text, row, column, command=None, bg_color="#505050", text_color="white", font_size=24, is_mode_button=False):
    canvas = tk.Canvas(frame, width=80, height=80, bg="#2C2C2C", highlightthickness=0)
    canvas.grid(row=row, column=column, padx=5, pady=5)
    
    circle = canvas.create_oval(10, 10, 70, 70, fill=bg_color, outline=bg_color)

    if is_mode_button:
        # Create initial mode icon (moon for dark mode)
        text_item = canvas.create_text(40, 40, text="🌙", font=("Segoe UI Symbol", font_size), fill=text_color, tags="icon")
    else:
        text_item = canvas.create_text(40, 40, text=text, fill=text_color, font=("Helvetica", font_size))

    if command:
        canvas.bind("<Button-1>", lambda e: command())
    
    button_widgets[text] = (canvas, circle, text_item)

buttons = [
    ['⌫', 'C', '%', '÷'],
    ['7', '8', '9', 'x'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['mode', '0', '.', '=']
]

for row_index, row in enumerate(buttons):
    for col_index, button_text in enumerate(row):
        if button_text == 'mode':
            create_circle_button(buttons_frame, button_text, row_index, col_index, 
                               toggle_dark_light_mode, bg_color="#505050", 
                               text_color="white" if is_dark_mode else "black", 
                               font_size=24, is_mode_button=True)
        elif button_text in {'+', '-', 'x', '÷'}:
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
                               bg_color="#505050", text_color="white" if is_dark_mode else "black")

update_mode(is_dark_mode)

window.mainloop()