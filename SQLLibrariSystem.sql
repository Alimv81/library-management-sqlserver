Create Database Library_System3

Use Library_System3
GO

CREATE TABLE Books (
    BookID INT IDENTITY(11111,1) PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Author NVARCHAR(100) NOT NULL,
    ISBN NVARCHAR(20) UNIQUE,
    PublishDate DATE,
    Genre NVARCHAR(50),
    AvailableCopies INT DEFAULT 1 CHECK (AvailableCopies >= 0)
);

CREATE TABLE Members (
    MemberID  INT IDENTITY(22222,1)  PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Address NVARCHAR(255),
    PhoneNumber NVARCHAR(20),
    Email NVARCHAR(100) UNIQUE
);


CREATE TABLE Librarians (
    LibrarianID INT IDENTITY(33333,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) UNIQUE,
    PhoneNumber NVARCHAR(20)
);


CREATE TABLE Transactions (
    TransactionID INT IDENTITY(55555,1) PRIMARY KEY,
    MemberID INT FOREIGN KEY REFERENCES Members(MemberID),
	BookID INT FOREIGN KEY REFERENCES Books(BookID),
    CheckoutDate DATETIME DEFAULT GETDATE(),
    ReturnDate DATETIME DEFAULT DATEADD(day, 10, GETDATE())
);