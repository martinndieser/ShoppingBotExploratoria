from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .controlador_csv import csv_controlador



class ActionSaludar(Action):

 	def name(self) -> Text:
 		return "action_saludar"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		cliente_id = tracker.current_state()['sender_id']
 		datos = csv_controlador.leer_csv()

 		for fila in datos:
 			contacto_id_fil = fila[0]
 			print(fila, cliente_id)
 			if (contacto_id_fil == cliente_id):
 				nombre = fila[1]
 				edad = fila[2]
 				genero = fila[3]
 				es_cliente_habitual = eval(fila[4])
 				categorias_de_interes = eval(fila[5])

 				dispatcher.utter_message(f"Bueno {nombre}, en que te puedo ayudar? 😇")
 				return [
 						SlotSet("nombre", nombre),
 						SlotSet("es_conocido", True),
 						SlotSet("edad", edad),
 						SlotSet("genero", genero),
 						SlotSet("es_cliente_habitual", es_cliente_habitual),
 						SlotSet("categorias_de_interes", categorias_de_interes),
 				]
 		dispatcher.utter_message("Hola! Me podrias decir cómo te llamas?")
 		return []


