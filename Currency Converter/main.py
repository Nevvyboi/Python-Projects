#Importing the necessary packages
from tkinter import *
from tkinter import ttk, messagebox
import requests

class Currency_Converter(Tk): #Defining a class by inheriting the Tk class
    def __init__(self):
        super().__init__() #Calling the super().__init__() from the parent class in the child class

        self.title("Currency Converter")  #Setting the title of the root window
        self.geometry('300x340') #Setting the size of the root window
        self.config(bg = "#52595D") #Setting the background colour of the root window
        self.resizable(0,0) #Making it, so that the user cant resize the window 
        #Creating a Label object used to specify the container box where we can place the text
        self.title_label = Label(self, text = 'Currency Converter', bg = '#52595D', fg = 'white', font = ('franklin gothic medium', 20), relief = 'sunken') #Defining the properties of the Label object that we created
        self.title_label.place(x = 150, y = 35, anchor = 'center')  #Placing the Label object at a specific position on the root window
        #Creating a Label object used to specify the container box where we can place the text
        self.amount_label = Label(self, text = 'Input Amount: ', bg = '#52595D', fg = 'white', font = ('franklin gothic book', 15)) #Defining the properties of the Label object that we created
        self.amount_label.place(x = 150, y = 80, anchor = 'center')  #Placing the Label object at a specific position on the root window
        #Creating Entry object used to accept single-line text strings from a user
        self.amount_entry = Entry(self)
        self.amount_entry.config(width=25) #Setting the size of the Entry object
        self.amount_entry.place(x = 150, y = 100, anchor = 'center') #Placing the Entry object at a specific position on the root window
        #Creating a Label object used to specify the container box where we can place the text
        self.base_currency_label = Label(self, text = 'From: ', bg = '#52595D', fg = 'white', font = ('franklin gothic book', 15)) #Defining the properties of the Label object that we created
        self.base_currency_label.place(x=150, y=140, anchor='center')  #Placing the Label object at a specific position on the root window
        #Creating a Label object used to specify the container box where we can place the text
        self.destination_currency_label = Label(self, text = 'To: ', bg = '#52595D', fg = 'white', font = ('franklin gothic book', 15)) #Defining the properties of the Label object that we created
        self.destination_currency_label.place(x = 150, y = 200, anchor = 'center')  #Placing the Label object at a specific position on the root window

        self.currency_variable1 = StringVar(self) #Setting the type for the variable
        self.currency_variable2 = StringVar(self) #Setting the type for the variable
        self.currency_variable1.set('Select a currency') #Setting a placeholder for the Entry object
        self.currency_variable2.set('Select a currency') #Setting a placeholder for the Entry object
        #Creating a Combobox object which is a combination of an Entry widget and a Listbox widget
        self.currency_combobox1 = ttk.Combobox(self, width = 20, textvariable = self.currency_variable1, values = Web_Scraping().symbols(1), state = 'readonly')
        self.currency_combobox1.place(x = 150, y = 170, anchor = 'center') #Placing the Combobox object at a specific position on the root window
        #Creating a Combobox object which is a combination of an Entry widget and a Listbox widget
        self.currency_combobox2 = ttk.Combobox(self, width = 20, textvariable = self.currency_variable2, values = Web_Scraping().symbols(1), state = 'readonly')
        self.currency_combobox2.place(x = 150, y = 230, anchor = 'center') #Placing the Combobox object at a specific position on the root window
        #Creating a Button object which will have trigger a command once the user has pressed it
        self.convert = Button(self, text = "Convert", bg = '#52595D', fg = 'white', command = self.processed) #Defining the properties of the Button object that we created
        self.convert.place(x = 120, y = 280, anchor = 'center') #Placing the Button object at a specific position on the root window
        #Creating a Button object which will have trigger a command once the user has pressed it
        self.clear = Button(self, text = "Clear", bg = 'red', fg = 'white', command = self.clearing) #Defining the properties of the Button object that we created
        self.clear.place(x = 180, y = 280, anchor = 'center') #Placing the Button object at a specific position on the root window
        #Creating a Label object used to specify the container box where we can place the text
        self.final_result = Label(self, text = '', bg = '#52595D', fg = 'white', font = ('calibri', 12), relief = 'sunken', width = 30) #Defining the properties of the Label object that we created
        self.final_result.place(x = 150, y = 310, anchor = 'center')  #Placing the Label object at a specific position on the root window

    def processed(self): #Creating a function which will get triggered once the button is pressed
        try: #Error handling to catch any errors
            given_amount = float(self.amount_entry.get()) #Getting the amount entry data and converting it to a float data type
            given_base_currency = self.currency_variable1.get() #Retrieving the currency_variable2
            given_des_currency = self.currency_variable2.get() #Retrieving the currency_variable2
            if given_base_currency == "Select a currency": #If statement to check if the Entry object is returned as NONE
                convert_error = messagebox.showwarning('WARNING!', 'Please select a currency you would like to convert from!')
                clear_result = self.final_result.config(text = '') #Clearing the final result field
                return convert_error, clear_result #Return and output the warning message
            elif given_des_currency == "Select a currency": #If statement to check if the Entry object is returned as NONE
                convert_error = messagebox.showwarning('WARNING!', 'Please select a currency you would like to convert to!')
                clear_result = self.final_result.config(text = '') #Clearing the final result field
                return convert_error, clear_result #Return and output the warning message 
            currency_class = Convert_Currency(given_amount, given_base_currency, given_des_currency) #Assigning values to the class, which can be retrieved within the class (constructor)
            converted_amount = currency_class.convert_currency() #Calling the convert_currency function in the class
            given_amount = '{:,}'.format(given_amount) #Adding a comma for every 3 numbers
            self.final_result.config(text=f'{given_amount} {given_base_currency} = {converted_amount} {given_des_currency}') #Showing the results of the conversion on the Label object on the root window
        except ValueError: #Catching the ValueError error which means non int type data has been inputted
            convert_error = messagebox.showwarning('WARNING!', 'Please fill the amount field (integer only)!') #Outputting a message box to the user about the wrong data type being inputted
            return convert_error #Return and output the warning message

    def clearing(self): #Creating a function which will get triggered once the button is pressed
        clear_entry = self.amount_entry.delete(0, END) #Clearing the entry field
        clear_result = self.final_result.config(text = '') #Clearing the final result field
        return clear_entry, clear_result #Returning it so the action can take place

class Convert_Currency:
  def __init__(self, amount : int, base_currency : str, des_currency : str): #Using the __init__() function to assign values for amount, base_currency and des_currency:
    self.amount = amount
    self.base_currency = base_currency
    self.des_currency = des_currency

  def convert_currency(self): #Creating a method in the object which belong to the Convert_Currency object .
    rates = Web_Scraping().symbols(2) #Calling the symbols function to get a list (json) rates with there value(s)
    rates = rates["rates"] #Accessing the set item
    if self.base_currency != 'EUR':
        amount = self.amount/rates[self.base_currency]
    #Converting the currency to and from and then limiting decimals to 2 decimal places
    amount = round(amount*rates[self.des_currency], 2)
    #Adding a comma every 3 numbers
    amount = '{:,}'.format(amount)
    return amount #Returning the amount (int)

class Web_Scraping:
    def __init__(self):
        pass
    
    def symbols(self, value : int) -> list: #Returns a list
        if value == 1:
            response = requests.get("https://api.exchangerate.host/latest") #Using the requests packages to get data from the guven url
            data = response.json() #Using the requests packages to get data from the guven url
            response = list(data.get("rates")) #Getting the rates item in the set and converting it to a list
            return response #Returning the value, which is a list of symbols and there rates
        elif value == 2:
            response = requests.get("https://api.exchangerate.host/latest") #Using the requests packages to get data from the guven url
            data = response.json() #Using the requests packages to get data from the guven url
            return data #Returning the value       

if __name__ == "__main__":
  Currency_Converter().mainloop() # Running the window
