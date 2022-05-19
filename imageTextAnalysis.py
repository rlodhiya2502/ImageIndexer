import os
from venv import create
# ! Above is for directory navigation
# ! Open-CV import
import cv2
# ! For directory selection GUI
import tkinter as tk
from tkinter import W, filedialog
# ! imports Tesseract OCR(Optical Character Recognition) package
import pytesseract
# ! imports json for json parsing
import json

# ! tells python where the exe for the OCR is
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# ! list containing all image formats supported by Open-CV
imgExts = [".bmp", ".dib", ".jpeg", ".jpg",  ".jp2", ".png", ".webp", ".pbm", ".pgm",
           ".ppm", ".pxm", ".pnm", ".pfm", ".sr", ".ras", ".tiff", ".tif", ".exr", ".hdr", ".pic"]
# * THE JPE FILE TYPE WAS CAUSING DUPLICATES BECAUSE OF JPEG ".jpe",
# ! Check directory for json or create json


def check_direc():
    # ! sets directory to variable path
    global path
    path = filedialog.askdirectory(initialdir="/")

    # ! Create list of files in a directory
    global files
    files = os.listdir(path)
    global jsonFile
    jsonFile = path + "\img_text.json"
    global images
    global info
    # ! if img_text json file is present then read and extract information from it otherwise create img_text json file
    if "img_text.json" in files:
        f = open(jsonFile, "r")
        data = f.read()
        info = [data]
        images = [json.loads(idx.replace("'", '"')) for idx in info][0]
        list_images()
    else:
        create_json()


def create_json():
    global images
    images = []
    # ! Iterates through files to return lists of images then store image name and image path
    for file in files:
        for imgExt in imgExts:
            if imgExt in file:
                imgDict = {}
                imgDict["image"] = file
                imgDict["imagePath"] = path + "/" + file
                imgDict["text"] = ""
                images.append(imgDict)
    list_images()
    # ! creates a file in the directory picked by user then writes list of images, image paths, and text found in image in JSON format
    f2s = open(jsonFile, "a")
    f2s.write(str(images))
    f2s.close

# ! Reads text in all listed images then creates a list of all images


def list_images():
    for img in images:
        pic = cv2.imread(img["imagePath"])
        text = pytesseract.image_to_string(pic).lower()
        img["text"] = text
    for i in images:
        label = tk.Label(frmResults, text=i['image'])
        label.pack()

# ! gets text in the search bar then creates and lists all images with searched text found in the image


def search_query():
    term = txtEntry.get().lower()
    results = []
    for j in images:
        if term in j["text"]:
            results.append(j)
    for lbl in frmResults.winfo_children():
        lbl.destroy()
    for r in results:
        button = tk.Button(frmResults, text=r['image'], command=lambda: open_image(
            r['image'], r['imagePath']))
        button.pack()

# ! Opens image clicked when list of images containing searched text is created


def open_image(name, path):
    cv2.imshow(name, cv2.imread(path))


# ! Root window of GUI
root = tk.Tk()

root.title('Character Recognition')
root.rowconfigure(0, minsize=200, weight=1)
root.columnconfigure(1, minsize=300, weight=1)

# * buttons frame
frmButtons = tk.Frame(relief=tk.RAISED, bd=2)
btnOpen = tk.Button(frmButtons, text='Load directory', command=check_direc)
btnUpdate = tk.Button(
    frmButtons, text='Create/Update JSON', command=create_json)

# * query frame
frmQuery = tk.Frame(borderwidth=1)
txtEntry = tk.Entry(frmQuery)
btnSearch = tk.Button(frmQuery, text='Search images', command=search_query)
frmResults = tk.Frame(frmQuery)

# * positioning
btnOpen.grid(column=0, row=0, sticky='ew', padx=5, pady=5)
btnUpdate.grid(column=0, row=1, sticky='ew', padx=5)
frmButtons.grid(column=0, row=0, sticky='ns')

txtEntry.grid(column=0, row=0, sticky='nsew', padx=5, pady=5)
btnSearch.grid(column=1, row=0, sticky='se', padx=5, pady=(0, 5))
frmQuery.grid(column=1, row=0, sticky='nsew')
frmResults.grid(column=0, row=1, sticky='nsew')

root.mainloop()
