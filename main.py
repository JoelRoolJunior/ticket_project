from glob import glob
from PIL import Image
import pandas as pd
import pytesseract
import numpy as np
import timeit
import cv2
import re
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def thresh_otsu(imagem_cinza):
    _,thresh = cv2.threshold(imagem_cinza, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

def get_ticket_number(imagem_cinza):
    thresh = thresh_otsu(imagem_cinza)
    config = '-c tessedit_char_whitelist=0123456789 --psm 6 --oem 3'
    numero_ticket = str(pytesseract.image_to_string(255 - thresh[20:,:], lang='por',config=config)).strip()
    return numero_ticket

def get_placa_carreta(imagem_cinza):
    thresh = thresh_otsu(imagem_cinza)
    config = '--psm 6 --oem 3'
    placa = str(pytesseract.image_to_string(255 - thresh[20:,:], lang='por',config=config)).strip()
    return placa

def get_transportadora(imagem_cinza):
    thresh = thresh_otsu(imagem_cinza)
    config = '--psm 6 --oem 3'
    saida = str(pytesseract.image_to_string(255 - thresh, lang='por',config=config)).strip()
    transportadora = saida.split('\n',1)[1].split('-')[1]
    return transportadora

def get_notas_fiscais(imagem_cinza):
    thresh = thresh_otsu(imagem_cinza)
    blacklist = r'][~/\. '
    config = f'-c tessedit_char_blacklist={blacklist} --psm 6 --oem 3'
    saida = str(pytesseract.image_to_string(255 - thresh, lang='por',config=config)).strip()
    notas_fiscais = saida.split('\n',1)[1]
    return notas_fiscais

def get_emissor(imagem_cinza):
    thresh = thresh_otsu(imagem_cinza)
    config = r'-c tessedit_char_blacklist=~/\[]  --psm 6  --oem 3'
    saida = str(pytesseract.image_to_string(255 - thresh, lang='por',config=config)).strip()
    emissor = saida.split('-')[1]
    return emissor

def get_material(imagem_cinza):
    thresh = thresh_otsu(imagem_cinza)
    config = '-c tessedit_char_whitelist=-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz --psm 6 --oem 3'
    saida = str(pytesseract.image_to_string(255 - thresh, lang='por',config=config))
    
    if 'caixa' in saida.lower():    material = 'CAIXA DE PAPELÃO'
    elif 'chapa' in saida.lower():  material = 'CHAPA DE PAPELÃO'
    elif 'bobina' in saida.lower(): material = 'BOBINA'
    else:                           material = 'sinalizar'

    return material

def get_info_pesagem(imagem_cinza):
    thresh = thresh_otsu(imagem_cinza)
    config = '-c tessedit_char_whitelist=/:0123456789 --psm 6 --oem 3'
    texto = str(pytesseract.image_to_string(255 - thresh, lang='por',config=config))
    
    try:
        padrao = re.compile(r"(\d{2}/\d{2}/\d{4})(\d{2}:\d{2}:\d{2})\n: (\d+)")
        match = padrao.search(texto)
        data, hora, peso = match.groups()
        saida = f"{data} {hora} {peso}"
    except:
        if len(texto) > 10:
            saida = 'sinalizar'
            return saida
        
        return ''
    else:
        return peso


def main():
    
    paths = glob('anexos\*.jpg')
    recortes = []
    for i,path in enumerate(paths):
        print(f'Recortes da imagem {path[-9:-1]}')
        imagem = cv2.imread(path)
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        imagem_binarizada = cv2.adaptiveThreshold(imagem_cinza,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        mser = cv2.MSER().create(min_area=400,max_area=5000)
        _, rects = mser.detectRegions(imagem_binarizada)


        #Ordenação dos recortes dando prioridade de cima para baixo 
        dtypes = ([('x',int),('y',int),('w',int),('h',int)])
        values = list(map(tuple,rects))
        rects = np.array(values,dtype=dtypes)
        rects = np.sort(rects,order=['y','x','w','h'])
        
        # Faz os Recortes das imagens
        for j, rect in enumerate(rects):
            x,y,w,h = rect
            if ((x in range(0,900)) and (y in range(0,240))) or (y in range(830,imagem.shape[0])):
                pass
            else:
                recortes.append(imagem_cinza[y:y+h,x:x+w])
    
    # leitura das Imagens Usando o pytesseract
    mapa = {
        0: get_ticket_number,
        2: get_placa_carreta,
        4: get_transportadora,
        5: get_notas_fiscais,
        6: get_emissor,
        8: get_material,
        9: get_info_pesagem,
        10: get_info_pesagem  # Mesma função para dois índices
    }

    colunas = [0,2,4,5,6,8,9,10]
    data = []
    campos = []
    for i,recorte in enumerate(recortes):
        print(f'Recorte de numero {i}')
        chave_funcao = i%15
        if chave_funcao in colunas: 
            campos.append(mapa[chave_funcao](recorte))
            if chave_funcao == 10:
                data.append(campos)
                campos = []

    # Criação e Edição do DataFrame
    print('criando um DataFrame')
    df = pd.DataFrame(data)
    df[6] = pd.to_numeric(df[6], errors='coerce')
    df[7] = pd.to_numeric(df[7], errors='coerce')
    df[8] = df[6] - df[7]
    
    df[8] = pd.to_numeric(df[6], errors='coerce') - pd.to_numeric(df[7], errors='coerce')
    is_negative = df[8]<0
    df.loc[is_negative, 8] = df.loc[is_negative, 8] * (-1)
    df[9] = ''
    df[10] = ''

    # Renomeação das colunas
    print('Editando o DataFrame')
    dict_rename = {
        0:'TICKET',
        1:'PLACA',
        2:'TRANSPORTADORA',
        3:'NOTA FISCAL',
        4:'EMISSOR',
        5:'MATERIAL',
        6:'PESO FINAL',
        7:'PESO INICIAL',
        8:'PESO LIQUIDO',
        9:'PESO PALETE',
        10:'NF'
    }
    df = df.rename(columns=dict_rename)
    
    # Troca de posição das colunas
    df = df[['TICKET',
            'PESO INICIAL',
            'PESO FINAL',
            'PESO LIQUIDO',
            'PESO PALETE',
            'NF',
            'EMISSOR',
            'TRANSPORTADORA',
            'PLACA',
            'MATERIAL',
            'NOTA FISCAL'
            ]]
    print('DataFrame processado e convertido em planilha.xlsx')
    df.to_excel('tickets de pesagem.xlsx',index=False)

if __name__ == "__main__":
    init = timeit.default_timer()
    main()
    final = timeit.default_timer()
    print(f'runtime: {final-init}')
