def add():
    global result_value  # Make result_value a global variable so that it can be accessed by other functions
    try:
        num1 = float(entry.get())  # Get the current value in the entry field
        result_value += num1       # Add the number to the existing result
        update_readout()           # Update the readout with the new value
        clear_entry()              # Clear the entry field after adding a number
    except ValueError:
        error_message("Invalid input")