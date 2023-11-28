from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .prolog import prolog


class ActionNombrarProductos(Action):

 	def name(self) -> Text:
 		return "action_nombrar_productos_disponibles"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		consulta = f'producto(Producto, Categoria).'
 		productos = prolog.consultar(consulta)
 		
 		respuesta = ( 
			    "Aca tienes la lista de todos los productos: \n" +
			    "\n".join([prod['Producto'] for prod in productos])
			) if productos else "No hay productos registrados en este momento.\n"

 		dispatcher.utter_message(respuesta)
 		return []

