from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .controlador_csv import csv_controlador


class ActionGuardarContacto(Action):

 	def name(self) -> Text:
 		return "action_guardar_contacto"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:




 		contacto_id = tracker.current_state()['sender_id']
 		print('Contacto id: ' + contacto_id)

 		nombre = tracker.get_slot("nombre")
 		edad = tracker.get_slot("edad")
 		genero = tracker.get_slot("genero")
 		es_cliente_habitual = tracker.get_slot("es_cliente_habitual")
 		categorias_de_interes = [cat.lower() for cat in tracker.get_slot("categorias_de_interes")]
 		#productos_de_interes = tracker.get_slot("productos_de_interes")

 		print(contacto_id, nombre, edad, genero, es_cliente_habitual, categorias_de_interes)

 		if not nombre:
 			return []

 		datos = csv_controlador.leer_csv()
 		for fila in datos:
 			contacto_id_fil = fila[0]
 			if (contacto_id_fil == contacto_id):
 				return []

 		datos.append([contacto_id, nombre, edad, genero, es_cliente_habitual, categorias_de_interes])
 		csv_controlador.escribir_csv(datos)
 		#dispatcher.utter_message(f"Bueno {nombre}, te voy a hacer unas preguntas para conocer más sobre tu perfil 😇")
 		return [SlotSet("es_conocido", True)]