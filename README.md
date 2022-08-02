# OCR-con-python
Lee pdf que pueden tener texto como imagen y genera un archivo de texto
Para que el programa funcione deben estar instalados los binarios de tesseract y plopper => (El cual debe ser agregado al PATH)
Importante recordar cambiar las rutas si se cambia el lugar de ejecución
Archivos necesarios (aparte de las librerias instaladas):
Indicar la ruta del tesseract en la linea 63

```
    raiz/
        ./img/
        ./pdf/
            .archivo.pdf
        ./txt/
        ./packages/
            .__init__.py
            .tiempo.py
        .main.py
```
