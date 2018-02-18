"""
This script contains the front-end interface for the BitShares Blockchain Fees Parser.
The interface allows the user to select the start and end dates that he wants the fees historical data for.
We use Python's Tkinter library to create the graphic user interface for the application.
"""

from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, date, timedelta
from bts_blockchain_parser import History

"""
Below are the codes for the functions that create calendars for the user to select his Start and End Dates.
They will be called upon when the user clicks on either "Start Date" or "End Date" buttons.
"""

# This function creates the date selector calendar for the user to select his Start Date.
def start_date_selector():

    # This function retrieves the user's selected start date and puts it in the textbox.
    def retrieve_start_date():
        # Retrieves value of StringVar
        global start_date_value
        start_date_value = start_cal.selection_get()

        # Before we insert the chosen date into the textbox, we need to erase whatever
        # was there before.
        start_textbox.delete(1.0, END)

        # Inserts the chosen date into the textbox.
        start_textbox.insert(END, start_date_value)

        # Since the OK Button has been clicked, the user now expects the calendar window
        # to close itself.
        start_top.destroy()

    # The toplevel widget functions like a frame to hold our calendar.
    start_top = Toplevel(window)

    start_cal = Calendar(start_top,font="Arial 10", selectmode='day', cursor="hand1",
                   year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    start_cal.pack(fill="both", expand=True)
    Button(start_top, text="Done", command=retrieve_start_date).pack()


# This function creates the date selector calendar for the user to select his End Date.
def end_date_selector():

    # This function retrieves the user's selected end date and puts it in the textbox.
    def retrieve_end_date():
        # Retrieves value of StringVar
        global end_date_value
        end_date_value = end_cal.selection_get()

        # Before we insert the chosen date into the textbox, we need to erase whatever
        # was there before.
        end_textbox.delete(1.0, END)

        # Inserts the chosen date into the textbox.
        end_textbox.insert(END, end_date_value)

        # Since the OK Button has been clicked, the user now expects the calendar window
        # to close itself.
        end_top.destroy()

    # The toplevel widget functions like a frame to hold our calendar.
    end_top = Toplevel(window)

    end_cal = Calendar(end_top,font="Arial 10", selectmode='day', cursor="hand1",
                   year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    end_cal.pack(fill="both", expand=True)
    Button(end_top, text="Done", command=retrieve_end_date).pack()


# This function checks the dates that the user inputted to ensure they are valid.
def data_validator(start, end):
    # Initial values of the three checks are each 0.
    check1, check2, check3 = 0, 0, 0

    # Check to see that Start Date is before End Date
    if start > end:
        messagebox.showerror("Error", "The Start Date needs to be before the End Date.")
    else:
        check1 = 1

    # Check to see that the Start Date is not before BitShares 2.0 debut (Oct 13, 2015).
    if start < date(2015, 10, 13):
        messagebox.showerror("Error", "The Start Date cannot be prior to the debut of BitShares on 13 October 2015.")
    else:
        check2 = 1

    # Check to see that the End Date is not after the current time.
    if end > date(datetime.now().year, datetime.now().month, datetime.now().day):
        messagebox.showerror("Error", "The dates cannot be in the future.")
    else:
        check3 = 1

    status = check1 * check2 * check3
    return bool(status)


# This function is called when the user presses the Ready To Parse button.
def parse_data():
    history = History()

    # Checks to make sure the inputted dates are valid first
    if data_validator(start_date_value, end_date_value) == True:

        # Now that we're good to go, let's call the progress screen to tell user that query is being processed now
        messagebox.showinfo("Processing", "Parsing blockchain for fees information now....")

        # Then send the dates over to History's fees_parser() method
        begin_date = datetime.combine(start_date_value, datetime.min.time())
        stop_date = datetime.combine(end_date_value, datetime.min.time())
        history.fees_parser(begin_date,stop_date, file_name.get())

"""
All the initial GUI design codes go below here.
"""

# This creates the physical window for the GUI.
window = Tk()
window.title("BitShares Blockchain Fees Parser")

date_label = Label(window, text = "Select your dates by pressing on their respective buttons:", font = "Arial 10")
date_label.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)

start_var = StringVar()
start_textbox = Text(window, height = 1, width = 15, font = "Arial 10")
start_textbox.grid(row = 1, column = 0, padx = 10, pady = 10)

end_var = StringVar()
end_textbox = Text(window, height = 1, width = 15, font = "Arial 10")
end_textbox.grid(row = 1, column = 1, padx = 10, pady = 10)

# These buttons active their corresponding functions that create calendars for the user to select dates.
Button(window, text = "Start Date", command = start_date_selector).grid(row = 2, column = 0, padx = 10, pady = 10)
Button(window, text = "End Date", command = end_date_selector).grid(row = 2, column = 1, padx = 10, pady = 10)

file_label = Label(window, text = "Save new CSV file as: ", font = "Arial 10").grid(row = 6, column = 0, columnspan = 2, pady = (30, 0))

file_name = StringVar()
file_save = Entry(window, textvariable = file_name, justify = CENTER).grid(row = 7, column = 0, columnspan = 2)

csv_label = Label(window, text = ".csv", font = "Arial 10", justify = LEFT).grid(row = 7, column = 1)

# The submit button to indicate that user has made his selections and is ready to run the blockchain parser algorithm.
Button(window, text = "Ready to Parse", justify = CENTER, command = parse_data).grid(row = 8, column = 0, columnspan = 2, padx = 10, pady = 10)

window.mainloop()
