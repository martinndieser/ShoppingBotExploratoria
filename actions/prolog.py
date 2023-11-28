from swiplserver import PrologMQI

class ControladorProlog:

	def __init__(self, ruta_archivo_pl):
		# importante que se le pase un string con el prefijo r de raw
		# sino va a dar errores cuando prolog busque el archivo
		self.consulta_ruta = r"consult('{}').".format(ruta_archivo_pl)

	def consultar(self, consulta):
		response = None
		with PrologMQI(port=8000) as mqi:
			with mqi.create_thread() as prolog_thread:
				prolog_thread.query(self.consulta_ruta)
				try:
					response = prolog_thread.query(consulta)
				except Exception as e:
					print(e)
		return response


PATH_PROLOG_DATOS = r"C:\\Users\\Martin\\Documents\\Desktop\\ShoppingBot\\prolog\\base.pl"

prolog = ControladorProlog(PATH_PROLOG_DATOS)
