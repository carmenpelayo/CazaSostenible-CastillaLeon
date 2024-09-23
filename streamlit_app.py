import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Define las secciones de la app
secciones = ["Inicio", "Consejos de Caza Sostenible"]

# Selecciona la sección con un selectbox en el sidebar o en la parte superior
seleccion = st.sidebar.selectbox("Selecciona una sección.", secciones)

# Periodos de caza
periodos_caza = {
'BECADA': '22 de octubre al 28 de enero',
'CABRA MONTÉS': '15 de septiembre al 15 de diciembre; 1 de marzo al 30 de junio',
'CIERVO': '1 de septiembre al 4º sábado de septiembre (rececho); 4º domingo de septiembre al 4º domingo de febrero',
'CODORNIZ': '15 de agosto al 3º domingo de septiembre',
'CONEJO': '15 de agosto al 3º domingo de septiembre',
'CORNEJAS Y CÓRVIDOS': '15 de agosto al 3º domingo de septiembre',
'FAISÁN': '22 de octubre al 28 de enero',
'GAMO': '4º domingo de septiembre al 4º domingo de febrero',
'JABALÍ': '1 de abril al 1er domingo de agosto (rececho); 4º domingo de septiembre al 4º domingo de febrero',
'LIEBRE': '22 de octubre al 28 de enero',
'LOBO': 'Según el plan cinegético aprobado',
'MUFLÓN': '4º domingo de septiembre al 4º domingo de febrero',
'AVES ACUÁTICAS': '22 de octubre al 28 de enero',
'PALOMA BRAVÍA': '25 de agosto al 3º domingo de septiembre',
'PALOMA TORCAZ': '1 de octubre al 2º domingo de febrero',
'PALOMA ZURITA': '1 de octubre al 2º domingo de febrero',
'PATO REAL': '22 de octubre al 28 de enero',
'PERDIZ ROJA': '22 de octubre al 28 de enero',
'REBECO': '1 de septiembre al 15 de noviembre; 1 de mayo al 15 de julio',
'TÓRTOLA': 'Caza prohibida',
'URRACAS Y GRAJILLAS': '15 de agosto al 3º domingo de septiembre',
'VENADO': '1 de septiembre al 4º sábado de septiembre (rececho); 4º domingo de septiembre al 4º domingo de febrero',
'ZORRO': 'Durante la temporada general y media veda',
'ZORZALES': '1 de octubre al 2º domingo de febrero',
}
periodos = pd.DataFrame.from_dict(periodos_caza, orient='index', columns=['Período de caza legal'])

# Sección de Caza Responsable
if seleccion == "Inicio":
  st.title("¡Configura tu estrategia de caza sostenible en Castilla y León en 30 segundos!")
  
  # ELECCIÓN 1: Ubicación
  st.subheader("📍 ¿En qué provincia(s) quieres cazar?")
  provincias = ['AVILA', 'BURGOS', 'LEON', 'PALENCIA', 'SALAMANCA', 'SEGOVIA', 'SORIA', 'VALLADOLID', 'ZAMORA']
  opcion1 = st.multiselect("", provincias, placeholder="Por favor, elige una o más provincias.")
  
  # ELECCIÓN 2: Animal
  st.subheader("🐗 ¿Qué animal(es) quieres cazar?")
  animales = ['BECADA', 'CABRA MONTÉS', 'CIERVO', 'CODORNIZ', 'CONEJO', 'CORNEJAS', 'CORZO', 'CÓRVIDOS', 'FAISÁN', 'GAMO', 'JABALÍ', 'LIEBRE', 'LOBO', 'MUFLÓN', 'OTRAS AVES ACUÁTICAS', 'PALOMA BRAVÍA', 'PALOMA TORCAZ', 'PALOMA ZURITA', 'PATO REAL O AZULÓN', 'PERDIZ ROJA', 'REBECO', 'TÓRTOLA', 'URRACAS,GRAJILLAS', 'VENADO', 'ZORRO', 'ZORZAL', 'ÁNADE REAL O AZULÓN']
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
    for animal in animales:
      # Animal image
      st.subheader(animal)
      if animal == "CABRA MONTÉS":
        image_path = "images/CABRA_MONTES.jpg"
      elif animal == "CÓRVIDOS":
        image_path = "images/CORVIDOS.jpg"
      elif animal == "FAISÁN":
        image_path = "images/FAISAN.jpg"
      elif animal == "JABALÍ":
        image_path = "images/JABALI.jpg"
      elif animal == "MUFLÓN":
        image_path = "images/MUFLON.jpg"
      elif animal == "OTRAS AVES ACUÁTICAS":
        image_path = "images/OTRAS_AVES_ACUATICAS.jpg"
      elif animal == "PALOMA BRAVÍA":
        image_path = "images/PALOMA_BRAVIA.jpg"
      elif animal == "PALOMA TORCAZ":
        image_path = "images/PALOMA_TORCAZ.jpg"
      elif animal == "PALOMA ZURITA":
        image_path = "images/PALOMA_ZURITA.jpg"
      elif animal == "PATO REAL O AZULÓN":
        image_path = "images/PATO_REAL_O_AZULON.jpg"
      elif animal == "PERDIZ ROJA":
        image_path = "images/PERDIZ_ROJA.jpg"
      elif animal == "TÓRTOLA":
        image_path = "images/TORTOLA.jpg"
      elif animal == "URRACAS,GRAJILLAS":
        image_path = "images/URRACAS_GRAJILLAS.jpg"
      elif animal == "ÁNADE REAL O AZULÓN":
        image_path = "images/ANADE_REAL_O_AZULON.jpg"
      else:
        image_path = "images/" + animal_path + ".jpg"
      st.image(image_path, width=300)
      # Periodo de caza
      st.write("📆 El **periodo de caza legal** es: ", periodos_caza[animal])
      
      for provincia in provincias:
        st.write("🎯 La **previsión de caza** en ", provincia, " para la próxima temporada:")
        # Time series preparation
        animal_provincia = caza[(caza.Provincia == provincia) & (caza.ESPECIE == animal)]
        capturas = animal_provincia['capturas']
        capturas = capturas.fillna(0)
        nonzero_counts = (capturas > 0).sum() 
        zero_counts = (capturas == 0).sum()
        if nonzero_counts <= 10 or  zero_counts >= 10: # Check if there are less than 10 non-zero records in the series
            st.warning("Información insuficiente para hacer la predicción.")
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

        # Handle case when no results are found
    if not resultados:
        st.warning("No se encontraron suficientes datos para generar una predicción. Por favor, reinicia la búsqueda con otros parámetros.")
        return None 

    resultados = pd.DataFrame(resultados)
    resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]] = resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]].astype(int)   
    
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

# Sección de Caza Responsable
if seleccion == "Consejos de Caza Sostenible":
    st.title("Consejos para una Caza Responsable")

    st.subheader("Períodos de caza legal en Castilla y León")
    st.table(periodos)
    
    # Buenas prácticas y consejos
    st.subheader("Consejos para una Caza Sostenible")
    st.write("""
    - **Respetar los periodos de caza**: Siempre asegúrate de conocer y seguir las fechas legales para cada especie.
    - **Licencias y permisos**: Asegúrate de contar con la licencia de caza actualizada y permisos específicos para la especie que planeas cazar.
    - **Evitar la sobrecaza**: Respeta los cupos de captura y ten en cuenta el estado de conservación de las especies.
    - **Uso adecuado del equipamiento**: Utiliza armas y munición adecuadas para cada especie, y asegúrate de realizar un disparo limpio y ético.
    - **Recuperación de las piezas**: Siempre intenta recuperar la pieza cazada, evitando dejar restos en el campo.
    - **Conservación del hábitat**: Minimiza el impacto ambiental durante la caza, cuidando la flora y fauna local.
    - **Recoge tus residuos**: No dejes basura en la naturaleza, incluyendo cartuchos de munición.
    """)


