# import time
import glob
import os

import cv2 as cv
import pandas as pd
import pytesseract as pt
from pdf2image import convert_from_path

pt.pytesseract.tesseract_cmd = 'C://Program Files//Tesseract-OCR//tesseract.exe'
direct = os.getcwd()
imge_pd = direct + "/Pdf_images"
crops_image = direct + "/Crops_image"


def Drawing_no1(dat, pdf):
    try1 = 0
    file = open("data.txt", "a")
    dt = dat.split("\n")
    number = []
    chr1 = [".", "*", "/", ",", "x", "]", "[", "|", "\\", "_"]
    find = False
    character_find = False
    dt = dt[::-1]
    for k2 in dt:
        if not find:
            tr = k2.split(" ")
            ind = 0
            for k3 in tr:
                for c in chr1:
                    if c in k3:
                        character_find = True
                        break
                    else:
                        character_find = False
                if len(k3) >= 6 and character_find is False and num_there(k3):
                    print(ind, ":", k3)
                    if digit_len(k3) >= 2:
                        k3.replace(".jpg", "")
                        ind = ind + 1
                        try1 = try1 + 1
                        if try1 is 1:
                            number.append(str(k3).replace("[", "").replace("]", "").replace("'", ""))
                        file.write(pdf + ":" + str(k3).replace("[", "").replace("]", "").replace("'", ""))
                        file.write('\n')
    file.close()
    data = [pdf, number]
    pd1 = pd.DataFrame(data, index=["PDF", "Number"])
    pd1 = pd1.T
    pd1.to_csv("output.csv", mode='a', header=False, index=False)


def num_there(s):
    return any(t.isdigit() for t in s)


def digit_len(line):
    return len([p for p in line if p.isdigit()])


def pic_sve():
    files = glob.glob("*.pdf")
    for file in files:
        pages = convert_from_path(file, 500)
        pages[0].save(imge_pd + "/" + str(file) + '.jpg', 'JPEG')


def cv_extract():
    files = glob.glob(imge_pd + "/" + "*.jpg")
    names = [os.path.basename(x) for x in glob.glob(imge_pd + "/" + "*.jpg")]
    print(names)
    for i, file in enumerate(files, 0):
        img1 = cv.imread(file)
        h, w = img1.shape[:2]
        y2 = int(h / 2)
        x2 = int(w / 2)
        crop = img1[y2 + 1750:h, x2 - 400:w]
        text = (pt.image_to_string(crop))
        crop = cv.resize(crop, (800, 800))
        # cv.imshow("crop", crop)
        # cv.waitKey(0)
        print(names[i])
        print(len(text))
        # print(text)
        if len(text) < 110:
            print("entered")
            img2 = cv.rotate(img1, cv.ROTATE_90_CLOCKWISE)
            h, w = img2.shape[:2]
            y2 = int(h / 2)
            x2 = int(w / 2)
            crop = img2[y2 + 1750:h, x2 - 400:w]
        cv.imwrite(crops_image + "/" + names[i], crop)
        clean = text.replace("\n\n", " ").replace("\"", "").replace("-", "").replace("‘", "").replace(":", " ").replace(
            "  ", " ").replace(">", " ").strip()
        # print(clean)
        Drawing_no1(clean, names[i])
        # break


pic_sve()
cv_extract()
