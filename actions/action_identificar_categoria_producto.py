from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .prolog import prolog

class ActionIdentificarCategoriaDeProducto(Action):

	def name(self) -> Text:
		return "action_identificar_categoria_producto"

	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		producto = tracker.get_slot("producto")
		producto = producto.lower() if producto else None
		
		consulta = f'producto("{producto}", Categoria).'
		categoria = prolog.consultar(consulta)
		
		# no esta implementado todavia
		# el caso para aquellos productos que pueden
		# ocupar varias categorias

		if not categoria:
			consulta = f'producto(Producto, Categoria).'
			productos_disponibles = prolog.consultar(consulta)
			productos_disponibles_str = "\n".join([f" - {producto['Producto']}" for producto in productos_disponibles])

			respuesta = "No pude identificar el producto al que te estas refiriendo."\
						"Actualmente solo puedo proporcionarte la información acerca de los siguientes productos: \n"\
						+ productos_disponibles_str
			dispatcher.utter_message(respuesta)
			return []

		respuesta = f"Todo lo relacionado con el producto {producto} lo podes encontrar en cualquier local de la categoria {categoria[0]['Categoria']}\n"

		#respuesta += f"¿Quieres que te recomiende un locales donde puedes conseguir {producto}?"
		dispatcher.utter_message(respuesta)
		return [SlotSet("categoria", categoria)]