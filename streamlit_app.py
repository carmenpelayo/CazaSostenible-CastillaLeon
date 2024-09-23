import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels
from statsmodels.tsa.arima.model import ARIMA
import warnings

st.title("¡Configura tu estrategia de caza en Castilla y León en 30 segundos!")

# ELECCIÓN 1: Ubicación
st.subheader("📍 ¿En qué provincia(s) quieres cazar?")
provincias = ['AVILA', 'BURGOS', 'LEON', 'PALENCIA', 'SALAMANCA', 'SEGOVIA', 'SORIA', 'VALLADOLID', 'ZAMORA']
opcion1 = st.multiselect("", provincias, placeholder="Por favor, elige una o más provincias.")

# ELECCIÓN 2: Animal
st.subheader("🐗 ¿Qué animal(es) quieres cazar?")
animales = ['BECADA', 'CABRA MONTÉS', 'CIERVO', 'CODORNIZ', 'CONEJO', 'CORNEJAS', 'CORZO', 'CÓRVIDOS', 'FAISÁN', 'GAMO', 'JABALÍ', 'LIEBRE', 'LOBO', 'MUFLÓN', 'OTRAS AVES ACUÁTICAS', 'PALOMA BRAVÍA', 'PALOMA TORCAZ', 'PALOMA ZURITA', 'PATO REAL O AZULÓN', 'PERDIZ ROJA', 'REBECO', 'TÓRTOLA', 'URRACAS,GRAJILLAS', 'VENADO', 'ZORRO', 'ZORZAL', 'ZORZALES', 'ÁNADE REAL O AZULÓN']
opcion2 = st.multiselect("", animales, placeholder="Por favor, elige uno o más animales.")

# RECOMENDACIÓN
result = st.button('¡Recomiéndame!')

# Apagar warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

# Importar datos
caza = pd.read_csv("resultados-temporadas-cinegeticas.csv", sep=";")

# Predicción
def predecir_caza(provincias, animales):
  resultados = []
  for provincia in provincias:
    for animal in animales:
      # Time series preparation
      animal_provincia = caza[(caza.Provincia == provincia) & (caza.ESPECIE == animal)]
      capturas = animal_provincia['capturas']
      capturas = capturas.fillna(0)
      nonzero_counts = (capturas > 0).sum() 
      zero_counts = (capturas == 0).sum()
      if nonzero_counts <= 10 or  zero_counts >= 10: # Check if there are less than 10 non-zero records in the series
          print(f"Información insuficiente para predecir la caza de {animal} en {provincia}.")
          continue  # Skip to the next iteration
      # Modeling
      arima = ARIMA(capturas, order=(2,0,2))
      results = arima.fit()
      forecast = results.get_forecast(steps=1)
      prediction = forecast.predicted_mean.values[0]
      conf_int = forecast.conf_int()
      lower_bound = max(0,conf_int.iloc[0, 0])
      upper_bound = conf_int.iloc[0, 1]
      # Results
      resultados.append({
                "Provincia": provincia,
                "Animal": animal,
                "Previsión de caza mínima": lower_bound,
                "Previsión de caza media": prediction,
                "Previsión de caza máxima": upper_bound
            })
      
      # Visualization
      fig, ax = plt.subplots(figsize=(12, 8))
      ax.plot(animal_provincia.TEMPORADA, capturas, label='Histórico', marker='o', linestyle='-', color='b', markersize=8)
      temporadas_ext = list(animal_provincia.TEMPORADA) + ['2023-2024']
      capturas_ext = list(capturas) + [prediction]
      ax.plot(temporadas_ext[-2:], capturas_ext[-2:], label='Previsión', linestyle='--', color='r', linewidth=2, marker='o', markersize=10)
      ax.fill_between(temporadas_ext[-2:], lower_bound, upper_bound, color='grey', alpha=0.3, label='Intervalo de Confianza 95%')
      ax.annotate(int(prediction), xy=('2023-2024', prediction), xytext=(10, 10), textcoords='offset points', fontsize=12, color='red')
      ax.set_title(f'Previsión de caza de {animal} en {provincia} para la temporada 2023-2024 (confianza del 95%)', fontsize=16)
      ax.set_xlabel('Temporada', fontsize=14)
      ax.set_ylabel('Capturas', fontsize=14)
      ax.legend(loc='upper left', fontsize=12)
      ax.tick_params(axis='x', rotation=45, labelsize=12)
      ax.tick_params(axis='y', labelsize=12)
      plt.tight_layout()
      plt.grid(True)
      st.pyplot(fig) 

    resultados = pd.DataFrame(resultados)
    resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]] = resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]].astype(int)   
    
    # Image
    image_path = "images/" + animal + ".jpg"
    st.image(image_path)
    
    return resultados

# RESULTADOS
if result:
  if not opcion1 or not opcion2:
        st.warning("Es obligatorio seleccionar al menos una provincia y un animal.")
  else:
    st.balloons()
    st.markdown("""---""")
    st.subheader("🏆 ¡Tus resultados!")
    match = predecir_caza(opcion1, opcion2)
    st.table(match)
    st.write("*Si no ves las previsiones de alguna de las búsquedas en la tabla, significa que no existen datos suficientes para predecir la caza de la temporada 2023-2024.*")
