import random as rng
from math import pi
from tkinter import *
from tkinter import filedialog

import cv2
import numpy as np
from cv2 import COLOR_BGR2RGB, COLOR_RGB2GRAY, THRESH_BINARY, THRESH_OTSU,  threshold, cvtColor, imread, equalizeHist
from matplotlib import pyplot as plt
from numpy.core import numerictypes
from numpy.core.fromnumeric import shape
from numpy.core.numeric import zeros_like
from numpy.core.records import array
from PIL import Image, ImageTk


def to_hex(c):
    c = c[:3]
    return "#" + "".join(format(int(np.round(val)), "02x")
                         for val in c)
                         
path = ''
img = []
newImg = []
cossSum = []

#FUNCTIONS OPERATIONS

#F 1 ------------------------------------------------

def toGrayScale(image):
    return np.average(image, axis=2)

def splitChannels(image):
    newImg = np.zeros_like(img, shape=(image.shape[0],image.shape[1], 3))
    for i in range(3):
        newImg[:,:,i] = image[:,:]
    return newImg

def grayScale():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        newImg = np.zeros_like(img)
        average = toGrayScale(img)
        newImg = splitChannels(average)
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

def generateNoisedImage(baseImg, percent):
    area = baseImg.shape[0] * baseImg.shape[1]
    newImage = np.copy(baseImg)
    for i in range(round(area * percent)):
        x = rng.randint(0, baseImg.shape[0]-1)
        y = rng.randint(0, baseImg.shape[1]-1)
        color = rng.randint(0, 1) * 255
        newImage[x,y] = [color, color, color]
    return newImage
    
def noiseImages():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        noisedImages = []
        for i in range(10):
            noisedImages.append(generateNoisedImage(img, 0.1))
        
        sumMatrix = np.zeros(img.shape, dtype=int)
        for noisedImg in noisedImages:
            sumMatrix += noisedImg
        sumMatrix = round(sumMatrix / len(noisedImages))
        newImg = np.uint8(sumMatrix)
        
        def printSelImg(imgSel):
            clearTopPanels()
            imgSel = noisedImages[int(imgNamesList.get()[-1])]
            createPanelTop(imgSel)

        def printAverage():
            clearTopPanels()
            createPanelTop(newImg)

        imgNames = []
        for i in range(len(noisedImages)):
            imgNames.append("Image "+str(i+1))

        imgNamesList = StringVar()
        imgNamesList.set(imgNames[0])
        dropdown = OptionMenu(frameBottom, imgNamesList, *imgNames, command=printSelImg)
        dropdown.pack(expand=True)
        panelsBottom.append(dropdown)
        btnAvrgImg = Button(frameBottom, text="Imagem Média", command=printAverage)
        btnAvrgImg.pack()
        panelsBottom.append(btnAvrgImg)

def HSLandRGB():
    clearAll()
    hPrev = 160; sPrev = 0; lPrev = 0
    RPrev = 0; GPrev = 0; BPrev = 0
    prevMatrix = [[hPrev, sPrev, lPrev], [RPrev, GPrev, BPrev]]
    def focus(e):

        def RGB2HSL(rgb):
            r_ = rgb[0]/255; g_ = rgb[1]/255; b_ = rgb[2]/255
            cMax = max(r_, g_, b_)
            cMin = min(r_, g_, b_)
            delta = cMax - cMin
            L = (cMax + cMin)/2
            if delta == 0:
                return [0, 0, L]
            # ------ L ------
            if r_ == cMax:
                H = 60 * ((g_-b_/delta) % 6)
            elif g_ == cMax:
                H = 60 * ((b_-r_/delta) + 2)
            elif b_ == cMax:
                H = 60 * ((r_-g_/delta) + 4)
            # ------ H ------
            S = delta / (1 - abs(2*L-1))
            # ------ S ------

            return [H, S*100, L*100]
        
        def HSL2RGB(hsl):
            hsl[1] /= 100
            hsl[2] /= 100
            C = (1 - abs((2*hsl[2])-1))* hsl[1]
            X = C * (1 - abs(((hsl[0]/60)%2) - 1))
            m = hsl[2]-(C/2)

            if 0 <= hsl[0] < 60:      rgb_ = [C, X, 0]
            elif 60 <= hsl[0] < 120:  rgb_ = [X, C, 0]
            elif 120 <= hsl[0] < 180: rgb_ = [0, C, X]
            elif 180 <= hsl[0] < 240: rgb_ = [0, X, C]
            elif 240 <= hsl[0] < 300: rgb_ = [X, 0, C]
            else:                     rgb_ = [C, 0, X]
            rgb_ = np.array(rgb_)
            rgb = (rgb_ + m)*255
            return rgb

        if h.get() != prevMatrix[0][0] or s.get() != prevMatrix[0][1] or l.get() != prevMatrix[0][2]:
            prevMatrix[0][0] = h.get(); prevMatrix[0][1] = s.get(); prevMatrix[0][2] = l.get()
            
            if prevMatrix[0][0] < 0: h.set(0); prevMatrix[0][0] = 0
            if prevMatrix[0][1] < 0: s.set(0); prevMatrix[0][1] = 0
            if prevMatrix[0][2] < 0: l.set(0); prevMatrix[0][2] = 0

            if prevMatrix[0][0] > 360: h.set(360); prevMatrix[0][0] = 360
            if prevMatrix[0][1] > 100: s.set(100); prevMatrix[0][1] = 100
            if prevMatrix[0][2] > 100: l.set(100); prevMatrix[0][2] = 100
            
            hsl2rgb = HSL2RGB(prevMatrix[0])
            R.set(hsl2rgb[0])
            G.set(hsl2rgb[1])
            B.set(hsl2rgb[2])
            showColor.config(bg=to_hex(hsl2rgb))
            prevMatrix[1] = hsl2rgb
        
        if R.get() != prevMatrix[1][0] or G.get() != prevMatrix[1][1] or B.get() != prevMatrix[1][2]:
            prevMatrix[1][0] = R.get(); prevMatrix[1][1] = G.get(); prevMatrix[1][2] = B.get()
            
            if prevMatrix[1][0] < 0: R.set(0); prevMatrix[1][0] = 0
            if prevMatrix[1][1] < 0: G.set(0); prevMatrix[1][1] = 0
            if prevMatrix[1][2] < 0: B.set(0); prevMatrix[1][2] = 0

            if prevMatrix[1][0] > 255: R.set(255); prevMatrix[1][0] = 255
            if prevMatrix[1][1] > 255: G.set(255); prevMatrix[1][1] = 255
            if prevMatrix[1][2] > 255: B.set(255); prevMatrix[1][2] = 255

            rgb2hsl = RGB2HSL(prevMatrix[1])
            h.set(rgb2hsl[0])
            s.set(rgb2hsl[1])
            l.set(rgb2hsl[2])
            showColor.config(bg=to_hex(prevMatrix[1]))
            prevMatrix[0] = rgb2hsl
        
        

    titulo = Label(frameBottom, text="Pressione enter para fazer a conversão")
    titulo.pack(pady=8, padx=8, fill="both")

    frameBox = Frame(frameBottom)
    frameBox.pack()
    window.bind('<Return>', focus)
    panelsBottom.append(frameBox)

    colorBox = Label(frameBox, width=20, height=8)#Entry(frameBox, state="readonly", width=20, textvariable=8ousePos)
    colorBox.grid(row=0, column=1, pady=2, sticky=NSEW)
    showColor = Label(colorBox, bg="black", width=12, height=7)
    showColor.pack(pady=8, padx=8, fill="both")
    
    HSLBox = Label(frameBox, width=20, height=8)
    HSLBox.grid(row=0, column=2, pady=15, padx=15, sticky=NSEW)
    h = DoubleVar(); s = DoubleVar(); l = DoubleVar()
    h.set(160.0);   s.set(0.0);     l.set(0.0)
    HLabel = Label(HSLBox, text="Hue: ")            .grid(row=0, column=0, pady=5, padx=15, sticky=E)
    HEntry = Entry(HSLBox, width=10, textvariable=h).grid(row=0, column=1, pady=5, padx=8, sticky=NSEW)
    SLabel = Label(HSLBox, text="Saturation:")      .grid(row=1, column=0, pady=5, padx=15, sticky=E)
    SEntry = Entry(HSLBox, width=10, textvariable=s).grid(row=1, column=1, pady=5, padx=8, sticky=NSEW)
    LLabel = Label(HSLBox, text="Luminosity:")       .grid(row=2, column=0, pady=5, padx=15, sticky=E)
    LEntry = Entry(HSLBox, width=10, textvariable=l).grid(row=2, column=1, pady=5, padx=8, sticky=NSEW)

    RGBBox = Label(frameBox, width=20, height=8)
    RGBBox.grid(row=0, column=3, pady=15, padx=15, sticky=NSEW)
    R = DoubleVar(); G = DoubleVar(); B = DoubleVar()
    R.set(0.0);   G.set(0.0);     B.set(0.0)
    RLabel = Label(RGBBox, text="Red: ").grid (row=0, column=0, pady=5, padx=15, sticky=E)
    REntry = Entry(RGBBox, width=10, textvariable=R).grid     (row=0, column=1, pady=5, padx=8, sticky=NSEW)
    GLabel = Label(RGBBox, text="Green:").grid(row=1, column=0, pady=5, padx=15, sticky=E)
    GEntry = Entry(RGBBox, width=10, textvariable=G).grid     (row=1, column=1, pady=5, padx=8, sticky=NSEW)
    BLabel = Label(RGBBox, text="Blue:").grid (row=2, column=0, pady=5, padx=15, sticky=E)
    BEntry = Entry(RGBBox, width=10, textvariable=B).grid     (row=2, column=1, pady=5, padx=8, sticky=NSEW)


#F 2 ------------------------------------------------ 

def insertNoise():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        def printNoisedImg():
            clearTopPanels()
            ammount = float(noiseAmmount.get())
            newImg = generateNoisedImage(img, ammount/100)
            createPanelTop(newImg)

        noiseAmmount = StringVar()
        noiseAmmEntry = Entry(frameBottom, textvariable=noiseAmmount)
        noiseAmmEntry.pack(expand=True)
        panelsBottom.append(noiseAmmEntry)
        btnNoise = Button(frameBottom, text="Confirmar", command=printNoisedImg)
        btnNoise.pack()
        panelsBottom.append(btnNoise)

def normalizer(matriz):
    return np.around(((matriz - matriz.min()) / (matriz.max() - matriz.min()))* 255)

def convolucao(matrizMascara, matrizImagem, multiplier):

    matrizImagem = toGrayScale(matrizImagem)
    hImg = len(matrizImagem)
    wImg = len(matrizImagem[0])
    lenMasc = len(matrizMascara)
    
    newMatrixH = (1 - lenMasc) + hImg
    newMatrixW = (1 - lenMasc) + wImg
    newMatrix = np.zeros((newMatrixH, newMatrixW), dtype=int)
    for i in range(newMatrixH):
        for j in range(newMatrixW):
            convSum = []
            
            for x in range(lenMasc):
                for y in range(lenMasc):
                    convSum.append(matrizImagem[i+x, j+y] *  matrizMascara[x][y])
            
            newMatrix[i, j] = int(round(multiplier * np.sum(convSum)))
    
    return newMatrix#imagemConv

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
        avgArray = np.array([[1, 1, 1],
                             [1, 1, 1],
                             [1, 1, 1]])
        newImg = convolucao(avgArray, img, (1/9)) 
        newImg = splitChannels(newImg)
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
        sobelMaskX = np.array([[-1, 0, 1],
                               [-2, 0, 2],
                               [-1, 0, 1]])
        sobelMaskY = np.array([[-1,-2,-1],
                               [ 0, 0, 0],
                               [ 1, 2, 1]])
        sobelArrayX = convolucao(sobelMaskX, img, 1)
        sobelArrayY = convolucao(sobelMaskY, img, 1)
        magnitude = np.zeros_like(sobelArrayX)
        for i in range(sobelArrayX.shape[0]):
            for j in range(sobelArrayY.shape[1]):
                magnitude[i, j] = np.sqrt(sobelArrayX[i, j]**2 + sobelArrayY[i, j]**2)
        magnitude = normalizer(magnitude)
        newImg = np.uint8(magnitude)
        createPanelTop(newImg)

def Laplaciano():
    global img, newImg
    if len(img) == 0:
        return
    clearOtherPanels()
    matrizMascara = np.array([[0, 1, 0],
                              [1, -4, 1],
                              [0, 1, 0] ])
    newImg = convolucao(matrizMascara, img, (1))
    newImg = normalizer(newImg) 
    newImg = splitChannels(newImg)
    createPanelTop(newImg)

#F 3 -------------------------------------------------

def EQdeHistograma():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        if len(newImg) == 0:
            newImg = zeros_like(img)
        newImg = cvtColor(img, COLOR_RGB2GRAY)
        newImg = equalizeHist(newImg)
        createPanelTop(newImg)
                
def operacaoOTSU():
    global img
    if len(img) == 0:
        return
    newImg = toGrayScale(img)
    pI = np.zeros(256) 
    ni = np.zeros(256) 
    n = img.shape[0] * img.shape[1] 
    nmin = -1.0
    for i in range(256):
        ni[i] = 0.0
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            ni[int(newImg[x, y])] += 1
    for i in range(256):
        pI[i]=ni[i]/n
    uT = 0.0
    for i in range(256):
        uT += i*pI[i]
    SigT2 = 0.0
    for i in range(256):
        SigT2 += ((i-uT)**2)*pI[i]
    j = -1; k = -1
    for i in range(256):
        if (j<0) and (pI[i] > 0.0): j = i 
        if pI[i] > 0.0: k = i
    
    for t in range(j, k):
        ut = 0.0
        for i in range(t):
            ut += i * pI[i]
        w0 = 0.0
        for i in range(t):
            w0 += pI[i]
        x = uT * w0 - ut
        x *= x
        y = w0 * (1.0 - w0)
        if (y > 0.0):
            x = x / y
        else:
            x = 0.0
        SigB2 = x
        nf = SigB2 / SigT2
        if (nf >= nmin):
            nmin = nf
            Threshold = t - 1
    return Threshold

def LimiarizacaoPassaAlta():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        def printLimiarImg():
            global newImg
            clearTopPanels()
            limiarVal = float(limiar.get())
            print(limiarVal)
            newImg = zeros_like(img)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img[i, j, 0] > limiarVal:
                        newImg[i, j] = img[i, j]
            newImg = np.uint8(newImg)
            createPanelTop(newImg)

        limiar = StringVar()
        limiarEntry = Entry(frameBottom, textvariable=limiar)
        limiarEntry.pack(expand=True)
        panelsBottom.append(limiarEntry)
        btnLimiar = Button(frameBottom, text="Confirmar", command=printLimiarImg)
        btnLimiar.pack()
        panelsBottom.append(btnLimiar)

def LimiarizacaoOTSU():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        limiarVal = operacaoOTSU()
        if len(newImg) == 0:
            newImg = zeros_like(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j, 0] > limiarVal:
                    newImg[i, j] = img[i, j]
        createPanelTop(newImg)

def BinarizacaoOTSU():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        limiarVal = operacaoOTSU()
        if len(newImg) == 0:
            newImg = zeros_like(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j, 0] > limiarVal:
                    newImg[i, j] = np.array([255, 255, 255])
        createPanelTop(newImg)

def LimiarizacaoPassaBaixa():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        def printLimiarImg():
            global newImg
            clearTopPanels()
            limiarVal = float(limiar.get())
            newImg = zeros_like(img)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img[i, j, 0] <= limiarVal:
                        newImg[i, j] = img[i, j]
            newImg = np.uint8(newImg)
            createPanelTop(newImg)

        limiar = StringVar()
        limiarEntry = Entry(frameBottom, textvariable=limiar)
        limiarEntry.pack(expand=True)
        panelsBottom.append(limiarEntry)
        btnLimiar = Button(frameBottom, text="Confirmar", command=printLimiarImg)
        btnLimiar.pack()
        panelsBottom.append(btnLimiar)

def operacaoZangSuen():
    global img
    if(len(img) > 0):
        img = toGrayScale(img)
        img = img/255
        newImg = np.copy(img)
        keepGoing = True
        itera =0
        def contTransform(areaAtual):
            matrizS = list(areaAtual[1:])
            cont = 0
            for i in range(len(matrizS)):
                if matrizS[i-1] == 0 and matrizS[i] == 1:
                    cont += 1
            return cont == 1
                
                        
        while keepGoing and itera < 25:
            keepGoing = False
            markForDelete = []
            for i in range(1, newImg.shape[0]-1):
                for j in range(1, newImg.shape[1]-1):
                    areaAtual = [newImg[i, j],     newImg[i, j+1],    newImg[i+1, j+1],
                                newImg[i+1, j],   newImg[i+1, j-1],  newImg[i, j-1], 
                                newImg[i-1, j-1], newImg[i-1, j],    newImg[i-1, j+1]]
                    if 2 <= sum(areaAtual[1:]) <= 6:
                        if contTransform(areaAtual):
                            if areaAtual[1] * areaAtual[3] * areaAtual[5] == 0: 
                                if areaAtual[3] * areaAtual[5] * areaAtual[7] == 0:
                                    markForDelete.append([i, j])
            for delete in markForDelete:
                newImg[delete[0], delete[1]] = 0
                keepGoing = True
            markForDelete = []
            for i in range(1, newImg.shape[0]-1):
                for j in range(1, newImg.shape[1]-1):
                    areaAtual = [newImg[i, j],     newImg[i, j+1],    newImg[i+1, j+1],
                                newImg[i+1, j],   newImg[i+1, j-1],  newImg[i, j-1], 
                                newImg[i-1, j-1], newImg[i-1, j],    newImg[i-1, j+1]]
                    if 2 <= sum(areaAtual[1:]) <= 6:
                        if contTransform(areaAtual):
                            if areaAtual[1] * areaAtual[3] * areaAtual[7] == 0: 
                                if areaAtual[1] * areaAtual[5] * areaAtual[7] == 0:
                                    markForDelete.append([i, j])

            for delete in markForDelete:
                newImg[delete[0], delete[1]] = 0
                keepGoing = True
            itera += 1
            print(itera)
            
        clearOtherPanels()
        imagePrint = np.uint8(newImg*255)
        createPanelTop(imagePrint)
        
    
#F 4 -------------------------------------------------


def transformaCosseno():
    global img, newImg, cossSum
    if not len(img):
        return 
    matrizImagem = toGrayScale(img)
    hImg = len(matrizImagem)
    wImg = len(matrizImagem[0])

    def alpha(x, N):
        if(x==0):
            return 1/((N)**(1/2))
        return (2/N)**(1/2)

    def cosFunc(x, i, N):
        exp = ((2*x + 1)*i*3)/(2*N)
        return np.cos(exp)
    
    cossSum = np.zeros(shape=(hImg, wImg))
    cossInversaSum = np.zeros(shape=(hImg, wImg))
    cossXArray = np.zeros(shape=(hImg, hImg))
    cossYArray = np.zeros(shape=(wImg, wImg))
    cossXArrayInv = np.zeros(shape=(hImg, hImg))
    cossYArrayInv = np.zeros(shape=(wImg, wImg))
    for j in range(wImg):
        for y in range(wImg):
            cossYArray[j, y] = cosFunc(y, j, wImg)
    for i in range(hImg):
        for x in range(hImg):
            cossXArray[i, x] = cosFunc(x, i, hImg)
        
      
    for i in range(hImg):
        for j in range(wImg):
            mult = [[cossXArray[i, x] * matrizImagem[x, :] * cossYArray[j, :]] for x in range(hImg)]
            cossSum[i,j] = alpha(i, hImg) * alpha(j, wImg) * np.sum(mult)
            
            if(i==j):
                perc = round(i/((hImg+wImg)/2), 3)
                if(np.mod((perc * 100), 10) <= 1):
                    print(str(perc*100)+"%")


    cossSumNorm = normalizer(cossSum)
    newImg = np.uint8(cossSumNorm)
    newImg = splitChannels(newImg)
    return newImg

def transformaInversaCosseno():
    global img, newImg, cossSum
    if not len(newImg) and not len(img):
        return 
    matrizImagem = cossSum
    hImg = len(matrizImagem)
    wImg = len(matrizImagem[0])

    def alpha(i, N):
        if(i==0):
            return 1/((N)**(1/2))
        return (2/N)**(1/2)

    def cosFunc(x, i, N):
        exp = ((2*x + 1)*i*3)/(2*N)
        return np.cos(exp)
    
    cossSum = np.zeros(shape=(hImg, wImg))
    cossXArray = np.zeros(shape=(hImg, hImg))
    cossYArray = np.zeros(shape=(wImg, wImg))
    for y in range(wImg):
        for j in range(wImg):
            cossYArray[j, y] = cosFunc(y, j, wImg) * alpha(j, wImg) 
    for x in range(hImg):
        for i in range(hImg):
            cossXArray[i, x] = cosFunc(x, i, hImg) * alpha(i, hImg)
      
    for x in range(hImg):
        for y in range(wImg):
            mult = [[cossXArray[i, x] * matrizImagem[i, :] * cossYArray[:, y]] for i in range(hImg)]
            cossSum[x,y] = np.sum(mult)
            
            if(x==y):
                perc = round(x/((hImg+wImg)/2), 3)
                if(np.mod((perc * 100), 10) <= 1):
                    print(str(perc*100)+"%")
        
    cossSum = normalizer(cossSum)
    img = np.uint8(cossSum)
    img = splitChannels(img)
    return img

def transformadaCompleta():
    global img, newImg, cossSum
    if not len(img):
        return
    if len(cossSum) > 0:
        cossSumNorm = normalizer(cossSum)
        newImg = np.uint8(cossSumNorm)
        newImg = splitChannels(newImg)
    else: newImg = transformaCosseno()
    createPanelBottom(newImg)
    createPanelBottom(transformaInversaCosseno())

def TDCPassaAlta():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        def corteImg():
            global newImg
            clearTopPanels()
            corteVal = float(corte.get())
            if len(cossSum) > 0:
                createPanelTop(newImg)
            else: 
                newImg = transformaCosseno()
                createPanelTop(newImg)
            imgCorte = zeros_like(newImg)
            for i in range(len(newImg)):
                for j in range(len(newImg[0])):
                    if newImg[i, j, 0] > corteVal:
                        imgCorte[i, j] = newImg[i, j]
            createPanelTop(imgCorte)

        corte = StringVar()
        noiseAmmEntry = Entry(frameBottom, textvariable=corte)
        noiseAmmEntry.pack(expand=True)
        panelsBottom.append(noiseAmmEntry)
        btnCorte = Button(frameBottom, text="Confirmar", command=corteImg)
        btnCorte.pack()
        panelsBottom.append(btnCorte)
    
def TDCPassaBaixa():
    global img, newImg, panelsTop
    if type(panelsTop[0]) is not Label:
        return
    if(len(img) > 0):
        clearOtherPanels()
        def corteImg():
            global newImg
            clearTopPanels()
            corteVal = float(corte.get())
            if len(cossSum) > 0:
                createPanelTop(newImg)
            else: 
                newImg = transformaCosseno()
                createPanelTop(newImg)
            imgCorte = zeros_like(newImg)
            for i in range(len(newImg)):
                for j in range(len(newImg[0])):
                    if newImg[i, j, 0] <= corteVal:
                        imgCorte[i, j] = newImg[i, j]
            createPanelTop(imgCorte)

        corte = StringVar()
        noiseAmmEntry = Entry(frameBottom, textvariable=corte)
        noiseAmmEntry.pack(expand=True)
        panelsBottom.append(noiseAmmEntry)
        btnCorte = Button(frameBottom, text="Confirmar", command=corteImg)
        btnCorte.pack()
        panelsBottom.append(btnCorte)


#DEFAULT OPERATIONS

def clearAll():
    if len(panelsTop) > 0:
        clearOtherPanels()
        clearMainPanel()

def select_image():
    global img, panelsTop, newImg, cossSum
    path = filedialog.askopenfilename(title='open')

    if(len(path) > 0):
        clearAll()
        cossSum = []
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
window.minsize(400, 400)

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
functions.add_command(label="HSL e RGB", command=HSLandRGB)
functions.add_command(label="To Gray Scale", command=grayScale)
functions.add_command(label="Invert Colors", command=invertColors)
functions.add_command(label="Split Colors", command=splitRGB)
functions.add_command(label="Insert Canvas Around Image", command=insertCanvas)
menubar.add_cascade(label="Functions 1", menu=functions)
functions2 = Menu(menubar, tearoff=0)
functions2.add_command(label="Inserir ruído", command=insertNoise)
functions2.add_command(label="Compressão de escala dinâmica", command=dynamicCompression)
functions2.add_command(label="Média 3x3", command=average3x3)
functions2.add_command(label="Mediana 3x3", command=median3x3)
functions2.add_command(label="Laplaciano", command=Laplaciano)
functions2.add_command(label="Sobel", command=sobel)
menubar.add_cascade(label="Functions 2", menu=functions2)
functions3 = Menu(menubar, tearoff=0)
filters = Menu(functions2, tearoff=0)
functions3.add_command(label="Equalização de Histograma", command=EQdeHistograma)
filters.add_command(label="Passa-alta", command=LimiarizacaoPassaAlta)
filters.add_command(label="Passa-baixa", command=LimiarizacaoPassaBaixa)
functions3.add_cascade(label="Limiarização", menu=filters)
functions3.add_command(label="Limiarização por OTSU", command=LimiarizacaoOTSU)
functions3.add_command(label="Binarização por OTSU", command=BinarizacaoOTSU)

menubar.add_cascade(label="Functions 3", menu=functions3)
functions4 = Menu(menubar, tearoff=0)
functions4.add_command(label="Mostrar transformada do cosseno", command=transformadaCompleta)
filters = Menu(functions4, tearoff=0)
filters.add_command(label="Passa-alta", command=TDCPassaAlta)
filters.add_command(label="Passa-baixa", command=TDCPassaBaixa)
functions4.add_cascade(label="Filtro na Transformada (TDC com limiar)", menu=filters)
functions3.add_command(label="Zang Suen", command=operacaoZangSuen)
menubar.add_cascade(label="Functions 4", menu=functions4)



frameTop = Frame()
frameTop.pack(side="top")
frameBottom = Frame()
frameBottom.pack(side="top", fill="x", padx=3)

window.config(menu=menubar)
window.mainloop()
