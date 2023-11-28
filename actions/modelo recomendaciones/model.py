import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('dataset.csv')

label_encoder_local = LabelEncoder()
label_encoder_producto = LabelEncoder()

df['Local'] = label_encoder_local.fit_transform(df['Local'])
df['Producto'] = label_encoder_producto.fit_transform(df['Producto'])

X = df[['Local', 'Producto']].values
Y = df['Valoración'].values

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


model = keras.Sequential([
    keras.layers.Input(shape=(X_train.shape[1],)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, Y_train, epochs=5, batch_size=64, validation_data=(X_test, Y_test))

loss, accuracy = model.evaluate(X_test, Y_test)
print(f'Loss: {loss}, Accuracy: {accuracy}')

path = "C:\\Users\\Martin\\Documents\\Desktop\\ShoppingBot\\actions\\modelo recomendaciones"
model.save(f'{path}\\model.h5')
joblib.dump(label_encoder_local, f'{path}\\label_encoder_local.pkl')
joblib.dump(label_encoder_producto, f'{path}\\label_encoder_producto.pkl')

producto = 'bolso'
local = 'markova'

producto_encoded = label_encoder_producto.transform([producto])
local_encoded = label_encoder_local.transform([local])

sample = np.array([[local_encoded[0], producto_encoded[0]]])
prediction = model.predict(sample)
print('Prediction:', prediction[0])