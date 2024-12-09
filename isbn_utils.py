from isbnlib import meta
import webbrowser

# The detected isbn number will be passed into the website after the last '/' which gives book details
BASE_URL = "https://isbnsearch.org/isbn/"


# Fetch book details using isbn
def getBookName(isbn):
    try:
        book_info = meta(isbn, 'openl')
        if book_info:
            title = book_info.get("Title", "N/A")
            authors = ", ".join(book_info.get("Authors", []))
            return title, authors
    except Exception as e:
        print(f"Error fetching metadata for ISBN {isbn}: {e}")
    return None, None

# def openBrowser(isbn):
#     # Try opening webpage based on the extracted isbn
#     try:
#         webbrowser.open(f"{BASE_URL}{isbn}")
#     except Exception as e:
#         # If opening webpage fails
#         print(f"Error opening webpage for ISBN {isbn}: {e}")
