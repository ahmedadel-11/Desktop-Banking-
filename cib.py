from tkinter import *
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.messagebox as mb
from tkinter.ttk import *
import pymysql
from random import Random
import copy

con = pymysql.connect(host='localhost', user='root', password='', database='signup')
cur = con.cursor()
visaPrefixList = [
    ['4', '5', '3', '9'],
    ['4', '5', '5', '6'],
    ['4', '9', '1', '6'],
    ['4', '5', '3', '2'],
    ['4', '9', '2', '9'],
    ['4', '0', '2', '4', '0', '0', '7', '1'],
    ['4', '4', '8', '6'],
    ['4', '7', '1', '6'],
    ['4']]
mastercardPrefixList = [
    ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]


def completed_number(prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)

    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):
            sum += int(reversedCCnumber[pos + 1])

        pos += 2

    # Calculate check digit

    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10

    ccnumber.append(str(checkdigit))

    return ''.join(ccnumber)


def credit_card_number(rnd, prefixList, length, howMany):
    result = []

    while len(result) < howMany:
        ccnumber = copy.copy(rnd.choice(prefixList))
        result.append(completed_number(ccnumber, length))

    return result


def output(numbers):
    result = []
    result.append('\n'.join(numbers))

    return '\n'.join(result)


generator = Random()
generator.seed()  # Seed from current time
mastercard = credit_card_number(generator, mastercardPrefixList, 16, 1)
visa = credit_card_number(generator, visaPrefixList, 8, 1)


class Deposit_money(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry('850x650+350+50')
        self.resizable(False, False)
        self.title('Deposit Money')
        self.iconbitmap('D:\\logo.ico')
        self.config(bg='#1054A9')

        # --------Frame--------#
        self.frame1 = Frame(self, width='450', height='600', )
        self.frame1.pack(expand=True)
        # --------Photo--------#
        self.photo = PhotoImage(file='D:\\cib2.png')
        self.panel = Label(self, image=self.photo)
        self.panel.place(x=360, y=40)
        # --------Label--------#
        sql = "select * from data where Username=%s "
        var3 = (str(username))
        cur.execute(sql, var3)
        result = cur.fetchone()
        balance = result[10]

        self.lb_y_amount = Label(self.frame1, text='Your Amount :', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_y_amount.place(x=10, y=200)

        self.lb_bal = Label(self.frame1, text=(str(balance) + ' $'), font=("Calisto MT", 12))
        self.lb_bal.place(x=200, y=200)

        self.lb_id = Label(self.frame1, text='Credit Card :', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_id.place(x=10, y=240)

        self.lb_amount = Label(self.frame1, text='Amount :', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_amount.place(x=10, y=280)

        self.lb_cc_pass_w = Label(self.frame1, text='CC Password :', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_cc_pass_w.place(x=10, y=320)

        self.lb_pass_w = Label(self.frame1, text='Your Password :', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_pass_w.place(x=10, y=360)

        # --------Entry--------#
        self.en_id = Entry(self.frame1)
        self.en_id.place(x=145, y=245)
        self.en_amount = Entry(self.frame1)
        self.en_amount.place(x=145, y=285)

        self.en_cc_passwd = Entry(self.frame1, show="*")
        self.en_cc_passwd.place(x=145, y=320)

        self.en_passwd = Entry(self.frame1, show="*")
        self.en_passwd.place(x=145, y=360)


        # --------Hide PASSWORD--------#

        def mark():
            if var.get() == 1:
                self.en_cc_passwd.configure(show="")
            elif var.get() == 0:
                self.en_cc_passwd.configure(show="*")
        def mark2():
            if var2.get() == 1:
                self.en_passwd.configure(show="")
            elif var2.get() == 0:
                self.en_passwd.configure(show="*")

        var = IntVar()
        var2 = IntVar()
        self.bt = Checkbutton(self.frame1, text='Show Password', command=mark, offvalue=0, onvalue=1, variable=var)
        self.bt.place(x=280, y=320)
        self.bt2 = Checkbutton(self.frame1, text='Show Password', command=mark2, offvalue=0, onvalue=1, variable=var2)
        self.bt2.place(x=280, y=360)

        # --------Button--------#
        self.b1 = Button(self.frame1, text='Deposit', width='15', command=self.deposit)
        self.b1.place(x=80, y=530)

        self.b2 = Button(self.frame1, text="Back", width='15', command=self.onclose)
        self.b2.place(x=200, y=530)

        # --------send data to DB--------#

    def deposit(self):
        cc = self.en_id.get()
        amount_0 = self.en_amount.get()
        cc_pass_w=self.en_cc_passwd.get()
        pass_w = self.en_passwd.get()

        if amount_0 == "":
            mb.showinfo('Information', "Please Enter Amount")
            self.en_amount.focus_set()
            return
        if cc == "":
            mb.showinfo('Information', "Please Enter Credit Card ")
            self.en_id.focus_set()
            return
        if cc_pass_w == "":
            mb.showinfo('Information', "Please Enter CC Password ")
            self.en_id.focus_set()
            return
        if pass_w == "":
            mb.showinfo('Information', "Please Enter Your Password")
            self.en_passwd.focus_set()
            return
        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur = con.cursor()
        sql = "select Balance from data where Username=%s "
        var = (str(username))
        cur.execute(sql, var)
        result = cur.fetchone()
        balance = result[0]
        try:
            con = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur = con.cursor()
            cur.execute("select * from data where Username=%s and  password=%s", (username, self.en_passwd.get()))
            con.commit()
            con.close()

            con = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur2 = con.cursor()
            sql2 = "select Balance from data where CreditCard=%s "
            var2 = (cc)
            cur2.execute(sql2, var2)
            result2 = cur2.fetchone()
            balance2 = result2[0]

            con = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur3 = con.cursor()
            sql3 = "select * from data where CreditCard=%s and password=%s "
            var3 = (cc,cc_pass_w)
            cur3.execute(sql3, var3)


        except:
            mb.showinfo('Information', "Transfer failed,Invalid Credit Card or Password .Try again!!!")
            self.en_id.focus_set()

        amount = self.en_amount.get()
        newbal = int(balance) + int(amount)
        ubdated_bal = int(balance2) - int(amount)

        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur2 = con.cursor()
        sql2 = "select Balance from data where CreditCard=%s "
        var2 = (cc)
        cur2.execute(sql2, var2)
        result2 = cur2.fetchone()
        balance2 = result2[0]

        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur3 = con.cursor()
        sql3 = "select * from data where CreditCard=%s and password=%s "
        var3 = (cc, cc_pass_w)
        cur3.execute(sql3, var3)


        if cur.rowcount and cur2.rowcount and cur3.rowcount == 1:
            con_u = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur_u = con_u.cursor()
            cur_u.execute("update data set Balance=%s where Username=%s", (newbal, username))
            con_u.commit()
            con_u.close()

            con_u2 = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur_u2 = con_u2.cursor()
            cur_u2.execute("update data set Balance=%s where CreditCard=%s", (ubdated_bal, self.en_id.get()))
            con_u2.commit()
            con_u2.close()

            mb.showinfo('Information', "Transaction Successfully")
            self.update()
            self.deiconify()
            self.destroy()
            self.original_frame.show()
        else:
            mb.showinfo('Information', "Login failed,Invalid Username or Password.Try again!!!")


    def onclose(self):
        """"""
        self.destroy()
        self.original_frame.show()


class Send_money(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry('850x650+350+50')
        self.resizable(False, False)
        self.title('Transfer Money')
        self.iconbitmap('D:\\logo.ico')
        self.config(bg='#1054A9')

        # --------Frame--------#
        self.frame1 = Frame(self, width='450', height='600', )
        self.frame1.pack(expand=True)
        # --------Photo--------#
        self.photo = PhotoImage(file='D:\\cib2.png')
        self.panel = Label(self, image=self.photo)
        self.panel.place(x=360, y=40)
        # --------Label--------#
        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur = con.cursor()
        sql = "select * from data where Username=%s "
        var3 = (str(username))
        cur.execute(sql, var3)
        result = cur.fetchone()
        balance = result[10]

        self.lb_y_amount = Label(self.frame1, text='Your Amount', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_y_amount.place(x=10, y=200)

        self.lb_bal = Label(self.frame1, text=(str(balance) + '$'), font=("Calisto MT", 12))
        self.lb_bal.place(x=200, y=200)

        self.lb_id = Label(self.frame1, text='Account ID', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_id.place(x=10, y=240)

        self.lb_amount = Label(self.frame1, text='Amount : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_amount.place(x=10, y=280)

        self.lb_pass_w = Label(self.frame1, text='Password : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_pass_w.place(x=10, y=320)

        # --------Entry--------#
        self.en_id = Entry(self.frame1)
        self.en_id.place(x=125, y=245)
        self.en_amount = Entry(self.frame1)
        self.en_amount.place(x=125, y=285)

        self.en_passwd = Entry(self.frame1, show="*")
        self.en_passwd.place(x=125, y=320)

        # --------Hide PASSWORD--------#

        def mark():
            if var.get() == 1:
                self.en_passwd.configure(show="")
            elif var.get() == 0:
                self.en_passwd.configure(show="*")

        var = IntVar()
        self.bt = Checkbutton(self.frame1, text='Show Password', command=mark, offvalue=0, onvalue=1, variable=var)
        self.bt.place(x=280, y=285)

        # --------Button--------#
        self.b1 = Button(self.frame1, text='Send', width='15', command=self.send_money)
        self.b1.place(x=80, y=530)

        self.b2 = Button(self.frame1, text="Back", width='15', command=self.onclose)
        self.b2.place(x=200, y=530)

        # --------send data to DB--------#

    def send_money(self):
        id1 = self.en_id.get()
        amount_0 = self.en_amount.get()
        pass_w = self.en_passwd.get()
        if amount_0 == "":
            mb.showinfo('Information', "Please Enter Amount")
            self.en_amount.focus_set()
            return
        if id1 == "":
            mb.showinfo('Information', "Please Enter Id")
            self.en_id.focus_set()
            return
        if pass_w == "":
            mb.showinfo('Information', "Please Enter Password")
            self.en_passwd.focus_set()
            return

        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur = con.cursor()
        sql = "select Balance from data where Username=%s "
        var = (str(username))
        cur.execute(sql, var)
        result = cur.fetchone()
        balance = result[0]
        try:
            con = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur = con.cursor()
            cur.execute("select * from data where Username=%s and  password=%s", (username, self.en_passwd.get()))
            con.commit()
            con.close()

            con = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur2 = con.cursor()
            sql2 = "select Balance from data where ID=%s "
            var2 = (id1)
            cur2.execute(sql2, var2)
            result2 = cur2.fetchone()
            balance2 = result2[0]
        except:
            mb.showinfo('Information', "Transfer failed,Invalid Account ID or Password .Try again!!!")
            self.en_id.focus_set()

        amount = self.en_amount.get()
        newbal = int(balance) - int(amount)
        ubdated_bal = int(balance2) + int(amount)

        con2 = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur2 = con2.cursor()
        cur2.execute("select * from data where ID=%s", (self.en_id.get()))
        con2.commit()
        con2.close()

        if cur.rowcount and cur2.rowcount == 1:
            con_u = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur_u = con_u.cursor()
            cur_u.execute("update data set Balance=%s where Username=%s", (newbal, username))
            con_u.commit()
            con_u.close()

            con_u2 = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur_u2 = con_u2.cursor()
            cur_u2.execute("update data set Balance=%s where ID=%s", (ubdated_bal, self.en_id.get()))
            con_u2.commit()
            con_u2.close()

            mb.showinfo('Information', "Transaction Successfully")
            # self.open_main_window()
            self.update()
            self.deiconify()
            self.destroy()
            self.original_frame.show()

        else:
            mb.showinfo('Information', "Login failed,Invalid Username or Password.Try again!!!")


    def onclose(self):
        """"""
        self.destroy()
        self.original_frame.show()


class My_profile(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry('850x650+350+50')
        self.resizable(False, False)
        self.title('My Profile')
        self.iconbitmap('D:\\logo.ico')
        self.config(bg='#1054A9')

        # --------Frame--------#
        self.frame1 = Frame(self, width='800', height='600', )
        self.frame1.pack(expand=True)
        # --------Photo--------#
        self.photo = PhotoImage(file='D:\\cib2.png')
        self.panel = Label(self, image=self.photo)
        self.panel.place(x=360, y=40)

        # --------Label--------#
        self.lb_f_name = Label(self.frame1, text='First Name : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_f_name.place(x=10, y=200)

        self.lb_l_name = Label(self.frame1, text='Last Name : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_l_name.place(x=10, y=240)
        self.lb_phone = Label(self.frame1, text='Phone Number : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_phone.place(x=10, y=280)

        self.lb_email = Label(self.frame1, text='Email : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_email.place(x=10, y=320)

        self.lb_uname = Label(self.frame1, text='Username : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_uname.place(x=10, y=360)

        self.lb_passwd = Label(self.frame1, text='Password : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_passwd.place(x=10, y=400)

        self.lb_gen = Label(self.frame1, text='Gender : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_gen.place(x=10, y=440)

        self.lb_country = Label(self.frame1, text='Country : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_country.place(x=10, y=480)

        self.lb_cc = Label(self.frame1, text='Credit Card : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_cc.place(x=300, y=200)

        self.lb_id = Label(self.frame1, text='ID : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_id.place(x=300, y=240)

        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur = con.cursor()

        sql = "select * from data where Username=%s "
        var3 = (str(username))
        cur.execute(sql, var3)

        result = cur.fetchone()
        f_name = result[0]
        l_name = result[1]
        p_num = result[2]
        email = result[3]
        u_name = result[4]
        passwd = result[5]
        gender = result[6]
        country = result[7]
        balance = result[10]
        id_1 = result[9]
        cc = result[8]

        print(result)
        # --------Info_Label--------#
        self.lb1_f_name = Label(self.frame1, text=f_name)
        self.lb1_f_name.place(x=125, y=205)

        self.lb1_l_name = Label(self.frame1, text=l_name)
        self.lb1_l_name.place(x=125, y=245)

        self.lb1_phone = Label(self.frame1, text=p_num)
        self.lb1_phone.place(x=125, y=285)

        self.lb1_email = Label(self.frame1, text=email)
        self.lb1_email.place(x=125, y=325)

        self.lb1_uname = Label(self.frame1, text=u_name)
        self.lb1_uname.place(x=125, y=365)

        self.lb1_passwd = Label(self.frame1, text=passwd)
        self.lb1_passwd.place(x=125, y=405)

        self.lb1_country = Label(self.frame1, text=country)
        self.lb1_country.place(x=125, y=485)

        self.lb1_gen = Label(self.frame1, text=gender)
        self.lb1_gen.place(x=125, y=445)

        self.lb1_cc = Label(self.frame1, text=cc)
        self.lb1_cc.place(x=450, y=205)

        self.lb1_id = Label(self.frame1, text=id_1)
        self.lb1_id.place(x=350, y=245)

        # --------Button--------#
        self.b1 = Button(self.frame1, text='Back', width='15', command=self.onclose)
        self.b1.place(x=80, y=530)

        self.b2 = Button(self.frame1, text="LOGIN", width='15', )
        self.b2.place(x=200, y=530)

    def onclose(self):
        """"""
        self.destroy()
        self.original_frame.show()


class main_window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry('850x650+350+50')
        self.resizable(False, False)
        self.title('Welcome')
        self.iconbitmap('D:\\logo.ico')
        self.config(bg='#1054A9')
        # --------Frame--------#
        self.frame1 = Frame(self, width='800', height='600', )
        self.frame1.pack(expand=True)
        # --------Photo--------#
        self.photo = PhotoImage(file='D:\\cib2.png')
        self.panel = Label(self, image=self.photo)
        self.panel.place(x=360, y=40)
        self.lb1 = Label(self.frame1, text='Welcome', font=("Calisto MT", 18), foreground='#1054A9')
        self.lb1.place(x=250, y=300)
        self.lb2 = Label(self.frame1, text=str(username), font=("Calisto MT", 16))
        self.lb2.place(x=380, y=304)

        # --------Button--------#
        self.b_check_balance = Button(self.frame1, text='Available Balance ', width='20', command=self.open_balance)
        self.b_check_balance.place(x=30, y=530)

        self.b_transfer = Button(self.frame1, text="Transfer Money", width='20', command=self.open_Send_money)
        self.b_transfer.place(x=180, y=530)

        self.b_transaction = Button(self.frame1, text="Exit", width='20', command=self.onclose)
        self.b_transaction.place(x=330, y=530)

        self.b_creat = Button(self.frame1, text='Creat New Account ', width='20', command=self.open_registration_window)
        self.b_creat.place(x=480, y=530)

        self.b_my_profile = Button(self.frame1, text='Deposit Money ', width='20', command=self.open_Deposit_money)
        self.b_my_profile.place(x=630, y=530)

        self.b_my_profile = Button(self.frame1, text='My Profile ', width='20', command=self.open_My_profile)
        self.b_my_profile.place(x=330, y=480)

    def open_balance(self):
        con7 = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur7 = con7.cursor()

        sql = "select * from data where Username=%s "
        var3 = (str(username))
        cur7.execute(sql, var3)
        result = cur7.fetchone()
        balance = result[10]
        con7.close()

        mb.showinfo('Information', "Available balance " + str(balance) + "$")
        self.update()
        self.deiconify()


    def open_My_profile(self):
        self.withdraw()
        window = My_profile(self)
        window.grab_set()

    def onclose(self):
        """"""
        self.destroy()

    def show(self):
        """"""
        self.update()
        self.deiconify()

    def open_Send_money(self):
        self.withdraw()
        window = Send_money(self)
        window.grab_set()

    def open_Deposit_money(self):
        self.withdraw()
        window = Deposit_money(self)
        window.grab_set()

    def open_registration_window(self):
        self.withdraw()
        window = SignupWindow(self)
        window.grab_set()

    def show(self):
        """"""
        self.update()
        self.deiconify()


class AdminWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.resizable(False, False)
        self.config(bg='#1054A9')
        self.title('Desktop Banking')
        self.iconbitmap('D:\\logo.ico')
        self.geometry('1250x750+150+40')
        # --------Frame--------#
        self.frame1 = Frame(self, width='1200', height='700', )
        self.frame1.pack(expand=True)
        # --------Photo--------#
        self.photo = PhotoImage(file='D:\\cib2.png')
        self.panel = Label(self, image=self.photo)
        self.panel.place(x=500, y=40)
        # --------Label--------#
        self.lb_f_name = Label(self.frame1, text='First Name : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_f_name.place(x=10, y=180)

        self.lb_l_name = Label(self.frame1, text='Last Name : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_l_name.place(x=10, y=220)
        self.lb_phone = Label(self.frame1, text='Phone Number : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_phone.place(x=10, y=260)

        self.lb_email = Label(self.frame1, text='Email : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_email.place(x=10, y=300)

        self.lb_uname = Label(self.frame1, text='Username : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_uname.place(x=10, y=340)

        self.lb_passwd = Label(self.frame1, text='Password : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_passwd.place(x=10, y=380)

        self.lb_gen = Label(self.frame1, text='Gender : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_gen.place(x=10, y=460)

        self.lb_country = Label(self.frame1, text='Country : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_country.place(x=10, y=500)

        self.lb_country = Label(self.frame1, text='CC : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_country.place(x=10, y=540)

        self.lb_country = Label(self.frame1, text='ID : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_country.place(x=10, y=580)

        self.lb_country = Label(self.frame1, text='Balance : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_country.place(x=10, y=620)

        # --------Strings-------
        self.first = StringVar()
        self.last = StringVar()  # to convert the data that the user enter it to string.
        self.phone = StringVar()
        self.email = StringVar()
        self.username = StringVar()
        self.passwd = StringVar()  # to convert the data that the user enter it to string.
        self.gen = StringVar()
        self.country = StringVar()
        self.cc = StringVar()
        self.id = StringVar()  # to convert the data that the user enter it to string.
        self.balance = StringVar()

        # --------combobox--------#
        self.combo_country = ttk.Combobox(self.frame1, textvariable=self.country)
        self.combo_country['value'] = ('EGYPT')
        self.combo_country.place(x=125, y=505)

        self.combo_gen = ttk.Combobox(self.frame1, textvariable=self.gen)
        self.combo_gen['value'] = ('Male', 'Female')
        self.combo_gen.place(x=125, y=465)

        # --------Entry--------#
        self.en_f_name = Entry(self.frame1, textvariable=self.first)
        self.en_f_name.place(x=125, y=185)

        self.en_l_name = Entry(self.frame1, textvariable=self.last)
        self.en_l_name.place(x=125, y=225)

        self.en_phone = Entry(self.frame1, textvariable=self.phone)
        self.en_phone.place(x=125, y=265)

        self.en_email = Entry(self.frame1, textvariable=self.email)
        self.en_email.place(x=125, y=305)

        self.en_uname = Entry(self.frame1, textvariable=self.username)
        self.en_uname.place(x=125, y=345)

        self.en_passwd = Entry(self.frame1, show="*", textvariable=self.passwd)
        self.en_passwd.place(x=125, y=385)

        self.en_cc = Entry(self.frame1, textvariable=self.cc)
        self.en_cc.place(x=125, y=545)

        self.en_id = Entry(self.frame1, textvariable=self.id)
        self.en_id.place(x=125, y=585)

        self.en_bal = Entry(self.frame1, textvariable=self.balance)
        self.en_bal.place(x=125, y=625)

        # --------Hide PASSWORD--------#

        def mark():
            if var.get() == 1:
                self.en_passwd.configure(show="")
            elif var.get() == 0:
                self.en_passwd.configure(show="*")

        var = IntVar()
        self.bt = Checkbutton(self.frame1, text='Show Password', command=mark, offvalue=0, onvalue=1, variable=var)
        self.bt.place(x=125, y=425)

        # --------Button--------#
        self.b1 = Button(self.frame1, text='ADD', width='15', command=self.add_user)
        self.b1.place(x=10, y=670)

        self.b2 = Button(self.frame1, text="UPDATE", width='15', command=self.update_i)
        self.b2.place(x=110, y=670)

        self.b3 = Button(self.frame1, text="DELETE", width='15', command=self.delete)
        self.b3.place(x=210, y=670)

        self.b4 = Button(self.frame1, text="CLEAR", width='15', command=self.Reset)
        self.b4.place(x=310, y=670)

        self.b5 = Button(self.frame1, text="LOGOUT", width='15', command=self.onclose)
        self.b5.place(x=1080, y=670)
        # --------Tree View--------
        self.FrameView = Frame(self.frame1, width='600', height='800')
        self.FrameView.place(x=290, y=180)
        self.scrollbar = Scrollbar(self.FrameView, orient=VERTICAL)

        self.table = ttk.Treeview(self.FrameView, columns=("FirstName", "LastName", "Phone Number", "Email"
                                                           , "Username", "Password", "Gender",
                                                           "Country", "Credit Card", "ID", "Balance"), show='headings',yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.table.pack(fill=BOTH)
        self.table.heading("FirstName", text='First Name')
        self.table.heading("LastName", text='Last Name')
        self.table.heading("Phone Number", text='Phone Number')
        self.table.heading("Email", text='Email')
        self.table.heading("Username", text='Username')
        self.table.heading("Password", text='Password')
        self.table.heading("Gender", text='Gender')
        self.table.heading("Country", text='Country')
        self.table.heading("Credit Card", text='Credit Card')
        self.table.heading("ID", text='ID')
        self.table.heading("Balance", text='Balance')

        self.table.column("FirstName", anchor=W, width=70)  # (w) to let the be shown at left.
        self.table.column("LastName", anchor=W, width=70)
        self.table.column("Phone Number", anchor=W, width=80)
        self.table.column("Email", anchor=W, width=100)
        self.table.column("Username", anchor=W, width=80)
        self.table.column("Password", anchor=W, width=80)
        self.table.column("Gender", anchor=W, width=50)
        self.table.column("Country", anchor=W, width=50)
        self.table.column("Credit Card", anchor=W, width=80)
        self.table.column("ID", anchor=W, width=80)
        self.table.column("Balance", anchor=W, width=80)
        self.read()
        self.table.bind("<ButtonRelease>", self.show)

    def add_user(self):
        generator = Random()
        generator.seed()  # Seed from current time
        mastercard = credit_card_number(generator, mastercardPrefixList, 16, 1)
        visa = credit_card_number(generator, visaPrefixList, 8, 1)

        y = output(visa)
        print(y)
        x = output(mastercard)
        print(x)

        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur = con.cursor()
        f_name = self.en_f_name.get()
        l_name = self.en_l_name.get()
        phone = self.en_phone.get()
        email = self.en_email.get()
        u_name = self.en_uname.get()
        passwd = self.en_passwd.get()
        gen = self.combo_gen.get()
        country = self.combo_country.get()
        cc = x
        id = y
        balance = 5000

        if f_name == "":
            mb.showinfo('Information', "Please Enter Firstname")
            self.en_f_name.focus_set()
            return
        if l_name == "":
            mb.showinfo('Information', "Please Enter Lastname")
            self.en_l_name.focus_set()
            return
        if phone == "":
            mb.showinfo('Information', "Please Enter Phone Number")
            self.en_phone.focus_set()
            return
        if email == "":
            mb.showinfo('Information', "Please Enter Email")
            self.en_email.focus_set()
            return

        if u_name == "":
            mb.showinfo('Information', "Please Enter Username")
            self.en_uname.focus_set()
            return
        if passwd == "":
            mb.showinfo('Information', "Please Enter Password")
            self.en_passwd.focus_set()
            return
        if gen == "":
            mb.showinfo('Information', "Please Select Gender")
            self.combo_gen.focus_set()
            return
        if country == "":
            mb.showinfo('Information', "Please Enter Select ")
            self.combo_country.focus_set()
            return

        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur = con.cursor()
        try:
            cur.execute("select * from data where Username=%s", (self.en_uname.get()))
            MyResults = cur.fetchone()  # used to print all id's and put all data.
            print(len(MyResults))
            if len(MyResults[4]) > 0:

                if MyResults[4] == self.en_uname.get():
                    mb.showinfo('Information', "That username is taken. Try another.")
                    self.en_uname.focus_set()
        except:
            cur.execute("insert into data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                f_name,
                l_name,
                phone,
                email,
                u_name,
                passwd,
                gen,
                country,
                cc,
                id,
                balance

            ))
            mb.showinfo('Information', "Data inserted Successfully")
            # Submit to database for execution
            con.commit()
            con.close()
            self.en_f_name.delete(0, 'end')  # to empty the place after insert the data
            self.en_l_name.delete(0, 'end')  # to empty the place after insert the data
            self.en_phone.delete(0, 'end')  # to empty the place after insert the data
            self.en_email.delete(0, 'end')  # to empty the place after insert the data
            self.en_uname.delete(0, 'end')  # to empty the place after insert the data
            self.en_passwd.delete(0, 'end')  # to empty the place after insert the data
            self.combo_country.delete(0, 'end')  # to empty the place after insert the data
            self.combo_gen.delete(0, 'end')  # to empty the place after insert the data

        self.read()

    def read(self):
        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur = con.cursor()
        sql = "select * from data"
        cur.execute(sql)
        MyResults = cur.fetchall()  # used to print all id's and put all data.
        self.table.delete(*self.table.get_children())  # to get all data and delete the old data.
        for res in MyResults:
            self.table.insert('', 'end', iid=res, values=res)
            con.commit()
        con.close()

    def show(self, ev):
        self.iid = self.table.focus()
        AllData = self.table.item(self.iid)
        val = AllData['values']
        self.first.set(val[0])
        self.last.set(val[1])
        self.phone.set(val[2])
        self.email.set(val[3])
        self.username.set(val[4])
        self.passwd.set(val[5])
        self.gen.set(val[6])
        self.country.set(val[7])
        self.cc.set(val[8])
        self.id.set(val[9])
        self.balance.set(val[10])
        print(self.iid)

    def Reset(self):
        self.en_f_name.delete(0, 'end')  # to empty the place after insert the data
        self.en_l_name.delete(0, 'end')  # to empty the place after insert the data
        self.en_phone.delete(0, 'end')  # to empty the place after insert the data
        self.en_email.delete(0, 'end')  # to empty the place after insert the data
        self.en_uname.delete(0, 'end')  # to empty the place after insert the data
        self.en_passwd.delete(0, 'end')  # to empty the place after insert the data
        self.combo_country.delete(0, 'end')  # to empty the place after insert the data
        self.combo_gen.delete(0, 'end')  # to empty the place after insert the data
        self.en_cc.delete(0, 'end')  # to empty the place after insert the data
        self.en_id.delete(0, 'end')  # to empty the place after insert the data
        self.en_bal.delete(0, 'end')  # to empty the place after insert the data

    def delete(self):
        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur = con.cursor()
        cur.execute("delete from data where Username=%s", (self.en_uname.get()))
        con.commit()
        mb.showinfo('Delete', 'The Student has been deleted', parent=self.master)
        self.read()  # to update the table after delete the student.
        self.Reset()

    def update_i(self):
        print(self.en_id.get())
        f_name = self.en_f_name.get()
        l_name = self.en_l_name.get()
        phone = self.en_phone.get()
        email = self.en_email.get()
        u_name = self.en_uname.get()
        passwd = self.en_passwd.get()
        gen = self.combo_gen.get()
        country = self.combo_country.get()
        cc = self.en_cc.get()
        id = self.en_id.get()
        balance = self.en_bal.get()

        con_0 = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur_0 = con_0.cursor()
        sql = (
            "update data set FirstName=%s,LastName=%s,PhoneNumber=%s,Email=%s,Username=%s,password=%s,Gender=%s,Country=%s,CreditCard=%s,Balance=%s where ID=%s")
        val = (f_name, l_name, phone, email, u_name, passwd, gen, country, cc, balance, id)
        cur_0.execute(sql, val)
        con_0.commit()

        mb.showinfo('Update', 'The Customer has been Updated', parent=self.master)
        self.read()  # to update the table after Update the student.
        self.Reset()

    def onclose(self):
        """"""
        self.destroy()
        self.original_frame.show()


class Admin_Login(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.resizable(False, False)
        self.config(bg='#1054A9')
        self.title('Desktop Banking')
        self.iconbitmap('D:\\logo.ico')
        self.geometry('850x450+350+150')
        # --------Frame--------
        self.frame1 = Frame(self, width='300', height='400', )
        self.frame1.pack(expand=True)
        # --------Photo--------
        self.photo = PhotoImage(file='D:\\cib2.png')
        self.panel = Label(self, image=self.photo)
        self.panel.place(x=360, y=40)
        # --------Label--------
        self.lb_admin = Label(self.frame1, text='ADMIN LOGIN', font=("Calisto MT", 12), foreground='black')
        self.lb_admin.place(x=85, y=160)

        self.lb_username = Label(self.frame1, text='USERNAME:', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_username.place(x=10, y=200)

        self.lb_password = Label(self.frame1, text='PASSWORD:', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_password.place(x=10, y=240)
        # --------Entry--------
        self.en1 = Entry(self.frame1)
        self.en1.place(x=125, y=200)

        self.en2 = Entry(self.frame1, show="*")
        self.en2.place(x=125, y=240)
        # --------Button--------
        self.b1 = Button(self.frame1, text='LOGIN', width='15', command=self.login)
        self.b1.place(x=100, y=310)
        self.b1 = Button(self.frame1, text='BACK', width='15', command=self.onclose)
        self.b1.place(x=100, y=350)

        # --------Hide PASSWORD--------
        def mark():

            if var.get() == 1:
                self.en2.configure(show="")
            elif var.get() == 0:
                self.en2.configure(show="*")

        var = IntVar()
        self.bt = Checkbutton(self.frame1, text='Show Password', command=mark, offvalue=0, onvalue=1, variable=var)
        self.bt.place(x=120, y=270)

    def open_main_window(self):
        self.withdraw()
        window = AdminWindow(self)
        window.grab_set()

    def login(self):
        try:
            global username
            username = str(self.en1.get())  # Retrieving entered username
            passwd = str(self.en2.get())  # Retrieving entered password
            if username == "":
                mb.showinfo('Information', "Please Enter Username")
                self.en1.focus_set()
                return
            if passwd == "":
                mb.showinfo('Information', "Please Enter Password")
                self.en2.focus_set()
                return
            con = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur = con.cursor()
            cur.execute("select * from admin where Username=%s and Password=%s", (self.en1.get(), self.en2.get()))
            row = cur.rowcount
            if cur.rowcount == 1:
                mb.showinfo('Information', "Login Successfully")
                self.open_main_window()
            else:
                mb.showinfo('Information', "Login failed,Invalid Username or Password.Try again!!!")
        except:
            # Closing Connection
            con.close()

    def show(self):
        """"""
        self.update()
        self.deiconify()

    def onclose(self):
        """"""
        self.destroy()
        self.original_frame.show()


class SignupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry('850x650+350+50')
        self.resizable(False, False)
        self.title('SIGNUP')
        self.iconbitmap('D:\\logo.ico')
        self.config(bg='#1054A9')

        # --------Frame--------#
        self.frame1 = Frame(self, width='450', height='600', )
        self.frame1.pack(expand=True)
        # --------Photo--------#
        self.photo = PhotoImage(file='D:\\cib2.png')
        self.panel = Label(self, image=self.photo)
        self.panel.place(x=360, y=40)
        # --------Label--------#
        self.lb_f_name = Label(self.frame1, text='First Name : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_f_name.place(x=10, y=200)

        self.lb_l_name = Label(self.frame1, text='Last Name : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_l_name.place(x=10, y=240)
        self.lb_phone = Label(self.frame1, text='Phone Number : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_phone.place(x=10, y=280)

        self.lb_email = Label(self.frame1, text='Email : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_email.place(x=10, y=320)

        self.lb_uname = Label(self.frame1, text='Username : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_uname.place(x=10, y=360)

        self.lb_passwd = Label(self.frame1, text='Password : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_passwd.place(x=10, y=400)

        self.lb_gen = Label(self.frame1, text='Gender : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_gen.place(x=10, y=440)

        self.lb_country = Label(self.frame1, text='Country : ', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_country.place(x=10, y=480)

        # --------combobox--------#
        self.combo_country = ttk.Combobox(self.frame1)
        self.combo_country['value'] = ('EGYPT')
        self.combo_country.place(x=125, y=485)

        self.combo_gen = ttk.Combobox(self.frame1)
        self.combo_gen['value'] = ('Male', 'Female')
        self.combo_gen.place(x=125, y=445)

        # --------Entry--------#
        self.en_f_name = Entry(self.frame1)
        self.en_f_name.place(x=125, y=205)

        self.en_l_name = Entry(self.frame1)
        self.en_l_name.place(x=125, y=245)

        self.en_phone = Entry(self.frame1)
        self.en_phone.place(x=125, y=285)

        self.en_email = Entry(self.frame1)
        self.en_email.place(x=125, y=325)

        self.en_uname = Entry(self.frame1)
        self.en_uname.place(x=125, y=365)

        self.en_passwd = Entry(self.frame1, show="*")
        self.en_passwd.place(x=125, y=405)

        # --------Hide PASSWORD--------#

        def mark():
            if var.get() == 1:
                self.en_passwd.configure(show="")
            elif var.get() == 0:
                self.en_passwd.configure(show="*")

        var = IntVar()
        self.bt = Checkbutton(self.frame1, text='Show Password', command=mark, offvalue=0, onvalue=1, variable=var)
        self.bt.place(x=280, y=405)

        # --------Button--------#
        self.b1 = Button(self.frame1, text='REGISTER', width='15', command=self.add_data)
        self.b1.place(x=80, y=530)

        self.b2 = Button(self.frame1, text="LOGIN", width='15', command=self.onclose)
        self.b2.place(x=200, y=530)

        # --------send data to DB--------#

    def add_data(self):
        generator = Random()
        generator.seed()  # Seed from current time
        mastercard = credit_card_number(generator, mastercardPrefixList, 16, 1)
        visa = credit_card_number(generator, visaPrefixList, 8, 1)

        y = output(visa)
        print(y)
        x = output(mastercard)
        print(x)
        con = pymysql.connect(host='localhost', user='root', password='', database='signup')
        cur = con.cursor()

        f_name = self.en_f_name.get()
        l_name = self.en_l_name.get()
        phone = self.en_phone.get()
        email = self.en_email.get()
        u_name = self.en_uname.get()
        passwd = self.en_passwd.get()
        gen = self.combo_gen.get()
        country = self.combo_country.get()
        cc = x
        id = y
        balance = 5000

        if f_name == "":
            mb.showinfo('Information', "Please Enter Firstname")
            self.en_f_name.focus_set()
            return
        if l_name == "":
            mb.showinfo('Information', "Please Enter Lastname")
            self.en_l_name.focus_set()
            return
        if phone == "":
            mb.showinfo('Information', "Please Enter Phone Number")
            self.en_phone.focus_set()
            return
        if email == "":
            mb.showinfo('Information', "Please Enter Email")
            self.en_email.focus_set()
            return

        if u_name == "":
            mb.showinfo('Information', "Please Enter Username")
            self.en_uname.focus_set()
            return
        if passwd == "":
            mb.showinfo('Information', "Please Enter Password")
            self.en_passwd.focus_set()
            return
        if gen == "":
            mb.showinfo('Information', "Please Select Gender")
            self.combo_gen.focus_set()
            return
        if country == "":
            mb.showinfo('Information', "Please Enter Select ")
            self.combo_country.focus_set()
            return

        try:
            cur.execute("select * from data where Username=%s", (self.en_uname.get()))
            MyResults = cur.fetchone()  # used to print all id's and put all data.
            print(len(MyResults))
            if len(MyResults[4]) > 0:
                if MyResults[4] == self.en_uname.get():
                    mb.showinfo('Information', "That username is taken. Try another.")
                    self.en_uname.focus_set()
        except:
            cur.execute("insert into data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                f_name,
                l_name,
                phone,
                email,
                u_name,
                passwd,
                gen,
                country,
                cc,
                id,
                balance

            ))
            mb.showinfo('Information', "Data inserted Successfully")
            # Submit to database for execution
            con.commit()
            con.close()

        self.destroy()
        self.original_frame.show()

    def onclose(self):
        """"""
        self.destroy()
        self.original_frame.show()

    def show(self):
        """"""
        self.update()
        self.deiconify()


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.config(bg='#1054A9')
        self.title('Desktop Banking')
        self.iconbitmap('D:\\logo.ico')
        self.geometry('850x450+350+150')
        # --------Frame--------
        self.frame1 = Frame(self, width='300', height='400', )
        self.frame1.pack(expand=True)
        # --------Photo--------
        self.photo = PhotoImage(file='D:\\cib2.png')
        self.panel = Label(self, image=self.photo)
        self.panel.place(x=360, y=40)
        # --------Label--------
        self.lb_username = Label(self.frame1, text='USERNAME:', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_username.place(x=10, y=200)

        self.lb_password = Label(self.frame1, text='PASSWORD:', font=("Calisto MT", 12), foreground='#1054A9')
        self.lb_password.place(x=10, y=240)
        # --------Entry--------
        self.en1 = Entry(self.frame1)
        self.en1.place(x=125, y=200)

        self.en2 = Entry(self.frame1, show="*")
        self.en2.place(x=125, y=240)
        # --------Button--------
        self.b1 = Button(self.frame1, text='LOGIN', width='15', command=self.login)
        self.b1.place(x=50, y=310)
        self.b2 = Button(self.frame1, text="SIGNUP", width='15', command=self.open_registration_window)
        self.b2.place(x=160, y=310)
        self.b3 = Button(self.frame1, text="ADMIN LOGIN", width='15', command=self.open_admin_login)
        self.b3.place(x=100, y=350)

        # --------Hide PASSWORD--------
        def mark():

            if var.get() == 1:
                self.en2.configure(show="")
            elif var.get() == 0:
                self.en2.configure(show="*")

        var = IntVar()
        self.bt = Checkbutton(self.frame1, text='Show Password', command=mark, offvalue=0, onvalue=1, variable=var)
        self.bt.place(x=120, y=270)

    def open_main_window(self):
        self.withdraw()
        window = main_window(self)
        window.grab_set()

    def open_registration_window(self):
        self.withdraw()
        window = SignupWindow(self)
        window.grab_set()

    def open_admin_login(self):
        self.withdraw()
        window = Admin_Login(self)
        window.grab_set()

    def login(self):
        try:
            global username
            username = str(self.en1.get())  # Retrieving entered username
            passwd = str(self.en2.get())  # Retrieving entered password
            if username == "":
                mb.showinfo('Information', "Please Enter Username")
                self.en1.focus_set()
                return
            if passwd == "":
                mb.showinfo('Information', "Please Enter Password")
                self.en2.focus_set()
                return
            con = pymysql.connect(host='localhost', user='root', password='', database='signup')
            cur = con.cursor()
            cur.execute("select * from data where Username=%s and password=%s", (self.en1.get(), self.en2.get()))
            row = cur.rowcount
            if cur.rowcount == 1:
                mb.showinfo('Information', "Login Successfully")
                self.open_main_window()
            else:
                mb.showinfo('Information', "Login failed,Invalid Username or Password.Try again!!!")
        except:
            # Closing Connection
            con.close()

    def show(self):
        """"""
        self.update()
        self.deiconify()


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
