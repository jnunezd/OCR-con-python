# Para que el programa funcione deben estar instalados los binarios de tesseract y plopper => (El cual debe ser agregado al PATH)
# !Importante recordar cambiar las rutas si se cambia el lugar de ejecución
# Archivos necesarios (aparte de las librerias instaladas):
# Indicar la ruta del tesseract en la linea 63
"""
    raiz/
        ./img/
        ./pdf/
            .archivo.pdf
        ./txt/
        ./packages/
            .__init__.py
            .tiempo.py
        .main.py
"""
# Imports
# Para convertir a img y ocr
from pdf2image import convert_from_path
import pytesseract
import cv2

# Sistema y manejo de archivos
import os, shutil
from os import system
from packages import tiempo as cron


###################################
############ Funciones ############
###################################

# Función para limpiar texto  
def str_fix(cadena):
    tabla = {
        "\n":" ",
        "\t":" ", 
        "\r":" ", 
        "\r\n":" ", 
        10:" ",
        13:" ",
        chr(9):" ", 
        chr(10):" ", 
        chr(13):" "
    }
    
    tr = cadena.translate(tabla)
    return str(tr)



###################################
############## Rutas ##############
###################################

# Ruta a tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cwd = os.getcwd()

# Rutas PDF, imagenes y txt
pdf_dir = cwd + "\\pdf"
img_dir = cwd + "\\img\\"
txt_dir = cwd + "\\txt\\"

out_txt = "OCR.txt"


###################################
############## Main ###############
###################################

system('cls')
tomar_tiempo = cron.Cronometro()
with open(txt_dir + out_txt, 'w') as txt:

    # Recorremos cada archivo dentro de la carpeta de PDFs
    for pdf_file in os.listdir(pdf_dir):
        try:
            # Verificamos que el archivo tenga la extension .pdf
            if pdf_file.endswith(".pdf"):

                # Extraccion del nombre del archivo sin la extension
                spl = pdf_file.split('.')
                new_name = spl[0]
                print(f'Leyendo: {pdf_file}' + '\n') 

                # Creacion de ruta al archivo
                in_file = (pdf_dir + '\\' + pdf_file)

                # convert_from_path convierte el pdf a imagen (una por página) y retorna la lista de imagenes # imagen sin ningun tipo de formato la cual hay que guardar con alguna extension para aplicar ocr
                pages = convert_from_path(in_file, 550)

                texto = ""                  # Inicialisamos el texto en vacio por cada documento
                n_paginas = len(pages)      # Numero de paginas en el documento

                for i, page in enumerate(pages, start=1):

                    # Damos el nombre a la imagen de salida
                    img_name = "archivo_%s_pagina_%d_de_%d.JPEG" %(new_name, i, n_paginas)

                    # Establecemos la ruta del archivo a salir
                    out_file = img_dir+img_name
                    print(img_name)

                    page.save(out_file, 'JPEG')     # Guardamos la imagen

                    # Leemos la imagen con cv2 y aplicamos ocr
                    img = cv2.imread(out_file)
                    ocr = pytesseract.image_to_string(img, lang="spa") # recibe una imagen y el lenguaje para retornar un string

                    ocr = str_fix(ocr)      # Limpiamos los saltos de linea del demas del texto devuelto en ocr
                    texto = f"{texto} {ocr}"

                # Grabamos en archivo de salida
                txt.write("%s|%s\n"%(new_name, texto))



            # Eliminamos las imagenes generadas recorriendo cada archivo en la carpeta de imagenes
            for filename in os.listdir(img_dir):
                file_path = os.path.join(img_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

        except Exception as e:
            print(f'Fallo al leer: {pdf_file}. Error: {e}')

tomar_tiempo.tiempo()
    
