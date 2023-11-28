from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .prolog import prolog


class ActionDameLaCategoriaDeUnLocal(Action):

 	def name(self) -> Text:
 		return "action_dar_categoria_de_un_local"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		local = tracker.get_slot("local")
 		local = local.lower() if local else None

 		consulta = f'local("{local}", Categoria).'
 		categoria = prolog.consultar(consulta)

 		if not categoria:
 			respuesta = f"No encontré ninguna categoria para {local}. Es probable que como la hayas escrito no sea como este registrado en el sistema"
 			dispatcher.utter_message(respuesta)
 			return []


 		respuesta = f"La categoria para el local {local} es {categoria[0]['Categoria']}\n"
 		dispatcher.utter_message(respuesta)
 		return []