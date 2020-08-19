import sys
import numpy as np
import numpy.ma as ma
import cv2

#INPUT_IMAGE = "Wind Waker GC.bmp"
INPUT_IMAGE = "GT2.BMP"
OUTPUT_NAME = INPUT_IMAGE[:-4]
BRIGHT_THRESHOLD = 0.5

# Qual metodo para gerar a mascara de fontes de luz
# Caso coloque os 2 ira rodar com ambos
BRIGHT_OPTIONS = ["HSL"] # NP_WHERE ou HSV

# Qual metodo para borrar a mascara
# Caso coloque os 2 ira rodar com ambos
BLUR_OPTIONS = ["GAUSSIAN", "BOX_FILTER"] #GAUSSIAN ou BOX_FILTER

NUMBER_BLURS = 5 #Quantas vezes a mascara sera borrada
START_KSIZE = 5 #Tamanho inicial do kernel(deve ser impar), par nao funciona n função do opencv
END_KSIZE = START_KSIZE + (NUMBER_BLURS*2) #ksize deve sempre ser impar

def brightPass(img, option):
    if not isinstance(img, np.ndarray):
        raise Exception("img is not numpy ndarray")
    if option == "NP_WHERE":
        # Mesmo resultado que cv2.threshold(img, BRIGHT_THRESHOLD, 1, cv2.THRESH_TOZERO)
        return np.where(img > BRIGHT_THRESHOLD, img, 0)
    elif option == "HSL":
        imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        mask = cv2.inRange(imgHLS[:,:,1], BRIGHT_THRESHOLD, 1)
        return cv2.bitwise_or(img, img, mask=mask)
    else:
        raise Exception(f"bright option '{option}' is not valid.")

def blur(img, option):
    if not isinstance(img, np.ndarray):
        raise Exception("img is not numpy ndarray")
    blurImg = np.zeros(img.shape)
    
    if option == "GAUSSIAN":
        for i in range(START_KSIZE,END_KSIZE,2): 
            blurImg += cv2.GaussianBlur(img, (i, i), 3)
            print("Vezes")
        return blurImg
    elif option == "BOX_FILTER":
        for i in range(START_KSIZE,END_KSIZE,2):
            blurImg += cv2.boxFilter(img, -1, (i, i))
        return np.where(blurImg > 1, 1, blurImg)
    else:
        raise Exception(f"blur option '{option}' is not valid")

def bloom(img):
    cv2.imshow(OUTPUT_NAME, img)

    brightImages = []    
    for option in BRIGHT_OPTIONS:
        brightImages.append( brightPass(img, option) )
    for idx, bright in enumerate(brightImages):
        cv2.imshow(f"{OUTPUT_NAME} brightPass {idx}" , bright)
   

    blurredImages = []
    for option in BLUR_OPTIONS:
        for bright in brightImages:
            blurredImages.append( blur(bright, option))
    for idx, blurred in enumerate(blurredImages):
        cv2.imshow(f"{OUTPUT_NAME} blurred {idx}" , blurred)
    
    outputImages = []
    for blurredImg in blurredImages:
        out = img + 0.7*blurredImg
        outputImages.append( out )

    for idx, output in enumerate(outputImages):
        cv2.imshow(f"{OUTPUT_NAME} bloom {idx}" , output)

    

def main():
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()
    
    # Converte para float32.
    img = img.astype(np.float32) / 255
    
    bloom(img)
    # O numero de resultados eh dado por: len(BRIGHT_OPTIONS) * len(BLUR_OPTIONS)
    # Os indices que aparecem no titulo das imagens correspondem a posicao na respectiva lista de opcoes

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()