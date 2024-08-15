# TICKET PROJECT

## Descrição

Este projeto tem como objetivo automatizar o processo de inserção de dados em uma planilha, coletando as informações diretamente a partir de imagens. Utilizando técnicas de visão computacional, o projeto extrai textos das imagens disponibilizadas  e organiza os dados em uma planilha de maneira eficiente e precisa.

## Dependências

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

## Como executar o projeto
```bash
python main.py
```

## Resultado

O resultado deve ser a criação de uma planilha excel nomeada como ``tickets de pesagem.xlsx``

## Contribuindo
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.