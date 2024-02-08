import re
import tkinter as tk
from tkinter import messagebox


def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


def is_valid_name(name):
    pattern = r"^[A-Za-z ]+$"
    match = re.match(pattern, name)
    return match is not None


def borrow_book(member_id, book_id, cursor, conn):
    sql_insert = "INSERT INTO Transactions (MemberID,BookID) VALUES (?, ?)"
    values = (member_id, book_id)
    cursor.execute(sql_insert, values)
    conn.commit()

    select_query = f"SELECT AvailableCopies FROM books WHERE BookID = {book_id}"
    result = cursor.execute(select_query).fetchone()
    conn.commit()
    bookcount = int(result[0]) - 1
    if bookcount >= 0:
        messagebox.showinfo("Adding book", f"Book added successfully ID:{member_id} ")
        select_query = f"UPDATE Books SET AvailableCopies = {bookcount} WHERE BookID = {book_id}"
        cursor.execute(select_query)
        conn.commit()
    else:
        messagebox.showerror("Adding book", "the book isn\'t available anymore")


def return_book(member_id, book_id, cursor, conn):
    member_id = int(member_id)
    book_id = int(book_id)
    query = f'SELECT TOP 1 * FROM Transactions WHERE MemberID = {member_id} AND BookID = {book_id}'
    result = cursor.execute(query).fetchmany()
    if not result:
        messagebox.showerror('info', 'cant return any more of this book')
        return
    query = f'DELETE TOP(1) FROM Transactions WHERE MemberID = {member_id} AND BookID = {book_id}'
    cursor.execute(query)
    conn.commit()
    query = f'UPDATE Books SET AvailableCopies = AvailableCopies+1 WHERE BookID = {book_id}'
    cursor.execute(query)
    conn.commit()
    messagebox.showinfo('info', 'return book successfully')


def ShowBooks_(selected_books, root, cursor, conn, ID, re_function, searchNotPersonal=True):
    root.title("books menu")

    button = tk.Button(root, text='back page', command=lambda: re_function(), bg='orange')
    button.pack(pady=10)

    canvas = tk.Canvas(root, bg='green', width=root.winfo_width())
    canvas.pack(side="left", fill='both', expand=True)

    scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill=tk.Y)
    canvas.config(yscrollcommand=scrollbar.set)

    scrollbar = tk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)
    scrollbar.pack(side="bottom", fill=tk.X)
    canvas.config(xscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas, bg='green', width=root.winfo_width())
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def create_composite_item(row, show_button=True):
        composite_frame = tk.Frame(frame, width=root.winfo_width())
        composite_frame.pack(fill="x", padx=20, pady=5)

        label = tk.Label(composite_frame, text=row[1])
        label.pack(side="left", padx=20)

        label2 = tk.Label(composite_frame, text=row[2])
        label2.pack(side="left", padx=20)

        label4 = tk.Label(composite_frame, text=row[4])
        label4.pack(side="left", padx=20)

        label5 = tk.Label(composite_frame, text=row[5])
        label5.pack(side="left", padx=40)

        label5 = tk.Label(composite_frame, text=row[6])
        label5.pack(side="left", padx=40)

        if show_button:
            if searchNotPersonal:
                button = tk.Button(composite_frame, text="borrow",
                                   command=lambda: borrow_book(ID, row[0], cursor, conn))
                button.pack(side="left")

                button2 = tk.Button(composite_frame, text="return",
                                    command=lambda: return_book(ID, row[0], cursor, conn))
                button2.pack(side='left', padx=20)
            else:
                button = tk.Button(composite_frame, text='return',
                                   command=lambda: return_book(ID, row[0], cursor, conn))
                button.pack(side='left')

    create_composite_item(['', 'Title', 'Author', '', 'PublishDate', 'Genre', 'number of copies left'],
                          show_button=False)
    for row in selected_books:
        create_composite_item(row)

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
