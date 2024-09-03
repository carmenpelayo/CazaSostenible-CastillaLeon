import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels
from statsmodels.tsa.arima.model import ARIMA
import warnings

st.title("🔍 Tu estrategia de caza")
st.write("""¡Encuentra la mejor forma de cazar en Castilla y León!""")
st.markdown("""---""")

# ELECCIÓN 1: Ubicación
st.subheader("📍 ¿En qué provincia(s) quieres cazar?")
provincias = ['BURGOS','SEGOVIA','SORIA','AVILA','LEON','VALLADOLID','PALENCIA','ZAMORA','SALAMANCA']
opcion1 = st.multiselect("", provincias)

# ELECCIÓN 2: Animal
st.subheader("🐗 ¿Qué animal(es) quieres cazar?")
animales = ['JABALÍ', 'LOBO', 'CORZO', 'VENADO', 'REBECO', 'CABRA MONTÉS', 'MUFLÓN', 'GAMO', 'CONEJO', 'LIEBRE', 'ZORRO', 'PALOMA ZURITA', 'PALOMA BRAVÍA', 'PALOMA TORCAZ', 'TÓRTOLA', 'CODORNIZ', 'BECADA', 'URRACAS,GRAJILLAS', 'PATO REAL O AZULÓN', 'OTRAS AVES ACUÁTICAS', 'ZORZAL', 'PERDIZ ROJA', 'FAISÁN', 'CORNEJAS', 'CÓRVIDOS', 'CIERVO', 'ÁNADE REAL O AZULÓN', 'ZORZALES']
opcion2 = st.multiselect("", animales)

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
      lower_bound = conf_int.iloc[0, 0]
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
      plt.figure(figsize=(10, 6))
      plt.plot(animal_provincia.TEMPORADA, capturas, label='Histórico', marker='o', linestyle='-', color='b')
      temporadas_ext = list(animal_provincia.TEMPORADA) + ['2023-2024']
      capturas_ext = list(capturas) + [prediction]
      plt.plot(temporadas_ext[-2:], capturas_ext[-2:], label='Previsión', linestyle='-', color='r')
      plt.fill_between(temporadas_ext[-2:], lower_bound, upper_bound, color='grey', alpha=0.3)
      plt.title(f'Previsión de caza de {animal} en {provincia} para la temporada 2023-2024 (confianza del 95%).')
      plt.xlabel('Temporada')
      plt.ylabel('Capturas')
      plt.legend(loc='upper left')
      plt.xticks(rotation=45)
      plt.tight_layout()
      plt.grid(True)
      plt.show()
  
  resultados = pd.DataFrame(resultados)
  resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]] = resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]].astype(int)   
  return resultados

# RESULTADOS
if result:
    match = predecir_caza(opcion1, opcion2)
    st.balloons()
    st.markdown("""---""")
    st.subheader("🏆 ¡Tus resultados!")
    st.write("Según tus preferencias, te recomendamos que caces en la temporada 2023-2024 en...")
    st.table(match.head(10))
