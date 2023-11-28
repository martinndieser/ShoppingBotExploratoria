import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import graphviz
import joblib

df = pd.read_csv('dataset.csv', sep=',')
df = df.drop(columns=['id'])

# mostrar más columnas en panda
pd.set_option('display.max_columns', 30)
# aplica el hot-encoding
df = pd.get_dummies(data=df)

x = df.drop(columns='recomendar') # feature
y = df['recomendar'] # target
# Creamos el árbol y limitamos su profundidad
model = DecisionTreeClassifier(max_depth=9)

# Entrenamos el árbol
model.fit(x, y)

# medimos la precisión del árbol
print(model.score(x, y))

# guardamos una imagen del árbol
dot_data = tree.export_graphviz(
	model,
	feature_names=x.columns.tolist(),
	out_file=None,
	class_names=df['recomendar'].astype(str).unique().tolist(),
	filled=True, rounded=True,
	special_characters=True)


graph = graphviz.Source(dot_data)
graph.render("ArbolPreview")

path = "C:\\Users\\Martin\\Documents\\Desktop\\ShoppingBot\\actions\\arbol de desicion"

# guardamos el dump del modelo para luego usarlo en las actions
joblib.dump(model, "arbol.pkl") 