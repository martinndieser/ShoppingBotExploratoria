from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .prolog import prolog



class ActionNombrarProductosEnCategoria(Action):

 	def name(self) -> Text:
 		return "action_dar_productos_en_categoria"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 	 	categoria = tracker.get_slot("categoria")
 	 	if not categoria:
 	 		respuesta = "No pude identificar a lo que te estas refiriendo, ¿Puedes decirlo de otra manera?"
 	 		dispatcher.utter_message(respuesta)
 	 		return []
 	 	categoria = categoria.lower()
 	 	consulta = f'producto(Producto, "{categoria}").'
 	 	productos = prolog.consultar(consulta)

 	 	respuesta = ( 
			    f"Aca tienes la lista de todos los productos para la categoria {categoria}: \n" +
			    "\n".join([prod['Producto'] for prod in productos])
			) if productos else f"No hay productos registrados en este momento en la categoria {categoria}.\n"

 	 	dispatcher.utter_message(respuesta)
 	 	return []
