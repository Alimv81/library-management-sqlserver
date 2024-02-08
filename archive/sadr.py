import sys
import tkinter as tk
import re
import pyodbc
from tkinter import *
from tkinter import messagebox

ID = None
Username = None
pos_title = None


def clear_page():
    # Clear all widgets from the root window
    for widget in window.winfo_children():
        widget.destroy()


def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


def is_valid_name(name):
    # Regular expression for a valid name containing only letters and spaces
    pattern = r"^[A-Za-z ]+$"
    # Use re.match to check if the entire string matches the pattern
    match = re.match(pattern, name)
    # If there is a match, the name is valid
    return match is not None


def show_login_button():
    login_button = tk.Button(window, text="Submit", command=SigninReaders)
    login_button.pack(pady=10)


def LoginOrSigninReaders():
    clear_page()
    username_label = tk.Label(window, text="Click the button below to enter")
    username_label.pack(pady=10, ipadx=290)
    login_button = tk.Button(window, text="Login To Library", command=LoginReaders, bg="Blue")
    login_button.pack(pady=10, ipady=30, ipadx=30)

    username_label = tk.Label(window, text="If you have not registered yet, click on the button below")
    username_label.pack(pady=10, ipadx=290)
    Signin_button = tk.Button(window, text="Sign In", command=SigninReaders, bg="Yellow")
    Signin_button.pack(pady=10, ipady=30, ipadx=30)

    login_button = tk.Button(window, text="Back Page", command=lambda: [window.destroy(), main()])
    login_button.pack(padx=13, ipady=10, ipadx=20)


def SigninReaders():
    clear_page()
    window.title("sign_in")
    firstname_label = tk.Label(window, text="First Name:")
    firstname_label.pack(pady=10)
    global firstname_entry
    firstname_entry = tk.Entry(window)
    firstname_entry.pack(pady=5)

    lastname_label = tk.Label(window, text="Last Name:")
    lastname_label.pack(pady=10)
    global lastname_entry
    lastname_entry = tk.Entry(window)
    lastname_entry.pack(pady=5)

    phonenumber_label = tk.Label(window, text="Phone Number:")
    phonenumber_label.pack(pady=10)
    global phonenumber_entry
    phonenumber_entry = tk.Entry(window)
    phonenumber_entry.pack(pady=5)

    email_label = tk.Label(window, text="Email:")
    email_label.pack(pady=10)
    global email_entry
    email_entry = tk.Entry(window)
    email_entry.pack(pady=5)

    address_label = tk.Label(window, text="Address:")
    address_label.pack(pady=10)
    global address_entry
    address_entry = tk.Entry(window)
    address_entry.pack(pady=5)

    login_button = tk.Button(window, text="Submit", command=CheckLoginINFO)
    login_button.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=lambda: [window.destroy(), LoginOrSigninReaders()])
    login_button.pack(padx=13, ipady=10, ipadx=20)


def LoginReaders():
    clear_page()
    window.title("login")
    username_label = tk.Label(window, text="User Name(ID):")
    username_label.pack(pady=10)
    global username_entry
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)

    password_label = tk.Label(window, text="password(Phone Number):")
    password_label.pack(pady=10)
    global password_entry
    password_entry = tk.Entry(window)
    password_entry.pack(pady=5)

    login_button = tk.Button(window, text="Enter", command=MembersPage)
    login_button.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=LoginOrSigninReaders)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def MembersPage():
    # clear_page()
    select_query = f"SELECT PhoneNumber FROM Members WHERE MemberID = {username_entry.get()}"
    result = cursor.execute(select_query).fetchval()
    conn.commit()
    # messagebox.showinfo("Login", result)
    if password_entry.get() == result:
        clear_page()
        login_button = tk.Button(window, text="Receive Book", command=BookPage, bg="orange")
        login_button.pack(padx=10, ipady=25, ipadx=50)

        login_button = tk.Button(window, text="back", command=LoginReaders)
        login_button.pack(padx=10, ipady=25, ipadx=50)
    else:
        messagebox.showinfo("Login", "your fail manager")


def BookPage():
    clear_page()
    login_button = tk.Button(window, text="Search by name", command=SearchByNameBook, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="Search by genre", command=SearchByGenreBook, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="Search by author name", command=SearchByAuthorName, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="back page", command=MembersPage, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)


# checking Readers information

def SearchByNameBook():
    clear_page()
    window.title("SearchByNameBook")
    bookName_label = tk.Label(window, text="Book Name:")
    bookName_label.pack(pady=10)
    global bookName_entry
    bookName_entry = tk.Entry(window)
    bookName_entry.pack(pady=5)

    login_button = tk.Button(window, text="confirm", command=SearchBookname, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    username_label = tk.Label(window, text=f'ID,Title,Author,ISBN,PublishedDate,Gener,AvailableCopy')
    username_label.pack(pady=10, ipadx=290)


def SearchBookname():
    clear_page()
    # Text
    select_query = f"SELECT * FROM Books WHERE Title like '%{bookName_entry.get()}%'"
    result = cursor.execute(select_query).fetchmany()
    conn.commit()


    username_label = tk.Label(window, text=f'{result}')
    username_label.pack(pady=10, ipadx=290)


def SearchByGenreBook():
    clear_page()
    window.title("SearchByGenreBook")
    bookgenre_label = tk.Label(window, text="Book Genre:")
    bookgenre_label.pack(pady=10)
    global bookgenre_entry
    bookgenre_entry = tk.Entry(window)
    bookgenre_entry.pack(pady=5)

    login_button = tk.Button(window, text="confirm", command=SearchBooknGenre, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    username_label = tk.Label(window, text=f'ID,Title,Author,ISBN,PublishedDate,Gener,AvailableCopy')
    username_label.pack(pady=10, ipadx=290)


def SearchBooknGenre():
    # clear_page()
    select_query = f"SELECT * FROM Books WHERE genre = '{bookgenre_entry.get()}'"
    result = cursor.execute(select_query).fetchall()
    # Iterate over the result set and print each line on one line
    for row in result:
        username_label = tk.Label(window, text='\t'.join(map(str, row)))
        username_label.pack(pady=10, ipadx=290)
    conn.commit()


def SearchByAuthorName():
    clear_page()
    window.title("SearchByAuthorName")
    BookAuthorName_label = tk.Label(window, text="BookAuthorName:")
    BookAuthorName_label.pack(pady=10)
    global BookAuthorName_entry
    BookAuthorName_entry = tk.Entry(window)
    BookAuthorName_entry.pack(pady=5)

    login_button = tk.Button(window, text="confirm", command=SearchBookAuthorName, bg="orange")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    username_label = tk.Label(window, text=f'ID,Title,Author,ISBN,PublishedDate,Gener,AvailableCopy')
    username_label.pack(pady=10, ipadx=290)


def SearchBookAuthorName():
    # clear_page()
    select_query = f"SELECT * FROM Books WHERE Author = '{BookAuthorName_entry.get()}'"
    result = cursor.execute(select_query).fetchall()
    # Iterate over the result set and print each line on one line
    for row in result:
        username_label = tk.Label(window, text='\t'.join(map(str, row)))
        username_label.pack(pady=10, ipadx=290)
    conn.commit()

    # messagebox.showinfo("Book Information", result)


def CheckLoginINFO():
    if is_valid_name(firstname_entry.get()) and \
            is_valid_name(lastname_entry.get()) and \
            (phonenumber_entry.get().isnumeric() and phonenumber_entry.get().__len__() == 11 and
             phonenumber_entry.get()[0] == '0' and phonenumber_entry.get()[1] == '9') and \
            validate_email(email_entry.get()) and \
            address_entry.get() is not None:
        sql_insert = "INSERT INTO Members (FirstName, LastName, Address,  PhoneNumber,Email) VALUES (?, ?, ?,?, ?) "

        values = (
            firstname_entry.get(), lastname_entry.get(), address_entry.get(), phonenumber_entry.get(),
            email_entry.get())

        cursor.execute(sql_insert, values)

        # Commit the transaction
        conn.commit()

        query = f'SELECT MemberID FROM Members WHERE PhoneNumber={phonenumber_entry.get()}'

        # اجرای کوئری و دریافت نتایج
        result = cursor.execute(query).fetchval()
        conn.commit()

        messagebox.showinfo("your ID(save for later actions)", result)
        LoginReaders()


# Stafff---------------------------------------------------------------------------------------------------------------staff

def LoginStaff():
    clear_page()
    window.title("login")
    usernamestaff_label = tk.Label(window, text="Staff User Name(ID):")
    usernamestaff_label.pack(pady=10)
    global usernamestaff_entry
    usernamestaff_entry = tk.Entry(window)
    usernamestaff_entry.pack(pady=5)

    passwordstaff_label = tk.Label(window, text="Staff password(Phone Number):")
    passwordstaff_label.pack(pady=10)
    global passwordstaff_entry
    passwordstaff_entry = tk.Entry(window)
    passwordstaff_entry.pack(pady=5)

    login_button = tk.Button(window, text="Enter", command=StaffPage)
    login_button.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=lambda: [window.destroy(), main()])
    login_button.pack(padx=13, ipady=10, ipadx=20)


def StaffPage():
    user_id_to_find = usernamestaff_entry.get()
    select_query = f"SELECT PhoneNumber FROM Librarians WHERE LibrarianID = {user_id_to_find}"
    result = cursor.execute(select_query).fetchval()
    conn.commit()
    # messagebox.showinfo("Login", result)
    if passwordstaff_entry.get() == result:
        login_button = tk.Button(window, text="Add Book", command=AddBook, bg="orange")
        login_button.pack(padx=10, ipady=25, ipadx=50)

        login_button = tk.Button(window, text="Delete book", command=DeletingBook, bg="red")
        login_button.pack(padx=10, ipady=25, ipadx=50)
    else:
        messagebox.showinfo("Login", "your fail manager")


def AddBook():
    clear_page()
    window.title("AddingBook")
    booktitle_label = tk.Label(window, text="booktitle:")
    booktitle_label.pack(pady=10)
    global booktitle_entry
    booktitle_entry = tk.Entry(window)
    booktitle_entry.pack(pady=5)

    bookAuthor_label = tk.Label(window, text="bookAuthor:")
    bookAuthor_label.pack(pady=10)
    global bookAuthor_entry
    bookAuthor_entry = tk.Entry(window)
    bookAuthor_entry.pack(pady=5)

    bookISBN_label = tk.Label(window, text="bookISBN:")
    bookISBN_label.pack(pady=10)
    global bookISBN_entry
    bookISBN_entry = tk.Entry(window)
    bookISBN_entry.pack(pady=5)

    bookPublishDate_label = tk.Label(window, text="bookPublishDate:")
    bookPublishDate_label.pack(pady=10)
    global bookPublishDate_entry
    bookPublishDate_entry = tk.Entry(window)
    bookPublishDate_entry.pack(pady=5)

    bookGenre_label = tk.Label(window, text="bookGenre:")
    bookGenre_label.pack(pady=10)
    global bookGenre_entry
    bookGenre_entry = tk.Entry(window)
    bookGenre_entry.pack(pady=5)

    bookAvailableCopies_label = tk.Label(window, text="bookAvailableCopies:")
    bookAvailableCopies_label.pack(pady=10)
    global bookAvailableCopies_entry
    bookAvailableCopies_entry = tk.Entry(window)
    bookAvailableCopies_entry.pack(pady=5)

    login_button = tk.Button(window, text="AddingBook", command=AddingBook)
    login_button.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=LoginStaff)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def AddingBook():
    sql_insert = "INSERT INTO Books (Title, Author, ISBN, PublishDate ,Genre,AvailableCopies) VALUES (?, ?, ?,?,?,?) "
    values = (
        booktitle_entry.get(), bookAuthor_entry.get(), bookISBN_entry.get(), bookPublishDate_entry.get(),
        bookGenre_entry.get(), bookAvailableCopies_entry.get())

    cursor.execute(sql_insert, values)

    conn.commit()
    messagebox.showinfo("Addingbook", "bookadded")
    AddBook()


def DeletingBook():
    clear_page()
    DeletingBookId_label = tk.Label(window, text="DeletingBookId:")
    DeletingBookId_label.pack(pady=10)
    global DeletingBookId_entry
    DeletingBookId_entry = tk.Entry(window)
    DeletingBookId_entry.pack(pady=5)

    login_button = tk.Button(window, text="Delete book", command=DeletTheBook, bg="red")
    login_button.pack(padx=10, ipady=25, ipadx=50)
    login_button = tk.Button(window, text="Back Page", command=LoginStaff)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def DeletTheBook():
    clear_page()
    print(DeletingBookId_entry.get())
    try:
        delete_query = f"DELETE FROM Books WHERE BookID = {DeletingBookId_entry.get()}"
        # Assuming cursor and conn are defined earlier in your code
        cursor.execute(delete_query)
        # Commit the transaction
        conn.commit()
        print("Deletion successful")
    except Exception as e:
        # Rollback the transaction in case of an exception
        conn.rollback()
        messagebox.showinfo("Deleting Book", f"ID of the deleted book: {e}")

    messagebox.showinfo("Deleting Book", f"You delete book thats ID is:{DeletingBookId_entry.get()}")
    login_button = tk.Button(window, text="Back Page", command=DeletingBook)
    login_button.pack(padx=13, ipady=10, ipadx=20)


# ADMIN FuNCTION------------------------------------------------------------------------------------------------------------------------------------ADMIN


def ManagerLogin():
    clear_page()
    window.title("login Manager panel")
    usernamemanager_label = tk.Label(window, text="User Name(manager):")
    usernamemanager_label.pack(pady=10)
    global usernamemanager_entry
    usernamemanager_entry = tk.Entry(window)
    usernamemanager_entry.pack(pady=5)

    passwordmanager_label = tk.Label(window, text="password(manager):")
    passwordmanager_label.pack(pady=10)
    global passwordmanager_entry
    passwordmanager_entry = tk.Entry(window)
    passwordmanager_entry.pack(pady=5)

    login_button = tk.Button(window, text="Enter", command=ManagerPage)
    login_button.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=lambda: [window.destroy(), main()])
    login_button.pack(padx=13, ipady=10, ipadx=20)


def ManagerPage():
    # clear_page()
    if passwordmanager_entry.get() == "admin" and usernamemanager_entry.get() == "admin":
        clear_page()
        login_button = tk.Button(window, text="1.Add Staff", command=ManageAddingStaff, bg="orange")
        login_button.pack(padx=10, ipady=25, ipadx=50)

        login_button = tk.Button(window, text="2.Delete Staff", command=ManageDeleteingStaff, bg="red")
        login_button.pack(padx=10, ipady=25, ipadx=50)
    else:
        messagebox.showinfo("Login", "your fail manager")

    login_button = tk.Button(window, text="Back page", command=lambda: [ManagerLogin(), window.destroy()])
    login_button.pack(padx=13, ipady=10, ipadx=20)


def ManageAddingStaff():
    clear_page()
    window.title("Sign In By Manager for Staff")
    firstnamestaff_label = tk.Label(window, text="*Librarian First Name:")
    firstnamestaff_label.pack(pady=10)
    global firstnamestaff_entry
    firstnamestaff_entry = tk.Entry(window)
    firstnamestaff_entry.pack(pady=5)

    lastnamestaff_label = tk.Label(window, text="*Librarian Last Name:")
    lastnamestaff_label.pack(pady=10)
    global lastnamestaff_entry
    lastnamestaff_entry = tk.Entry(window)
    lastnamestaff_entry.pack(pady=5)

    phonenumberstaff_label = tk.Label(window, text="*Librarian Phone Number:")
    phonenumberstaff_label.pack(pady=10)
    global phonenumberstaff_entry
    phonenumberstaff_entry = tk.Entry(window)
    phonenumberstaff_entry.pack(pady=5)

    emailstaff_label = tk.Label(window, text="*Librarian Email:")
    emailstaff_label.pack(pady=10)
    global emailstaff_entry
    emailstaff_entry = tk.Entry(window)
    emailstaff_entry.pack(pady=5)

    login_button = tk.Button(window, text="Submit", command=CheckAdminInsertionStaffINFO)
    login_button.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=ManagerLogin)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def CheckAdminInsertionStaffINFO():
    if is_valid_name(firstnamestaff_entry.get()) and \
            is_valid_name(lastnamestaff_entry.get()) and \
            (phonenumberstaff_entry.get().isnumeric() and phonenumberstaff_entry.get().__len__() == 11 and
             phonenumberstaff_entry.get()[0] == '0' and phonenumberstaff_entry.get()[1] == '9') and \
            validate_email(emailstaff_entry.get()):

        sql_insert = "INSERT INTO Librarians (FirstName, LastName, Email, PhoneNumber) VALUES (?, ?, ?,?) "
        values = (
            firstnamestaff_entry.get(), lastnamestaff_entry.get(), emailstaff_entry.get(), phonenumberstaff_entry.get())

        cursor.execute(sql_insert, values)
        conn.commit()

        query = f'SELECT LibrarianID FROM Librarians WHERE PhoneNumber={phonenumberstaff_entry.get()}'
        result = cursor.execute(query).fetchval()
        conn.commit()

        messagebox.showinfo("SMS send to Librarian ", f"Your ID is:{result}")
    else:
        messagebox.showinfo("WRONG INFO ", "You Enter a WRONG INFO please try again")
        ManageAddingStaff()


def ManageDeleteingStaff():
    clear_page()
    window.title("delete By Manager for Staff")
    IDStaffDelete_label = tk.Label(window, text="Staff ID(for deleting):")
    IDStaffDelete_label.pack(pady=10)
    global IDStaffDelete_entry
    IDStaffDelete_entry = tk.Entry(window)
    IDStaffDelete_entry.pack(pady=5)

    login_button = tk.Button(window, text="Delete", command=DeletingStaff)
    login_button.pack(pady=10)

    login_button = tk.Button(window, text="Back Page", command=ManagerLogin)
    login_button.pack(padx=13, ipady=10, ipadx=20)


def DeletingStaff():
    record_id_to_delete = IDStaffDelete_entry.get()
    delete_query = f"DELETE FROM Librarians WHERE LibrarianID = {record_id_to_delete}"
    cursor.execute(delete_query)
    conn.commit()
    messagebox.showinfo("SMS sent to Librarian ", f"You delete from librarian:{record_id_to_delete}")


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------


def main():
    global window
    window = tk.Tk()
    window.geometry("500x600")
    window.title("main page Library ")

    username_label = tk.Label(window, text="<<<<<===Welcome To Library System===>>>>>", bg="Green")
    username_label.pack(pady=1, ipadx=2900)
    username_label = tk.Label(window, text="Choose your position ::>")
    username_label.pack(pady=1)

    Signin_button = tk.Button(window, text="Readers Page", command=LoginOrSigninReaders, bg="Yellow")
    Signin_button.pack(pady=10, ipady=50, ipadx=50)
    login_button = tk.Button(window, text="Staff Page", command=LoginStaff, bg="Blue")
    login_button.pack(padx=10, ipady=50, ipadx=50)
    login_button = tk.Button(window, text="Manager Page", command=ManagerLogin, bg="orange")
    login_button.pack(padx=10, ipady=50, ipadx=50)

    username_label = tk.Label(window, text="")
    username_label.pack(pady=40)

    login_button = tk.Button(window, text="Exit Page", command=exit, bg="red")
    login_button.pack(padx=13, ipady=10, ipadx=20)

    window.mainloop()


def exit():
    clear_page()
    sys.exit()


if __name__ == "__main__":
    global coon
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-294E7HS;"
        "Database=Library_System;"
        "Trusted_Connection=yes;"
        , autocommit=True
    )
    # Create a cursor object to execute SQL queries
    global cursor
    cursor = conn.cursor()
    main()
