from tkinter import filedialog, messagebox
import cv2
import imutils
from pyzbar.pyzbar import decode
from isbn_utils import getBookName
import numpy as np


def extract_barcode_region(image_path, scale_factor=1.4, upscale_factor=1):
    """
    Process an image to detect and extract a barcode region and decode the ISBN.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read image file {image_path}")
        return None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute the Scharr gradient magnitude representation in the x and y directions
    ddepth = cv2.CV_32F
    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

    # Subtract the y-gradient from the x-gradient and convert to an 8-bit representation
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # Blur and threshold the image
    blurred = cv2.blur(gradient, (7, 7))
    _, thresh = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    # Construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Perform erosions and dilations to remove small blobs
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    # Find contours, sort by area, and keep only the largest one
    contours = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = imutils.grab_contours(contours)

    if contours:
        # Get the largest contour by area
        c = sorted(contours, key=cv2.contourArea, reverse=True)[0]

        # Compute the rotated bounding box of the largest contour
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Scale the box points to make the contour box slightly bigger
        box_center = np.mean(box, axis=0)
        box = ((box - box_center) * scale_factor + box_center).astype(int)

        # Crop the region within the bounding box
        x, y, w, h = cv2.boundingRect(box)
        cropped_contour = image[y:y + h, x:x + w]

        # Upscale the cropped contour to enhance resolution
        high_res_cropped_contour = cv2.resize(cropped_contour, (w * upscale_factor, h * upscale_factor),
                                              interpolation=cv2.INTER_LANCZOS4)

        # Decode the barcode from the upscaled region
        decoded_objs = decode(high_res_cropped_contour)
        for obj in decoded_objs:
            if obj.type == 'EAN13':
                isbn = obj.data.decode('utf-8')
                return isbn

    return None  # If no contour or barcode is found


def scan_from_image(window):
    scanned_isbns = []
    """
    Scan ISBNs from an image using advanced processing and fetch book details or open webpage if unavailable.
    """
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    if not file_path:
        return
    # Run the extract barcode method on the image obtained from the file path
    isbn = extract_barcode_region(file_path)
    if isbn:
        scanned_isbns.append(isbn)
        title, authors = getBookName(isbn)
        if title and authors:
            messagebox.showinfo("Book Scanned", f"Book Scanned:\nTitle: {title}\nAuthors: {authors}\nISBN: {isbn}", parent=window)
        else:
            messagebox.showinfo("ISBN Scanned", f"ISBN Detected: {isbn}\nDetails not found. It will open after all books are scanned.", parent=window)
    else:
        messagebox.showinfo("No ISBN Detected", "No ISBN could be detected in the selected image.", parent=window)


