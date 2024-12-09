import webbrowser
import time

import cv2
import threading
from pyzbar.pyzbar import decode
from isbn_utils import getBookName
from tkinter import messagebox
import tkinter as tk


# Declare variables to store scanned ISBNs and a flag to indicate scanning status
scanned_isbns = []
done_scanning = False

BASE_URL = "https://isbnsearch.org/isbn/"


# Return detected isbns
def show_detected_isbns(window):
    # If no isbn was scanned/detected
    if not scanned_isbns:
        messagebox.showinfo("No ISBNs", "No ISBNs were scanned.", parent=window)
        return

    book_details = []
    unmapped_isbns = []

    # Get book info for each ISBN
    for isbn in scanned_isbns:
        title, authors = getBookName(isbn)
        if title:
            book_details.append(f"Title: {title}\nAuthors: {authors}\nISBN: {isbn}")
        else:
            book_details.append(f"ISBN: {isbn} - Details not found")
            unmapped_isbns.append(isbn)

    # Display all detected details
    details_message = "\n\n".join(book_details)
    messagebox.showinfo("Scanned Books", f"The following books were scanned:\n\n{details_message}", parent=window)

    # Open web pages for ISBNs where no info was found on openl
    for isbn in unmapped_isbns:
        try:
            webbrowser.open(f"{BASE_URL}{isbn}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open webpage for ISBN: {isbn}\nError: {e}", parent=window)


# Scan ISBN using video camera / webcam
def scan_from_video(window):
    def video_thread():
        # While scanning video, original window shouldnt be seen
        window.withdraw()
        vid = cv2.VideoCapture(0)
        last_detected_time = time.time()

        # Detect ISBN from a video frame
        def getIsbn(frame):
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_objs = decode(gray_frame)
            for obj in decoded_objs:
                if obj.type == 'EAN13':
                    return obj.data.decode('utf-8')
            return None

        # Initialize control panel variables
        global done_scanning, control_window
        done_scanning = False
        control_window = None

        # Create Control Panel
        def open_control_panel():
            global control_window
            control_window = tk.Toplevel(window)
            control_window.title("Control Panel")
            control_window.geometry("200x100")
            control_window.resizable(False, False)
            tk.Button(control_window, text="Done Scanning", command=on_done, width=15, bg="#4caf50", fg="white").pack(
                pady=20)

        # Operation of done scanning button
        def on_done():
            global done_scanning, control_window
            done_scanning = True
            if control_window:
                control_window.destroy()  # Close the control panel window

        open_control_panel()

        # Access video camera to access frames
        while True:
            ret, frame = vid.read()
            if not ret:
                break

            cv2.imshow('Webcam - Press Q to Quit', frame)
            # Detect ISBNs from the frame
            isbn = getIsbn(frame)
            if isbn:
                last_detected_time = time.time()
                if isbn not in scanned_isbns:
                    scanned_isbns.append(isbn) # Only if a new ISBN is detected, add it
                    messagebox.showinfo("ISBN Detected", f"ISBN: {isbn} detected.", parent=window)

            # Check for 15 seconds of inactivity to ensure that the user knows that their book is not being detected.
            if time.time() - last_detected_time > 15:
                vid.release()
                cv2.destroyAllWindows()
                inactivityDetected(window)
                break

            # Stop scanning if "Done Scanning" button was pressed
            if done_scanning:
                vid.release()
                cv2.destroyAllWindows()
                show_detected_isbns(window)
                break

            # Quit if user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        vid.release()
        cv2.destroyAllWindows()
        window.deiconify()

    def inactivityDetected(window):
        response = messagebox.askquestion(
            "Inactivity Detected",
            "No ISBN detected for 15 seconds. Are you done scanning?",
            icon="question",
            parent=window
        )
        if response == 'yes':
            show_detected_isbns(window)
        else:
            scan_from_video(window)

    t = threading.Thread(target=video_thread)
    t.start()
