import os
import zipfile
import rarfile
import tempfile
import fitz
import shutil
import pandas as pd
from django.http import FileResponse

class Manejador:
    def __init__(self, archivo):
        self.archivo = archivo  # Archivo es un objeto 'File' de Django
        self.ruta_archivo = os.path.join(tempfile.mkdtemp(), self.archivo.name)  # Guardar en temp

    def guardar_archivo(self):
        """Guarda el archivo en disco temporalmente."""
        with open(self.ruta_archivo, 'wb') as destino:
            for chunk in self.archivo.chunks():
                destino.write(chunk)

    def extraer_archivo(self):
        """Extrae el archivo en una carpeta temporal y retorna la ruta."""
        destino_temp = tempfile.mkdtemp()

        if self.ruta_archivo.endswith(".zip"):
            with zipfile.ZipFile(self.ruta_archivo, 'r') as zip_ref:
                zip_ref.extractall(destino_temp)
        elif self.ruta_archivo.endswith(".rar"):
            with rarfile.RarFile(self.ruta_archivo, 'r') as rar_ref:
                rar_ref.extractall(destino_temp)
        else:
            return None  # Tipo de archivo no soportado

        return destino_temp

    def extraer_cliente(self, pdf_path):
        """Extrae el nombre del cliente de un PDF."""
        with fitz.open(pdf_path) as pdf:
            for pagina in pdf:
                texto = pagina.get_text("text")
                for linea in texto.split("\n"):
                    if linea.startswith("Cliente: "):
                        return linea.replace("Cliente: ", "").strip()
        return None

    def generar_excel_factura(self, factura_pdf, carpeta_destino):
        """Genera un archivo Excel a partir de la información de una factura en PDF."""
        datos_factura = {"Cliente": None, "Fecha": None, "Número de Factura": None, "Concepto": None, "Total": None}

        # Extraer el texto del PDF
        with fitz.open(factura_pdf) as pdf:
            for pagina in pdf:
                texto = pagina.get_text("text")
                for linea in texto.split("\n"):
                    if linea.startswith("Cliente:"):
                        datos_factura["Cliente"] = linea.replace("Cliente:", "").strip()
                    elif linea.startswith("Fecha:"):
                        datos_factura["Fecha"] = linea.replace("Fecha:", "").strip()
                    elif linea.startswith("Numero de Factura:"):
                        datos_factura["Número de Factura"] = linea.replace("Numero de Factura:", "").strip()
                    elif linea.startswith("Concepto:"):
                        datos_factura["Concepto"] = linea.replace("Concepto:", "").strip()
                    elif linea.startswith("Total:"):
                        datos_factura["Total"] = linea.replace("Total:", "").strip()

        # Crear un DataFrame con los datos de la factura
        df = pd.DataFrame([datos_factura])

        # Ruta donde se guardará el Excel
        num_factura = datos_factura["Número de Factura"]
        excel_path = os.path.join(carpeta_destino, f"{num_factura}.xlsx")

        # Guardar Excel
        df.to_excel(excel_path, index=False)

        return excel_path

    def manejar(self):
        """Gestiona el archivo: extrae, clasifica, genera Excel y empaqueta todo en un ZIP."""
        self.guardar_archivo()
        carpeta_extraida = self.extraer_archivo()

        if carpeta_extraida:
            facturas_por_cliente = {}
            carpeta_temporal = tempfile.mkdtemp()  # Crear carpeta temporal para todo el proceso

            # Recogemos los nombres de los clientes
            for factura in os.listdir(carpeta_extraida):
                factura_path = os.path.join(carpeta_extraida, factura)
                if factura.endswith(".pdf"):
                    cliente = self.extraer_cliente(factura_path)
                    if cliente:
                        if cliente not in facturas_por_cliente:
                            facturas_por_cliente[cliente] = []
                        facturas_por_cliente[cliente].append(factura_path)

            # Mover archivos a su carpeta correspondiente y generar Excel
            for cliente, facturas in facturas_por_cliente.items():
                cliente_dir = os.path.join(carpeta_temporal, cliente)
                os.makedirs(cliente_dir, exist_ok=True)  # Crear carpeta si no existe

                for factura in facturas:
                    destino_factura = os.path.join(cliente_dir, os.path.basename(factura))
                    shutil.move(factura, destino_factura)  # Mover archivo

                    # Generar el Excel con la información del gasto
                    self.generar_excel_factura(destino_factura, cliente_dir)

            # Crear el ZIP final para la descarga
            zip_destino = os.path.join(tempfile.mkdtemp(), "facturas_procesadas.zip")
            with zipfile.ZipFile(zip_destino, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(carpeta_temporal):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), carpeta_temporal))

            # Limpiar archivos temporales
            shutil.rmtree(carpeta_temporal)
            shutil.rmtree(carpeta_extraida)

            return zip_destino  # Devolvemos la ruta del ZIP

    def descargar_facturas(self, request):
        """Función para descargar el ZIP generado."""
        zip_path = self.manejar()
        return FileResponse(open(zip_path, 'rb'), as_attachment=True, filename="facturas_procesadas.zip")
