import csv

class ControladorCSV:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def leer_csv(self):
    	data = []
    	with open(self.nombre_archivo, 'r', newline='') as csvfile:
    		csvreader = csv.reader(csvfile)
    		for fila in csvreader:
    			data.append(fila)
    	return data

    def escribir_csv(self, data):
        with open(self.nombre_archivo, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for fila in data:
                csvwriter.writerow(fila)



PATH_CSV = r'C:\\Users\\Martin\\Documents\\Desktop\\ShoppingBot\\bd\\datos.csv'

# importante que se le pase un string con el prefijo r de raw
csv_controlador = ControladorCSV(PATH_CSV)


