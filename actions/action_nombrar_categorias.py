from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .prolog import prolog

class ActionNombrarCategorias(Action):

 	def name(self) -> Text:
 		return "action_nombrar_categorias"

 	def run(self, dispatcher: CollectingDispatcher,
 		tracker: Tracker,
 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

 		consulta = f'categoria(Categoria).'
 		categorias = prolog.consultar(consulta)

 		respuesta = ( 
			    "Aca tienes la lista de todas las categorias: \n" +
			    "\n".join([resultado['Categoria'] for resultado in categorias])
			) if categorias else "No hay categorias por el momento.\n"

 		dispatcher.utter_message(respuesta)
 		return []




