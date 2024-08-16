# TICKET PROJECT
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Tesseract](https://img.shields.io/badge/TESSERACT-red?style=for-the-badge&logo=opencv)

## Descrição

Este projeto tem como objetivo automatizar o processo de inserção de dados em uma planilha, coletando as informações diretamente a partir de imagens. Utilizando técnicas de visão computacional, o projeto extrai textos das imagens disponibilizadas na pasta ``anexos`` e organiza os dados em uma planilha de maneira eficiente e precisa.

## Requerimentos

Para executar este projeto, as seguintes bibliotecas Python são necessárias:

- `glob`: Para manipulação de padrões de nomes de arquivos.
- `PIL (Pillow)`: Para processamento de imagens.
- `pandas`: Para manipulação de dados e planilhas.
- `pytesseract`: Para reconhecimento óptico de caracteres (OCR).
- `numpy`: Para operações matemáticas e manipulação de arrays.
- `timeit`: Para medir o tempo de execução de pequenos trechos de código.
- `cv2 (OpenCV)`: Para processamento de imagens.
- `re`: Para operações com expressões regulares.

Você pode instalar todas as dependências executando:

```
pip install -r requirements.txt
```

### Instalação do Tesseract

1. Baixe o instalador do Tesseract [aqui](https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe)

2. Siga as seguintes instruções de instalação.
    
    - clique em `ok`
    - clique em `next`
    - clique em `I Agree`.
    - Fica a sua escolha se quer instalar apenas para seu usuário ou todos os seus usuários do computador.
    - Abra o nó `Additional language data (download)` e procure pela opção `Portuguese` e marque ela.

    ![Choose Components](doc\passo5.png)
    ![Choose Components portuguese](doc\passo6.png)

    <a name="path_tesseract"></a>
    - Copie o caminho que aparece na tela e clique em `next`

    ![Chosse install Location](doc\passo7.png)

    - clique em `Install`
    - espere o download e clique em `next`
    - clique em `finish`


3. Adicione o diretório de instalação do Tesseract ao `PATH` do sistema.
    -  pesquise por `variaveis de ambiente` no seu computador.
    
    ![variaveis_de_ambiente](doc\variaveis_de_ambiente.png)

    - Nas variáveis de usuario adicione ao PATH o caminho do tesseract.exe que está na presente na pasta que você [copiou o caminho](#path_tesseract).


## Como executar o projeto
```bash
python main.py
```

## Resultado

O resultado deve ser a criação de uma planilha excel nomeada como ``tickets de pesagem.xlsx``

## Contribuindo
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.