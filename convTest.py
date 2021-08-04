from PIL.Image import fromarray
import numpy as np
import cv2
import PIL

def normalizer(matriz):
    return np.around(matriz / matriz.max()) * 255

def sameSize(matriz):
    if matriz.shape[0] > matriz.shape[1]:
        sizeDiff = round((matriz.shape[0] - matriz.shape[1])/2)
        return matriz[sizeDiff: matriz.shape[0]-sizeDiff, :]
    sizeDiff = round((matriz.shape[1] - matriz.shape[0])/2)
    return matriz[:, sizeDiff: matriz.shape[1]-sizeDiff]

def convolucao(matrizMascara, matrizImagem, multiplier):
    
    if(matrizImagem.shape[0] != matrizImagem.shape[1]):
        matrizImagem = sameSize(matrizImagem)
    lenImg = len(matrizImagem)
    lenMasc = len(matrizMascara)
    newMatrixLenght =  (1 - lenMasc) + lenImg
    newMatrix = np.zeros((newMatrixLenght, newMatrixLenght))
    for i in range(newMatrixLenght):
        for j in range(newMatrixLenght):
            convSum = 0
            for k in range(lenMasc):
                for l in range(lenMasc):
                    convSum += (matrizImagem[i+k][j+l] * matrizMascara[k, l])
                    ()
            newMatrix[i][j] = round(multiplier * convSum)
    print(i, j, k, l)
    return newMatrix#imagemConv

imgMatrix = cv2.imread("C:\\Users\\ranoc\\OneDrive\\Documentos\\GitHub\\Processamento-Digital-de-Imagens\\first-step\\photos\\profilePic.png")
imgMatrix = cv2.cvtColor(imgMatrix ,cv2.COLOR_RGB2GRAY)

filterMatrix = np.array([[1,1,1],
                        [1,1,1],
                        [1,1,1]])

    
#print(convolucao(filterMatrix, imgMatrix, 1/9).shape)
 

newImage = convolucao(filterMatrix, imgMatrix, 1/9)
print(newImage)
cv2.imwrite("new.bmp", newImage)
#cv2.imshow("new.bmp")