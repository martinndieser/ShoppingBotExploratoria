from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .prolog import prolog



class ActionDarProductosDeLocal(Action):

 	def name(self) -> Text:
 		return "action_dar_productos_de_local"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		local = tracker.get_slot("local")
 		local = local.lower() if local else None
 		consulta = f'local("{local}", Categoria).'
 		categoria = prolog.consultar(consulta)
 		if not categoria:
 			dispatcher.utter_message("No encontré ninguna categoria para el local que me proporcionaste")
 			return []

 		categoria = categoria[0]['Categoria']
 		productos = prolog.consultar(f'producto(Producto, "{categoria}")')
 		respuesta = f"Los productos que se pueden comprar en el local {local} son: \n" + \
           "\n".join([f"- {prod['Producto']}" for prod in productos]) + \
           f"\n También te puedo ayudar si necesitas algún otro dato de contacto de {local}" if productos else \
           f"El local {local} actualmente no tiene nada a la venta"


 		dispatcher.utter_message(respuesta)
 		return []