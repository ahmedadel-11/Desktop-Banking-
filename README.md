# Desktop Banking
Project in python with use of Tkinter GUI toolkit and MYSQL

## Packages required
1. Tkinter - Tkinter is the standard GUI library for Python.
2. MYSQL - The Database module in Python provides The Data.
3. Random - Random module supplies arandome Number to Account ID and Credit Card Number

## Installation
###### Tkinter
```
 We just need to install Python from www.python.org, and it comes along with Python.
We do not need to install it separately.
```
###### MYSQL
```
MYSQL module You should install it from python packages in your IDE,,,, And you should to install xampp.
```
###### Random
```
Random module comes build into Python, so there is no need to install it externally.

```

## Usage
```
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkinter.ttk import *
import pymysql
from random import Random
import copy
```

## Execution flow (How to run the program?)
###### Option 1
```
1. First extract the zip file.
2. Navigate to the file cib.py
3. Launch the code in any of the supporting IDE/code editors. (You must have python pre-installed in your system)
4. open (C:\xampp\mysql\data) and paste signup file in this path
4. Launch XAMPP and Start Apache and MYSQL 
4. Run the code.
5. Now you are ready to interact with our python-based GUI program.
```


## Features of program
This is a GUI-based program. Once started running, it will prompt users to ask whose role they want to play. According to the selection, the program will ask for credentials. Once the credentials are matched, the program will unlock the respective functions
```
1) Admin LOGIN
>> admin username and password
If username and password match then banker will unlock his/her
functionalities. If they don’t match or entered admin username doesn't exist then appropriate error prompts are displayed.
> Functionalities:
                 1. Create bank account
                    - First Name
                    - Last Name
                    - Phone Number
                    - Email
                    - Username
                    - password
                    - Gender 
                    - Country
                    - CreditCard
                    - Acount Number
                    - Balance
                    Above mentioned details are typed into the form.
                    - Mobile number should be of 10 digits 
                    - Unique Username
                    - Unique CreditCard
                    - Unique Acount Number
                      If and only if the entered data passes through all these criteria then data is accepted and account is created successfully. Else appropriate error prompts are displayed to the user. 
                 2. Close bank account
                    - Delete the account whose account number is specified in the input area. Here it is checked whether the entered account number exists or not. If it doesn't then an error prompt is thrown.
                 3. Update bank account
                    - Update the account whose account number is specified in the input area. Here it is checked whether the entered account number exists or not. If it doesn't then an error prompt is thrown.
                 6. Exit
                    - Takes back to admin login screen
2) Customer            
>> Customer account Username and password should be entered
> If account Username and password matches then customer will unlock his/her
functionalities. If they don’t match or entered Username doesn't exist then appropriate error prompts are displayed.
> Functionalities:
                 1. Deposit Money
                    - Deposit Money With Credit Card Number and You Should Enter The Password of This Credit Card and confirm it with your password
                    and balance is updated with the new amount.
                 2. My Profile
                    - It's show your all data in the bank
                 3. Creat New Account
                    - You can create new acount with diffrent credit card and account number
                 4. Transfer Money
                    - Transfer Money With Account Number and confirm it with your password
                    and balance is updated with the new amount.
                 5. Check your balance
                    - On pressing this button, the total balance of customer
                 6. Exit
                    - Takes back to customer login screen
```

## Input and Output of program
We are giving a link below that redirects to the Facebook page playing our video which demonstrates the input and output of the program.
Execution video Link: [Facebook video](https://www.facebook.com/100010739831834/videos/948381589147151/)

## Made By
Ahmed Adel                                                                                              
Higher Technological Institute                                                                                              
Egypt

