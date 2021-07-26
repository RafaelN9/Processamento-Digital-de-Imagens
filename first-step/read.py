from tkinter import *
from tkinter import filedialog

import numpy as np
import random as rng
from cv2 import COLOR_BGR2RGB, cvtColor, imread
from numpy.core.fromnumeric import shape
from numpy.core.records import array
from PIL import Image, ImageTk


def to_hex(c):
    c = c[:3]
    return "#" + "".join(format(int(np.round(val)), "02x")
                         for val in c)
                         
path = ''
img = []
newImg = []

#FUNCTIONS OPERATIONS

#F 1 ------------------------------------------------

def grayScale():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        newImg = np.zeros_like(img)
        average = np.average(img, axis=2)
        for i in range(3):
            newImg[:,:,i] = average[:,:]
        createPanelTop(newImg)
        
def invertColors():
    global img, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        newImg = np.zeros_like(img)
        newImg[:, :, 0] = 255 - (img[:, :, 0])
        newImg[:, :, 1] = 255 - (img[:, :, 1])
        newImg[:, :, 2] = 255 - (img[:, :, 2]) 
        createPanelTop(newImg)

def splitRGB():
    global img, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        for i in range(3):
            newColor = np.zeros_like(img)
            newColor[:, :, i] = (img[:, :, i])
            newColor = Image.fromarray(newColor)
            newSize = (round(newColor.size[0]/2), round(newColor.size[1]/2))
            newColor = newColor.resize(newSize, Image.ANTIALIAS)
            newColor = np.array(newColor)
            createPanelBottom(newColor)
              
def insertCanvas():
    global panelsTop, img
    if panelsTop[0] == None:
        return
    elif len(panelsTop) > 1 or len(panelsBottom) > 0: 
        clearOtherPanels()
    p1 = [] 
    p2 = []
    lineMode = [False]

    def paint( event ):
        if lineMode[0]:
            if len(p1) == 0 and len(p2) == 0:
                p1.append(event.x)
                p1.append(event.y)
        else:
            x1, y1 = ( event.x - 1 ), ( event.y - 1 )
            x2, y2 = ( event.x + 1 ), ( event.y + 1 )
            panelsTop[0].create_oval( x1, y1, x2, y2, fill = "#000000" )
            drawPos(event)

    def drawPos(e):
        mousePos.set(f"{e.x}, {e.y}")
        if e.x < len(img[0]) and e.y < len(img):
            pixel = cvtColor(img, COLOR_BGR2RGB)[e.y, e.x]
            panelsBottom[1].config(bg=to_hex(pixel))

    def drawLine(event):
        if not(lineMode[0]):
            return
        if len(p1) > 0 and len(p2) == 0:
            p2.append(event.x)
            p2.append(event.y)
            panelsTop[0].create_line(p1[0], p1[1], p2[0], p2[1])
            p1.clear()
            p2.clear()

    def toggleLineMode():
        lineMode[0] = not(lineMode[0])
        if lineMode[0]:
            btnToggleLineMode.config(bg="gray")
        else: btnToggleLineMode.config(bg="white")

    def clearCanvas():
        panelsTop[0].delete('all')
        panelsTop[0].create_image(0, 0, image=canvasImage, anchor=NW)
         
    clearAll()

    imgSize = Image.fromarray(img)
    window.canvasImage = canvasImage = ImageTk.PhotoImage(Image.fromarray(cvtColor(img, COLOR_BGR2RGB)))
    newCanvas = Canvas(frameTop, width=imgSize.size[0], height=imgSize.size[1], bg="white")
    newCanvas.pack(padx=20, pady=20)
    newCanvas.create_image(0, 0, image=canvasImage, anchor=NW)
    

    
    panelsTop[0] = newCanvas
    window.bind( "<ButtonRelease-1>", drawLine)

    frameToolBox = Frame(frameBottom)
    frameToolBox.pack()

    btnToggleLineMode = Button(frameToolBox, command=toggleLineMode, text="Modo Linha")
    btnToggleLineMode.grid(row=0, column=0, pady=2, sticky=NSEW)

    mousePos = StringVar()
    displayMousePos = Entry(frameToolBox, state="readonly", width=10, textvariable=mousePos)
    mousePos.set("0,0")
    displayMousePos.grid(row=0, column=1, pady=2, sticky=NSEW)
    panelsBottom.append(displayMousePos)
    
    pixelColorBox = Label(frameToolBox, width=10, height=3)
    pixelColorBox.grid(row=0, column=2, pady=1, sticky=NSEW)
    panelsBottom.append(pixelColorBox)

    btnClearCanvas = Button(frameToolBox, command=clearCanvas, text="Limpar Canvas")
    btnClearCanvas.grid(row=0, column=3, pady=2, sticky=NSEW)

    panelsTop[0].bind( "<B1-Motion>", paint)    
    panelsTop[0].bind( "<Motion>", drawPos)  

def noiseImages():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        noisedImages = []
        sumMatrix = np.zeros_like(img)
        width = img.shape[0]-1
        height = img.shape[1]-1
        for i in range(10):
            noisedImg = img
            rngListW = rng.sample(range(width), 20)
            rngListH = rng.sample(range(height), 20)

            for j in range(round(len(img)/10)):
                noisedImg[rngListW[i], rngListH[i]] = 255
                noisedImg[rngListW[i+1], rngListH[i+1]] = 0
            sumMatrix[:,:] += noisedImg[:,:]
            noisedImages.append(noisedImg)
        sumMatrix[:,:] = np.around(sumMatrix[:,:]/10)
        noisedImages.insert(0, sumMatrix)

        def printSelImg(imgSel):
            clearTopPanels()
            imgSel = noisedImages[int(imgNamesList.get()[-1])]
            createPanelTop(imgSel)

        imgNames = []
        for i in range(len(noisedImages)):
            imgNames.append("Image "+str(i+1))

        imgNamesList = StringVar()
        imgNamesList.set(imgNames[0])
        dropdown = OptionMenu(frameBottom, imgNamesList, *imgNames, command=printSelImg)
        dropdown.pack(expand=True)
        panelsBottom.append(dropdown)

#F 2 ------------------------------------------------ 

def dynamicCompression():
    global img
    if len(img) > 0:
        clearOtherPanels()

        def filterImg():
            clearTopPanels()
            constVar = float(const.get().replace(',',''))
            gamaVar = float(gama.get().replace(',',''))
            newImg = np.zeros_like(img)
            for i in range(3):
                newImg[:,:,i] = pow((constVar * img[:,:, i]), gamaVar)
            createPanelTop(newImg)

        frameToolBox = Frame(frameBottom)
        frameToolBox.pack(pady=15)

        labelConst = Label(frameToolBox, text="Insira a Constante")
        labelConst.grid(row=0, column=1)
        panelsBottom.append(labelConst)
        const = StringVar()
        inputConst = Entry(frameToolBox, width=20, textvariable=const)
        const.set("1")
        inputConst.grid(row=1, column=1)
        panelsBottom.append(inputConst)

        labelGama = Label(frameToolBox, text="Insira o Gama")
        labelGama.grid(row=0, column=2)
        panelsBottom.append(labelGama)
        gama = StringVar()
        inputGama = Entry(frameToolBox, width=20, textvariable=gama)
        gama.set("1")
        inputGama.grid(row=1, column=2)
        panelsBottom.append(inputGama)
        
        btnFilter = Button(frameToolBox, command=filterImg, text="Fazer Compressão")
        btnFilter.grid(row=0, rowspan=2, column=3, padx=10, sticky=NSEW)
        panelsBottom.append(btnFilter)

def average3x3():
    global img, newImg
    if len(img) > 0:
        clearOtherPanels()
        newImg = np.zeros_like(img)
        for i in range(1,len(newImg)-1):
            for j in range(1,len(newImg[0])-1):
                                    #Left           Top Left        Top         Right        TopRight      Bottom       Bottom Left    Bottom Right
                avgArray = np.array([img[i-1, j] ,img[i-1, j-1] ,img[i, j-1] ,img[i+1, j] ,img[i+1, j-1] ,img[i, j+1] ,img[i-1, j+1], img[i+1, j+1]])
                newImg[i, j] = np.around(np.average(avgArray, axis=0)) 
        createPanelTop(newImg)

def median3x3():
    global img, newImg
    if len(img) > 0:
        clearOtherPanels()
        newImg = np.zeros_like(img)
        for i in range(1,len(newImg)-1):
            for j in range(1,len(newImg[0])-1):
                                    #Left           Top Left        Top         Right        TopRight      Bottom       Bottom Left    Bottom Right
                medianArray = np.array([img[i-1, j] ,img[i-1, j-1] ,img[i, j-1] ,img[i+1, j] ,img[i+1, j-1] ,img[i, j+1] ,img[i-1, j+1], img[i+1, j+1]])
                medianArray = np.sort(medianArray, axis=0)
                medianElement = medianArray[round(len(medianArray)/2)]
                newImg[i, j] = medianElement
        createPanelTop(newImg)

def sobel():
    global img, newImg
    if len(img) > 0:
        clearOtherPanels()
        newImg = np.zeros_like(img)
        imgGrayScale = np.zeros_like(img)
        imgGrayScale = np.average(img, axis=2)
        for i in range(1,len(newImg)-1):
            for j in range(1,len(newImg[0])-1):
                                            #Left           Top Left        Top             Right            TopRight      Bottom       Bottom Left    Bottom Right
                sobelArrayX = np.array([imgGrayScale[i-1, j]*-2 ,imgGrayScale[i-1, j-1]*-1 ,0     ,imgGrayScale[i+1, j]*2 ,imgGrayScale[i+1, j-1]*1  ,0  ,imgGrayScale[i-1, j+1]*-1, imgGrayScale[i+1, j+1]*1])
                sobelArrayY = np.array([ 0    ,imgGrayScale[i-1, j-1]*-1 ,imgGrayScale[i, j-1]*-2 ,0    ,imgGrayScale[i+1, j-1]*-1 ,imgGrayScale[i, j+1] ,imgGrayScale[i-1, j+1]*1, imgGrayScale[i+1, j+1]*1])
                sobelElementX = np.sum(sobelArrayX)
                sobelElementY = np.sum(sobelArrayY)
                newImg[i, j] = np.around(np.sqrt(sobelElementX**2 + sobelElementY**2))
        createPanelTop(newImg)

#DEFAULT OPERATIONS

def clearAll():
    if len(panelsTop) > 0:
        clearOtherPanels()
        clearMainPanel()

def select_image():
    global panelsTop, img
    path = filedialog.askopenfilename(title='open')

    if(len(path) > 0):
        clearAll()
        
        img = imread(path)
        imgPrint = cvtColor(img, COLOR_BGR2RGB)
        imgPrint = ImageTk.PhotoImage(Image.fromarray(imgPrint))
    
        if panelsTop[0] is None:
            panelsTop[0]= Label(frameTop, image=imgPrint)
            panelsTop[0].image = imgPrint
            panelsTop[0].pack(side="left", padx=10, pady=10)
        else: 
            panelsTop[0].configure(image=imgPrint)
            panelsTop[0].image = imgPrint
        noiseImages()

def clearMainPanel():
    global panelsTop, panelsBottom
    if len(panelsTop) == 1 and len(panelsBottom) == 0:
        if not(panelsTop[0] is None):
            panelsTop[0].destroy()
            panelsTop[0] = None

def clearOtherPanels():
    global panelsTop, img
    
    clearTopPanels()
    clearBottomPanels()
    
    if type(panelsTop[0]) is Canvas: 
        clearMainPanel()
        imgPrint = ImageTk.PhotoImage(Image.fromarray(cvtColor(img, COLOR_BGR2RGB)))
        panelsTop[0]= Label(frameTop, image=imgPrint)
        panelsTop[0].image = imgPrint
        panelsTop[0].pack(side="left", padx=10, pady=10)

def clearTopPanels():
    global panelsTop
    if len(panelsTop) > 1:
        for widget in frameTop.winfo_children()[1:]:
            widget.destroy()
        panelsTop = [frameTop.winfo_children()[0]]

def clearBottomPanels():
    global panelsBottom
    if len(panelsBottom) > 0:
        for widget in frameBottom.winfo_children():
            widget.destroy()
        panelsBottom = []

def setMainImg():
    global newImg, img, panelsTop
    if len(newImg) > 0 and len(panelsTop) > 1:
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
filemenu.add_command(label="Clear All", command=clearAll)
filemenu.add_command(label="Reset to only Primary", command=clearOtherPanels)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
functions = Menu(menubar, tearoff=0)
functions.add_command(label="To Gray Scale", command=grayScale)
functions.add_command(label="Invert Colors", command=invertColors)
functions.add_command(label="Split Colors", command=splitRGB)
functions.add_command(label="Insert Canvas Around Image", command=insertCanvas)
menubar.add_cascade(label="Functions 1", menu=functions)
functions2 = Menu(menubar, tearoff=0)
functions2.add_command(label="Compressão de escala dinâmica", command=dynamicCompression)
functions2.add_command(label="Limiarização", command=())
functions2.add_command(label="Equalização de Histograma", command=())
filters = Menu(functions2, tearoff=0)
filters.add_command(label="Média 3x3", command=average3x3)
filters.add_command(label="Mediana 3x3", command=median3x3)
filters.add_command(label="Laplaciano", command=())
filters.add_command(label="Sobel", command=sobel)
functions2.add_cascade(label="Filters", menu=filters)
menubar.add_cascade(label="Functions 2", menu=functions2)
functions3 = Menu(menubar, tearoff=0)
functions3.add_command(label="Mostrar transformada do cosseno", command=())
functions3.add_command(label="Mostrar inversa da transformada", command=())
functions3.add_command(label="Inserir ruído", command=())
filters = Menu(functions2, tearoff=0)
filters.add_command(label="Passa-alta", command=())
filters.add_command(label="Passa-baixa", command=())
functions3.add_cascade(label="Filtro na Transformada", menu=filters)
filters = Menu(functions3, tearoff=0)
menubar.add_cascade(label="Functions 3", menu=functions2)



frameTop = Frame()
frameTop.pack(side="top")
frameBottom = Frame()
frameBottom.pack(side="top", fill="x", padx=3)

window.config(menu=menubar)
window.mainloop()
