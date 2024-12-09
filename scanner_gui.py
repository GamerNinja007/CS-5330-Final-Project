import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from scan_video import scan_from_video
from scan_image import scan_from_image
from manual_entry import manual_entry

# Create and run application window
def main():
    window = tk.Tk()
    window.title("ISBN Scanner")
    window.geometry("400x300")
    window.resizable(False, False)
    window.config(bg="#ffffff")

    # Add title to window
    tk.Label(window, text="ISBN Scanner", font=("Helvetica", 18, "bold"), bg="#ffffff").pack(pady=10)

    # Add description for the user
    tk.Label(window, text="Scan or enter the ISBN to fetch book details", font=("Helvetica", 12), bg="#ffffff").pack()

    # Add buttons for video based scanning along with passing the method to scan from video
    btn_video = tk.Button(window, text="Scan from Video", command=lambda: scan_from_video(window),
                          width=25, height=2, bg="#4caf50", fg="white", font=("Helvetica", 10, "bold"))
    btn_video.pack(pady=10)

    # Add buttons for image based scanning along with passing the method to scan from image
    btn_image = tk.Button(window, text="Scan from Image", command=lambda: scan_from_image(window),
                          width=25, height=2, bg="#2196f3", fg="white", font=("Helvetica", 10, "bold"))
    btn_image.pack(pady=10)

    # Add buttons for returning book details based on manually entered isbn number
    btn_manual = tk.Button(window, text="Manual Entry", command=lambda: manual_entry(window),
                           width=25, height=2, bg="#ff5722", fg="white", font=("Helvetica", 10, "bold"))
    btn_manual.pack(pady=10)


    tk.Label(window, text="Powered by pyzbar", font=("Helvetica", 8), bg="#ffffff", fg="#888888").pack(side=tk.BOTTOM, pady=5)

    window.mainloop()


# Run the script
if __name__ == "__main__":
    main()
