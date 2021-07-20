from tkinter import *
from tkinter import filedialog 
 
from cv2 import cvtColor, imread, COLOR_BGR2RGB
import numpy as np
from PIL import Image, ImageTk
from ctypes import windll

path = ''
img = []
newImg = []


#FUNCTIONS OPERATIONS

def grayScale():
    global img, newImg
    if(len(img) > 0):
        clearOtherPanels()
        newImg = np.zeros_like(img)
        average = np.average(img, axis=2)
        for i in range(3):
            newImg[:,:,i] = average[:,:]
        createPanelTop(newImg)
        

def invertColors():
    global img
    if(len(img) > 0):
        clearOtherPanels()
        newImg = np.zeros_like(img)
        newImg[:, :, 0] = 255 - (img[:, :, 0])
        newImg[:, :, 1] = 255 - (img[:, :, 1])
        newImg[:, :, 2] = 255 - (img[:, :, 2]) 
        createPanelTop(newImg)

def splitRGB():
    global img
    if(len(img) > 0):
        clearOtherPanels()
        for i in range(3):
            newColor = np.zeros_like(img)
            newColor[:, :, i] = (img[:, :, i])
            newColor = Image.fromarray(newColor)
            newSize = (round(newColor.size/2), round(newColor.size[1]/2))
            newColor = newColor.resize(newSize, Image.ANTIALIAS)
            newColor = np.array(newColor)
            createPanelBottom(newColor)
        

        
def insertCanvas():
    global panelsTop
    def paint( event ):
        x1, y1 = ( event.x - 1 ), ( event.y - 1 )
        x2, y2 = ( event.x + 1 ), ( event.y + 1 )
        panelsTop[0].create_oval( x1, y1, x2, y2, fill = "#000000" )
        drawPos(event)

    def drawPos(event):
        mousePos.set(f"{event.x}, {event.y}")
        

    
    clearOtherPanels()
    clearMainPanel()
    newCanvas = Canvas(frameTop, width=800, height=600, bg="white")
    panelsTop[0] = newCanvas
    panelsTop[0].pack(padx=20, pady=20)
    panelsTop[0].bind( "<B1-Motion>", paint)    
    panelsTop[0].bind( "<Motion>", drawPos)  
    window.bind( "<ButtonRelease-1>", drawPos)
    #entrys
    mousePos = StringVar()
    displayMousePos = Entry(frameBottom, state="readonly", width=10,textvariable=mousePos)
    mousePos.set("0,0")
    panelsTop.insert(1, displayMousePos)
    panelsTop[1].pack()
    #
    underMouseColor = StringVar()
    displayMousePos = Entry(frameBottom, state="readonly", width=10,textvariable=underMouseColor)
    underMouseColor.set("0,0,0")
    panelsTop.insert(1, displayMousePos)
    panelsTop[2].pack()
    
#DEFAULT OPERATIONS

def select_image():
    global panelsTop, img
    path = filedialog.askopenfilename(title='open')

    if(len(path) > 0):
        clearOtherPanels()
        clearMainPanel()
        img = imread(path)
        imgPrint = cvtColor(img, COLOR_BGR2RGB)
        imgPrint = ImageTk.PhotoImage(Image.fromarray(imgPrint))
    
        if panelsTop[0] is None:
            panelsTop[0]= Label(frameTop, image=imgPrint)
            panelsTop[0].image = imgPrint
            panelsTop[0].pack(side="left", padx=10, pady=10, )
        else: 
            panelsTop[0].configure(image=imgPrint)
            panelsTop[0].image = imgPrint

def clearMainPanel():
    global panelsTop, panelsBottom
    if len(panelsTop) == 1 and len(panelsBottom) == 0:
        if not(panelsTop[0] is None):
            panelsTop[0].destroy()


def clearOtherPanels():
    global panelsTop, panelsBottom
    if len(panelsTop) > 1:
        for widget in frameTop.winfo_children()[1:]:
            widget.destroy()
        if len(panelsBottom) > 0:
            for widget in frameBottom.winfo_children():
                widget.destroy()
        panelsTop = [frameTop.winfo_children()[0]]
        panelsBottom = []
        

def setMainImg():
    global newImg, img, panels
    if len(newImg) > 0:
        clearOtherPanels()
        img = newImg
        imgPrint = cvtColor(img, COLOR_BGR2RGB)
        imgPrint = ImageTk.PhotoImage(Image.fromarray(imgPrint))
        panelsTop[0].configure(image=imgPrint)
        panelsTop[0].image = imgPrint
        panelsTop[0].pack(side="left", padx=10, pady=10)

def save_image():
    global newImg
    if len(newImg) > 0:
        filename = filedialog.asksaveasfile(mode='w', title="messed up image", defaultextension=".jpg")
        if not filename:
            return
        imgPrint = cvtColor(newImg, COLOR_BGR2RGB)
        imgPrint = Image.fromarray(imgPrint)
        imgPrint.save(filename)

def createPanelTop(image):
    global panelsTop
    newImgPrint = cvtColor(image, COLOR_BGR2RGB)
    newImgPrint = ImageTk.PhotoImage(Image.fromarray(newImgPrint))
    newPanel = Label(frameTop, image=newImgPrint)
    newPanel.image = newImgPrint
    newPanel.pack(padx=10, pady=10)

    panelsTop.append(newPanel)

def createPanelBottom(image):
    global panelsBottom
    newImgPrint = cvtColor(image, COLOR_BGR2RGB)
    newImgPrint = ImageTk.PhotoImage(Image.fromarray(newImgPrint))
    newPanel = Label(frameBottom, image=newImgPrint)
    newPanel.image = newImgPrint
    newPanel.pack(side="left", padx=10, pady=10)

    panelsBottom.append(newPanel)
    print(panelsBottom)
    

def printToPanelB(printImg):
    global panelsTop, newImg
    if len(printImg) > 0:
        newImg = printImg
        newImgPrint = cvtColor(newImg, COLOR_BGR2RGB)
        newImgPrint = ImageTk.PhotoImage(Image.fromarray(newImgPrint)) 
        if panelsTop[1] is None:
            panelsTop[1] = Label(frameTop, image=newImgPrint)
            panelsTop[1].image = newImgPrint
            panelsTop[1].pack(side="right", padx=10, pady=10)
        else:
            panelsTop[1].configure(image=newImgPrint)
            panelsTop[1].image = newImgPrint


#--


#DISPLAY
window = Tk()
window.title("Image Manipulation App")
window.minsize(300, 400)

mainPanel = None
panelsTop = [mainPanel]
panelsBottom = []

menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=select_image)
filemenu.add_command(label="Set Secondary Image as Primary", command=setMainImg)
filemenu.add_command(label="Save", command=save_image)
filemenu.add_separator()
filemenu.add_command(label="Clear Primary", command=clearMainPanel)
filemenu.add_command(label="Clear Other Panels", command=clearOtherPanels)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
functions = Menu(menubar, tearoff=0)
functions.add_command(label="To Gray Scale", command=grayScale)
functions.add_command(label="Invert Colors", command=invertColors)
functions.add_command(label="Split Colors", command=splitRGB)
functions.add_command(label="Insert Canvas", command=insertCanvas)
menubar.add_cascade(label="Functions", menu=functions)

frameTop = Frame()
frameTop.pack(side="top")
frameBottom = Frame()
frameBottom.pack(side="top")

window.config(menu=menubar)
window.mainloop()
