import webbrowser
from tkinter import simpledialog, messagebox
from isbn_utils import getBookName

BASE_URL = "https://isbnsearch.org/isbn/"
def manual_entry(window):
    """
    Manually enter an ISBN and fetch book details or open webpage if unavailable.
    """
    isbn = simpledialog.askstring("Manual Entry", "Enter the ISBN:", parent=window)
    if isbn:
        # If an ISBN number is entered, return book name
        title, authors = getBookName(isbn)
        messagebox.showinfo("Book Scanned", f"ISBN: {isbn}\nTitle: {title or 'Not Found'}", parent=window)
        # If no match is found in "openl" library, then popup webpage to show book details.
        if not title:
            webbrowser.open(f"{BASE_URL}{isbn}")
