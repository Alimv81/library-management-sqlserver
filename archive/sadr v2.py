import re
import sys
import pyodbc
import tkinter as tk
from tkinter import *
from VBFunctions import *
from tkinter import messagebox


def reset_page():
    global window
    if window:
        window.destroy()
    window = tk.Tk()
    window.geometry("500x600")
    window.title("main page Library")
    window.resizable(False, False)
    window.configure(background='black')


def exit_program():
    global conn
    global cursor
    conn.close()
    window.destroy()
    sys.exit()


def ReadersMainPage():
    reset_page()
    window.title('Readers platform')
    username_label = tk.Label(window, text="Click the button below to enter")
    username_label.pack(pady=10, ipadx=290)
    login_button = tk.Button(window, text="Login To Library", command=LoginReader, bg="Blue")
    login_button.pack(pady=10, ipady=30, ipadx=30)
    username_label = tk.Label(window, text="If you have not registered yet, click on the button below")
    username_label.pack(pady=10, ipadx=290)
    Signin_button = tk.Button(window, text="Sign In", command=SigninReader, bg="Yellow")
    Signin_button.pack(pady=10, ipady=30, ipadx=30)
    login_button = tk.Button(window, text="Back Page", command=first_page)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def LoginReader():
    reset_page()
    window.title('login reader')
    username_label = tk.Label(window, text="User Name(ID):")
    username_label.pack(pady=10)
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)
    password_label = tk.Label(window, text="password(Phone Number):")
    password_label.pack(pady=10)
    password_entry = tk.Entry(window)
    password_entry.pack(pady=5)
    login_button = tk.Button(window, text="Enter", command=lambda: ShowReaderPage(username_entry.get(),
                                                                                  password_entry.get()), bg='blue')
    login_button.pack(pady=10)
    login_button = tk.Button(window, text="Back Page", command=ReadersMainPage)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def SigninReader():
    reset_page()
    window.title("sign in reader")
    firstname_label = tk.Label(window, text="First Name:")
    firstname_label.pack(pady=10)
    firstname_entry = tk.Entry(window)
    firstname_entry.pack(pady=5)

    lastname_label = tk.Label(window, text="Last Name:")
    lastname_label.pack(pady=10)
    lastname_entry = tk.Entry(window)
    lastname_entry.pack(pady=5)

    phonenumber_label = tk.Label(window, text="Phone Number:")
    phonenumber_label.pack(pady=10)
    phonenumber_entry = tk.Entry(window)
    phonenumber_entry.pack(pady=5)

    email_label = tk.Label(window, text="Email:")
    email_label.pack(pady=10)
    email_entry = tk.Entry(window)
    email_entry.pack(pady=5)

    address_label = tk.Label(window, text="Address:")
    address_label.pack(pady=10)
    address_entry = tk.Entry(window)
    address_entry.pack(pady=5)

    login_button = tk.Button(window, text="Submit",
                             command=lambda: CheckLoginINFOReader(firstname_entry.get(), lastname_entry.get(),
                                                                  phonenumber_entry.get(),
                                                                  email_entry.get(), address_entry.get()))
    login_button.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=ReadersMainPage)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def CheckLoginINFOReader(firstname, lastname, phonenumber, email, address, login_now=True):
    global conn
    global cursor
    global ID
    if is_valid_name(firstname) and is_valid_name(lastname) and \
            (phonenumber.isnumeric() and phonenumber.__len__() == 11 and
             phonenumber[0] == '0' and phonenumber[1] == '9') and \
            validate_email(email) and address is not None:

        sql_insert = "INSERT INTO Members (FirstName, LastName, Address,  PhoneNumber,Email) VALUES (?, ?, ?,?, ?) "
        values = (firstname, lastname, address, phonenumber, email)
        cursor.execute(sql_insert, values)
        conn.commit()
        query = f'SELECT MemberID FROM Members WHERE Phonenumber={phonenumber}'
        ID = cursor.execute(query).fetchval()
        messagebox.showinfo('member created', 'members ID is:' + str(ID))
        if login_now:
            ShowReaderPage(ID, phonenumber)
        else:
            Show_Librarian_Options()
    else:
        messagebox.showinfo('Login Error', 'wrong information format')
        if login_now:
            ReadersMainPage()
        else:
            Show_Librarian_Options()


def ShowReaderPage(id, password):
    global conn
    global cursor
    global ID
    global pos_title
    if type(id) == str: id = int(id)
    select_query = f"SELECT * FROM Members WHERE MemberID = {id} AND PhoneNumber = '{password}'"
    result = cursor.execute(select_query).fetchmany()
    if result:
        ID = id
        pos_title = 'Members'
        Show_Reader_Book_Options()
    else:
        messagebox.showinfo('Login Error', 'id or password is wrong, try again!')
        LoginReader()


def Show_Reader_Book_Options():
    reset_page()
    window.title('personal library')
    login_button = tk.Button(window, text="Search by name", command=SearchBookByName, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="Search by genre", command=SearchBookByGenre, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="Search by author name", command=SearchBookByAuthorName, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="back page", command=ReadersMainPage, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)


def SearchBookByName():
    reset_page()
    search_label = tk.Label(window, text='enter part of the name of the book or the full name')
    search_label.pack(pady=10)
    search_field = tk.Entry(window)
    search_field.pack(pady=10)
    search_button = tk.Button(window, text="Search by name", command=lambda: SearchBookByName_(search_field.get()),
                              bg="orange")
    search_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="back page", command=Show_Reader_Book_Options, bg="green")
    login_button.pack(padx=10, ipady=25, ipadx=50)


def SearchBookByName_(name: str):
    global conn
    global cursor
    query = f"SELECT * FROM Book WHERE Title like '%{name}%'"
    selected_books = cursor.execute(query)
    conn.commit()
    ShowBooks(selected_books)


def SearchBookByAuthorName():
    reset_page()
    search_label = tk.Label(window, text='please enter the authors name of the book  that you wish to find')
    search_label.pack(pady=10)
    search_field = tk.Entry(window)
    search_field.pack(pady=10)
    search_button = tk.Button(window, text="Search by author",
                              command=lambda: SearchBookByAuthorName_(search_field.get()),
                              bg="orange")
    search_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="back page", command=Show_Reader_Book_Options, bg="green")
    login_button.pack(padx=10, ipady=25, ipadx=50)


def SearchBookByAuthorName_(name: str):
    global conn
    global cursor
    query = f"SELECT * FROM Book WHERE Author = {name}"
    selected_books = cursor.execute(query)
    conn.commit()
    ShowBooks(selected_books)


def SearchBookByGenre():
    reset_page()
    search_label = tk.Label(window, text='please enter the genre of the book that you wish to find')
    search_label.pack(pady=10)
    search_field = tk.Entry(window)
    search_field.pack(pady=10)
    search_button = tk.Button(window, text="Search by genre", command=lambda: SearchBookByGenre_(search_field.get()),
                              bg="orange")
    search_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="back page", command=Show_Reader_Book_Options, bg="green")
    login_button.pack(padx=10, ipady=25, ipadx=50)


def SearchBookByGenre_(genre: str):
    global conn
    global cursor
    query = f"SELECT * FROM Book WHERE Genre = {genre}"
    selected_books = cursor.execute(query)
    conn.commit()
    ShowBooks(selected_books)


# Stafff-----------------------------------------------------------------------------------------------------------------------------------
def StaffMainPage():
    reset_page()
    window.title('Staff\'s platform')
    username_label = tk.Label(window, text="Click the button below to enter")
    username_label.pack(pady=10, ipadx=290)
    login_button = tk.Button(window, text="Login To Library", command=LoginStaff, bg="Blue")
    login_button.pack(pady=10, ipady=30, ipadx=30)
    login_button = tk.Button(window, text="Back Page", command=first_page)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def LoginStaff():
    reset_page()
    window.title('login staff')
    username_label = tk.Label(window, text="User Name(ID):")
    username_label.pack(pady=10)
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)
    password_label = tk.Label(window, text="password(Phone Number):")
    password_label.pack(pady=10)
    password_entry = tk.Entry(window)
    password_entry.pack(pady=5)
    login_button = tk.Button(window, text="Enter", command=lambda: ShowStaffPage(username_entry.get(),
                                                                                 password_entry.get()), bg='blue')
    login_button.pack(pady=10)
    login_button = tk.Button(window, text="Back Page", command=StaffMainPage)
    login_button.pack(padx=13, ipady=10, ipadx=20)






def ShowStaffPage(id, password):
    global conn
    global cursor
    global ID
    global pos_title
    if type(id) == str:
        id = int(id)
    select_query = f"SELECT * FROM Librarians WHERE LibrarianID = {id} AND PhoneNumber = '{password}'"
    result = cursor.execute(select_query).fetchmany()
    if result:
        ID = id
        pos_title = 'Librarian'
        Show_Librarian_Options()
    else:
        messagebox.showinfo('Login Error', 'id or password is wrong, try again!')
        LoginStaff()


def Show_Librarian_Options():
    reset_page()
    window.title('personal library')
    login_button = tk.Button(window, text="Add member", command=AddMember, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="delete member", command=DeleteMember, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="add book", command=AddBook, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="delete book", command=DeleteBook, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="back page", command=StaffMainPage, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)


def AddMember():
    reset_page()
    window.title('add member')
    firstname_label = tk.Label(window, text="First Name:")
    firstname_label.pack(pady=10)
    firstname_entry = tk.Entry(window)
    firstname_entry.pack(pady=5)

    lastname_label = tk.Label(window, text="Last Name:")
    lastname_label.pack(pady=10)
    lastname_entry = tk.Entry(window)
    lastname_entry.pack(pady=5)

    phonenumber_label = tk.Label(window, text="Phone Number:")
    phonenumber_label.pack(pady=10)
    phonenumber_entry = tk.Entry(window)
    phonenumber_entry.pack(pady=5)

    email_label = tk.Label(window, text="Email:")
    email_label.pack(pady=10)
    email_entry = tk.Entry(window)
    email_entry.pack(pady=5)

    address_label = tk.Label(window, text="Address:")
    address_label.pack(pady=10)
    address_entry = tk.Entry(window)
    address_entry.pack(pady=5)

    login_button = tk.Button(window, text="Submit",
                             command=lambda: CheckLoginINFOReader(firstname_entry.get(), lastname_entry.get(),
                                                                  phonenumber_entry.get(),
                                                                  email_entry.get(), address_entry.get(),
                                                                  login_now=False))
    login_button.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=Show_Librarian_Options)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def DeleteMember():
    reset_page()
    window.title('delete member')
    id_label = tk.Label(window, text="username(id):")
    id_label.pack(pady=10)
    id_entry = tk.Entry(window)
    id_entry.pack(pady=10)

    submit = tk.Button(window, text="Delete",
                       command=lambda: [DeleteMember_(id_entry.get()), Show_Librarian_Options()])
    submit.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=Show_Librarian_Options)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def DeleteMember_(id):
    global conn
    global cursor
    if type(id) == str: id = int(id)
    query = f'SELECT * FROM Members WHERE MemberID={id}'
    result = cursor.execute(query).fetchmany()
    if not result:
        messagebox.showwarning('not found', 'no member with this id')
        return
    query = f'DELETE FROM Members WHERE MemberID={id}'
    cursor.execute(query)
    conn.commit()
    messagebox.showinfo('success', f'members with id={id} deleted successfully')


def AddBook():
    pass


def DeleteBook():
    pass


# Manager---------------------------------------------------------------------------------------------------------------------------------------
def ManagerMainPage():
    reset_page()
    window.title('Manager\'s platform')
    username_label = tk.Label(window, text="Click the button below to enter")
    username_label.pack(pady=10, ipadx=290)
    login_button = tk.Button(window, text="Login To Library", command=LoginManager, bg="Blue")
    login_button.pack(pady=10, ipady=30, ipadx=30)
    login_button = tk.Button(window, text="Back Page", command=first_page)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def LoginManager():
    reset_page()
    window.title('Login Manager')
    username_label = tk.Label(window, text="User Name:")
    username_label.pack(pady=10)
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)
    password_label = tk.Label(window, text="password:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(window)
    password_entry.pack(pady=5)
    login_button = tk.Button(window, text="Enter", command=lambda: ShowManagerPage(username_entry.get(),
                                                                                   password_entry.get()), bg='blue')
    login_button.pack(pady=10)
    login_button = tk.Button(window, text="Back Page", command=ManagerMainPage)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def ShowManagerPage(id, password):
    pos_title == 'Manager'
    if id == 'admin' and password == 'admin':
        Show_Manager_Options()
    else:
        messagebox.showinfo('Login Error', 'id or password is wrong, try again!')
        LoginManager()


def Show_Manager_Options():
    reset_page()
    window.title('personal library')
    login_button = tk.Button(window, text="Add Staff member", command=AddStaffMember, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="delete Staff member", command=DeleteStaffMember, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="back page", command=LoginManager)
    login_button.pack(padx=10, ipady=25, ipadx=50)


# --------------
def AddStaffMember():
    reset_page()
    window.title('add satff member')
    firstname_label = tk.Label(window, text="First Name:")
    firstname_label.pack(pady=10)
    firstname_entry = tk.Entry(window)
    firstname_entry.pack(pady=5)

    lastname_label = tk.Label(window, text="Last Name:")
    lastname_label.pack(pady=10)
    lastname_entry = tk.Entry(window)
    lastname_entry.pack(pady=5)

    email_label = tk.Label(window, text="Email:")
    email_label.pack(pady=10)
    email_entry = tk.Entry(window)
    email_entry.pack(pady=5)

    phonenumber_label = tk.Label(window, text="Phone Number:")
    phonenumber_label.pack(pady=10)
    phonenumber_entry = tk.Entry(window)
    phonenumber_entry.pack(pady=5)

    login_button = tk.Button(window, text="Submit",
                             command=lambda: CheckLoginINFOStaff(firstname_entry.get(), lastname_entry.get(),
                                                                 phonenumber_entry.get(), email_entry.get()))
    login_button.pack(pady=10)
    login_button = tk.Button(window, text="Back Page", command=Show_Manager_Options)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def CheckLoginINFOStaff(firstname, lastname, phonenumber, email):
    global conn
    global cursor
    global ID
    if is_valid_name(firstname) and is_valid_name(lastname) and \
            (phonenumber.isnumeric() and phonenumber.__len__() == 11 and
             phonenumber[0] == '0' and phonenumber[1] == '9') and \
            validate_email(email):

        sql_insert = "INSERT INTO Librarians (FirstName, LastName, Email, Phonenumber) VALUES (?, ?, ?, ?) "
        values = (firstname, lastname, email, phonenumber)
        cursor.execute(sql_insert, values)
        conn.commit()
        query = f"SELECT LibrarianID FROM Librarians WHERE Phonenumber={phonenumber}"
        ID = cursor.execute(query).fetchval()
        messagebox.showinfo("you may now login to your library", 'Staff ID is:' + str(ID))
        AddStaffMember()
    else:
        messagebox.showinfo('Login Error', 'wrong information format')
        LoginStaff()


def DeleteStaffMember():
    reset_page()
    window.title('delete member')
    id_label = tk.Label(window, text="username(id):")
    id_label.pack(pady=10)
    id_entry = tk.Entry(window)
    id_entry.pack(pady=10)

    submit = tk.Button(window, text="Delete",
                       command=lambda: [DeleteStaffMember_(id_entry.get()), Show_Manager_Options()])
    submit.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=Show_Manager_Options)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def DeleteStaffMember_(id):
    global conn
    global cursor
    if type(id) == str: id = int(id)
    query = f'SELECT * FROM Librarians WHERE LibrarianID={id}'
    result = cursor.execute(query).fetchmany()
    if not result:
        messagebox.showwarning('not found', 'no member with this id')
        return
    query = f'DELETE FROM Librarians WHERE LibrarianID={id}'
    cursor.execute(query)
    conn.commit()
    messagebox.showinfo('success', f'Librarian with id={id} deleted successfully')


def first_page():
    reset_page()
    username_label = tk.Label(window, text="<<<<<===Welcome To Library System===>>>>>", bg="Green")
    username_label.pack(pady=1, ipadx=2900)
    username_label = tk.Label(window, text="Choose your position ::>", bg='Red')
    username_label.pack(pady=1)

    position1 = tk.Button(window, text="Readers Page", command=ReadersMainPage, bg="Yellow")
    position1.pack(pady=10, ipady=50, ipadx=50)
    position2 = tk.Button(window, text="Staff Page", command=StaffMainPage, bg="Blue")
    position2.pack(padx=10, ipady=50, ipadx=50, pady=0)
    position3 = tk.Button(window, text="Manager Page", command=ManagerMainPage, bg="orange")
    position3.pack(padx=10, ipady=50, ipadx=50, pady=0)

    exit_ = tk.Button(window, text="Exit Page", command=exit_program, bg="red")
    exit_.pack(padx=13, ipady=20, ipadx=20, pady=20)

    window.mainloop()


def connect_db():
    global conn
    global cursor
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-MQQL8BK;"
        "Database=Library_System2;"
        "Trusted_Connection=yes;"
        , autocommit=True
    )
    cursor = conn.cursor()


if __name__ == '__main__':
    ID = None
    pos_title = None

    cursor = None
    window = None
    conn = None

    connect_db()
    first_page()
