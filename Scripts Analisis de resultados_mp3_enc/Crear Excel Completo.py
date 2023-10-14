import openpyxl

# Crear un nuevo archivo de Excel
workbook = openpyxl.Workbook()
sheet = workbook.active

# Abrir el archivo de texto
with open('new3.txt', 'r') as file:
    for line in file:
        # Dividir la línea en partes usando el punto como separador
        parts = line.strip().split('/')

        # Agregar cada parte como una celda en la hoja de Excel
        sheet.append(parts)

# Guardar el archivo de Excel
workbook.save('archivo_excel.xlsx')

print("Archivo de Excel creado con éxito.")
