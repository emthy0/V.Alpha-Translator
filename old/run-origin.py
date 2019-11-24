import cv2
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image, ImageDraw, ImageFont
import pytesseract
from googletrans import Translator
from functools import partial
from os import walk
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
translator = Translator()


ix,iy = -1,-1
count = 0
check = 0
initial = "Thanat Wongsamut"
eyedrop = "OFF"
bgcolor = [0,0,0]
fgcolor = [0,0,0]
edcolor = [0,0,0]
font_option = []
slider_pos = 0

for (dirpath, dirnames, filenames) in walk("font/"):
    font_option.append(filenames)

class textbox():
    def __init__(self):
        self.number = 0
        self.position = list() 
        self.before = ""
        self.after = ""

def extract(f):
    textboxes = list()
    file = open(f,'r')
    texts = file.read()
    texts = texts.split('\n')
    for i in range(len(texts)):
        _textbox = textbox()
        text = texts[i].split(';')
        _textbox.number = int(text[0])
        _textbox.position = list()

        temp = text[1]
        temp = temp.strip('{').strip('}')
        temp = temp.split(',')
        for k in temp:
            k = k.strip('[').strip(']')
            k = k.split('-')
            pos = [int(k[0]),int(k[1])]
            _textbox.position.append(pos)
        _textbox.before = text[2]
        _textbox.after = text[3]
        textboxes.append(_textbox)
    return textboxes

def packing(f,tb):
    textboxes = tb
    file = open(f,'w')
    for i in range(len(textboxes)):
        file.write()

def display_box(i):
    global page_no
    global img
    global textboxes
    global before_text
    global after_text
    position = textboxes[i].position
    xmin , ymin = np.amin(np.array(position), axis=0)
    xmax , ymax = np.amax(np.array(position), axis=0)
    img = cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (0,255,0), 2)
    for k in range(len(textboxes)):
        if k != i:
            position = textboxes[k].position
            xmin , ymin = np.amin(np.array(position), axis=0)
            xmax , ymax = np.amax(np.array(position), axis=0)
            img = cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (255,0,0), 2)
    prompt.set(str(page_no+1) + "/" + str(len(textboxes)))
    before_text.delete("1.0",tk.END)
    before_text.insert(tk.END, textboxes[page_no].after)
    after_text.delete("1.0",tk.END)
    after_text.insert(tk.END, textboxes[page_no].after)
    OCR()
    root.update()
    
def mark(event,x,y,flags,param):
    global ix,iy
    global textboxes
    global page_no
    global count
    global check
    global initial
    global img
    global eyedrop
    global edcolor
    global prompt_eye
    global slider_pos
    y = y+ int(slider_pos)
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if eyedrop == "OFF":
            for i in range(len(textboxes)):
                position = textboxes[i].position
                if len(position) != 0:
                    xmin , ymin = np.amin(np.array(position), axis=0)
                    xmax , ymax = np.amax(np.array(position), axis=0)
                    if x in range(xmin,xmax) and y in range(ymin,ymax):
                        page_no = i
                        display_box(page_no)
                        check = 1
                        break
            if check == 0:
                cv2.circle(img,(x,y),2,(255,255,255),-1)
                ix,iy = x,y
                if page_no == 0 and initial == "Thanat Wongsamut":
                    initial = "Developer"
                    if count == 0:
                        textboxes[0].position.append([ix, iy])
                        count += 1
                    elif count == 1:
                        textboxes[0].position.append([ix, iy])
                        OCR()
                        count = 0
                    prompt.set(str(page_no+1) + "/" + str(len(textboxes)))
                else:
                    if count == 0:
                        temp_textbox = textbox()
                        temp_textbox.number = len(textboxes)-1
                        textboxes.append(temp_textbox)
                        textboxes[-1].position.append([ix, iy])
                        count += 1
                    elif count == 1:
                        textboxes[-1].position.append([ix, iy])
                        display_box(len(textboxes)-1)
                        count = 0
                        OCR()
                    page_no = len(textboxes) - 1
                    prompt.set(str(page_no+1) + "/" + str(len(textboxes)))
            check = 0
            root.update()
        elif eyedrop=="ON":
            edcolor[0] = img[x,y][0]
            edcolor[1] = img[x,y][1]
            edcolor[2] = img[x,y][2]
            eyedrop = "OFF"
            eyedrop_but = tk.Button(tool, bg='#313131', fg='#ffffff', activebackground='#ffffff' ,activeforeground='#000000', font=('Courier', 18), text="EYE", command=CLONE)
            eyedrop_but.place(relx=0.75, rely=0.5, relwidth=0.1, relheight=1, anchor='center')
            prompt_eye.set(edcolor)
            root.update()

def CropRec(img,position):
    xmin , ymin = np.amin(np.array(position), axis=0)
    xmax , ymax = np.amax(np.array(position), axis=0)
    img = cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (0,255,0), 2)

def OCR():
    global original
    global textboxes
    global page_no
    global before_text
    position = textboxes[page_no].position
    xmin , ymin = np.amin(np.array(position), axis=0)
    xmax , ymax = np.amax(np.array(position), axis=0)
    temp_img = original[ymin:ymax,xmin:xmax]
    cv2.imwrite("textbox" + str(page_no) + ".jpg" , temp_img)
    cv2.namedWindow('Cropped')
    cv2.imshow("Cropped", temp_img)

    text_rec = pytesseract.image_to_string("textbox" + str(page_no) + ".jpg")
    text_rec = ''.join(text_rec)
    text_rec = text_rec.split('\n')
    text_rec = ' '.join(text_rec)
    text_rec = text_rec.lower()
    textboxes[page_no].before = text_rec

    before_text.delete("1.0",tk.END)
    before_text.insert(tk.END, textboxes[page_no].before)
    root.update()

def TRANS():
    global original
    global textboxes
    global page_no
    global before_text
    global after_text
    translations = translator.translate(before_text.get("1.0", tk.END), dest='thai')
    textboxes[page_no].before = before_text
    after_text.insert(tk.END, translations.text)
    root.update()

def PRE():
    global final
    global after_text
    global textboxes
    global page_no
    global img
    global f_option
    global f_size
    global after_text
    position = textboxes[page_no].position
    xmin , ymin = np.amin(np.array(position), axis=0)
    xmax , ymax = np.amax(np.array(position), axis=0)

    if bg_color.get("1.0",tk.END) != '\n' and len(bg_color.get("1.0",tk.END).split(',')) == 3 and '\n' not in bg_color.get("1.0",tk.END).split(',') and '' not in bg_color.get("1.0",tk.END).split(',') :
        back_color = []
        back_color.append(int(bg_color.get("1.0",tk.END).split(',')[0]))
        back_color.append(int(bg_color.get("1.0",tk.END).split(',')[1]))
        back_color.append(int(bg_color.get("1.0",tk.END).split(',')[2]))
    else:
        back_color = [0,0,0]
    
    if fg_color.get("1.0",tk.END) != '\n' and len(fg_color.get("1.0",tk.END).split(',')) == 3 and '\n' not in fg_color.get("1.0",tk.END).split(',') and '' not in fg_color.get("1.0",tk.END).split(',') :
        fore_color = []
        fore_color.append(int(fg_color.get("1.0",tk.END).split(',')[0]))
        fore_color.append(int(fg_color.get("1.0",tk.END).split(',')[1]))
        fore_color.append(int(fg_color.get("1.0",tk.END).split(',')[2]))
        fore_color = tuple(fore_color)
    else:
        fore_color = tuple([255,255,2552])

    font_name = f_option.get()
    if f_size.get("1.0",tk.END) != '\n':
        font_size = int(f_size.get("1.0",tk.END))
    else:
        font_size = 16

    text = after_text.get("1.0", tk.END)
    font = ImageFont.truetype("font/" + font_name, font_size)
    img = cv2.rectangle(img, (xmin,ymin), (xmax,ymax), back_color, -1)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    text_width, text_height = draw.textsize(text, font)
    line = text.split('\n')
    ini_height = (ymax + ymin)/2 
    ini_width = (xmax + xmin)/2
    line_width, line_height = draw.textsize(text, font)
    draw.multiline_text((ini_width - line_width//2, ini_height - line_height//2), text, fore_color, font=font, align='center')
    img = np.array(img_pil)
    textboxes[page_no].after = after_text.get("1.0",tk.END).strip('\n')
    cv2.imshow('Image',img[0 + int(slider_pos) :540 + int(slider_pos),:])

    final = cv2.rectangle(final, (xmin,ymin), (xmax,ymax), back_color, -1)
    img_pil = Image.fromarray(final)
    draw = ImageDraw.Draw(img_pil)
    text_width, text_height = draw.textsize(text, font)
    line = text.split('\n')
    ini_height = (ymax + ymin)/2 
    ini_width = (xmax + xmin)/2
    line_width, line_height = draw.textsize(text, font)
    draw.multiline_text((ini_width - line_width//2, ini_height - line_height//2), text, fore_color, font=font, align='center')
    final = np.array(img_pil)

def REND():
    global final
    cv2.imwrite("final.jpg", final)
def LOAD():
    print('1')
def SAVE():
    print('1')

def CLONE():
    global eyedrop
    global eyedrop_but
    eyedrop = "ON"
    eyedrop_but = tk.Button(tool, bg='#313131', fg='#00ff00', activebackground='#ffffff' ,activeforeground='#000000', font=('Courier', 18), text="EYE", command=CLONE)
    eyedrop_but.place(relx=0.75, rely=0.5, relwidth=0.1, relheight=1, anchor='center')
    root.update()

path = "./MangaImage/3.jpg"
img = cv2.imread(path)
original = cv2.imread(path)
final = cv2.imread(path)
cv2.namedWindow('Image' , cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('Image',mark)

pointer = 0
page_no = 0

root = tk.Tk()
root.title('Main menu')

H = 600  # กำหนดค่าตัวแปรความสูงหน้าต่างโปรแกรม
W = 900  # ตัวแปรความกว้าง

canvas = tk.Canvas(root, height=H, width=W, bg='#242424')
canvas.pack()

navi_frame = tk.Frame(canvas, bg='#7a7a7a', bd=5)
navi_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='center')

prompt = tk.StringVar()

page = tk.Label(navi_frame, bg='#303030', fg='#ffffff', font=('Courier', 24), textvariable=prompt)
page.place(relx=0.5, rely=0.5, relwidth=0.15, relheight=1, anchor='center')

before_frame = tk.Frame(canvas, bg='#7a7a7a', bd=5)
before_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.2, anchor='center')

before_text = tk.Text(before_frame, bg='#303030', fg='#ffffff', font=('Courier', 16))
before_text.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.9, anchor='center')

trans = tk.Frame(canvas, bg='#7a7a7a', bd=5)
trans.place(relx=0.5, rely=0.47, relwidth=0.75, relheight=0.08, anchor='center')

ocr_but = tk.Button(trans, bg='#313131', fg='#ffffff', activebackground='#ffffff' ,activeforeground='#000000', font=('Courier', 18), text="OCR", command=OCR)
ocr_but.place(relx=0.1, rely=0.5, relwidth=0.1, relheight=1, anchor='center')

trans_but = tk.Button(trans, bg='#313131', fg='#ffffff', activebackground='#ffffff' ,activeforeground='#000000', font=('Courier', 18), text="Trans", command=TRANS)
trans_but.place(relx=0.25, rely=0.5, relwidth=0.15, relheight=1, anchor='center')

pre_but = tk.Button(trans, bg='#313131', fg='#ffffff', activebackground='#ffffff' ,activeforeground='#000000', font=('Courier', 18), text="Pre", command=PRE)
pre_but.place(relx=0.4, rely=0.5, relwidth=0.15, relheight=1, anchor='center')

render_but = tk.Button(trans, bg='#313131', fg='#ffffff', activebackground='#ffffff' ,activeforeground='#000000', font=('Courier', 18), text="Rend", command=REND)
render_but.place(relx=0.55, rely=0.5, relwidth=0.15, relheight=1, anchor='center')

load_but = tk.Button(trans, bg='#313131', fg='#ffffff', activebackground='#ffffff' ,activeforeground='#000000', font=('Courier', 18), text="Load", command=LOAD)
load_but.place(relx=0.75, rely=0.5, relwidth=0.1, relheight=1, anchor='center')

save_but = tk.Button(trans, bg='#313131', fg='#ffffff', activebackground='#ffffff' ,activeforeground='#000000', font=('Courier', 18), text="Save", command=SAVE)
save_but.place(relx=0.9, rely=0.5, relwidth=0.1, relheight=1, anchor='center')

tool = tk.Frame(canvas, bg='#7a7a7a', bd=5)
tool.place(relx=0.5, rely=0.57, relwidth=0.75, relheight=0.08, anchor='center')

bg_color = tk.Text(tool, bg='#303030', fg='#ffffff', font=('Courier', 12))
bg_color.place(relx=0.1, rely=0.5, relwidth=0.2, relheight=0.9, anchor='center')
bg_color.insert(tk.END,"255,255,255")

fg_color = tk.Text(tool, bg='#303030', fg='#ffffff', font=('Courier', 12))
fg_color.place(relx=0.3, rely=0.5, relwidth=0.2, relheight=0.9, anchor='center')
fg_color.insert(tk.END,"0,0,0")

f_option = tk.StringVar()
f_option.set(font_option[0][0])

font_drop = tk.OptionMenu(tool, f_option, *font_option[0])
font_drop.config(bg='#313131', fg='#ffffff')
font_drop.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=1, anchor='center')

f_size = tk.Text(tool, bg='#303030', fg='#ffffff', font=('Courier', 16))
f_size.place(relx=0.66, rely=0.5, relwidth=0.06, relheight=0.9, anchor='center')
f_size.insert(tk.END,"16")

eyedrop_but = tk.Button(tool, bg='#313131', fg='#ffffff', activebackground='#ffffff' ,activeforeground='#000000', font=('Courier', 18), text="EYE", command=CLONE)
eyedrop_but.place(relx=0.75, rely=0.5, relwidth=0.1, relheight=1, anchor='center')

prompt_eye = tk.StringVar()

eye_dis = tk.Label(tool, bg='#303030', fg='#ffffff', font=('Courier', 8), textvariable=prompt_eye)
eye_dis.place(relx=0.9, rely=0.5, relwidth=0.2, relheight=1, anchor='center')

after_frame = tk.Frame(canvas, bg='#7a7a7a', bd=5)
after_frame.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.3, anchor='center')

after_text = tk.Text(after_frame, bg='#303030', fg='#ffffff', font=('Courier', 16))
after_text.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.9, anchor='center')

textboxes = list()
textboxes.append(textbox())

slide_canvas = tk.Canvas(root, height=50, width=900, bg='#7a7a7a')
slide_canvas.pack()

slider = tk.Scale(slide_canvas, from_=0, to=100, orient=tk.HORIZONTAL, borderwidth=0, highlightthickness=0, width=10, showvalue=0, bg='#7a7a7a', fg='#7a7a7a', length=900)
slider.pack()

while(1):
    cv2.imshow('Image',img[0 + int(slider_pos) :540 + int(slider_pos),:])
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    root.update()
    if len(textboxes[0].position) != 0:
        PRE()

    img_width, img_height= img.shape[:2]
    slider_pos = (slider.get()/100) * (img_height)
root.mainloop()
cv2.destroyAllWindows()