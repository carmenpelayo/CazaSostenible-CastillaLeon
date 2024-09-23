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
    'BECADA': 'Desde el cuarto domingo de octubre hasta el cuarto domingo de enero del año siguiente (modalidades al salto, a rabo y en mano). Cupo: 3 ejemplares por cazador y día.',
    'CABRA MONTÉS': '1 de marzo al 30 de junio; 15 de septiembre al 15 de diciembre.',
    'CIERVO': '1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera); 4º domingo de septiembre al 4º domingo de febrero en todas las modalidades.',
    'CODORNIZ': '15 de agosto al 3er domingo de septiembre. Cupo: 20 ejemplares por cazador y día.',
    'CONEJO': '15 de agosto al 3er domingo de septiembre (media veda).',
    'CORNEJA': '15 de agosto al 3er domingo de septiembre (media veda).',
    'CÓRVIDOS': '15 de agosto al 3er domingo de septiembre (media veda).',
    'CORZO': 'Para ambos sexos: 1 de abril al 1er domingo de agosto, y del 1 de septiembre al 2º domingo de octubre. Solo hembras: 1 de enero al 4º domingo de febrero.',
    'FAISÁN': 'Desde el cuarto domingo de octubre hasta el cuarto domingo de enero del año siguiente.',
    'GAMO': '1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera); 4º domingo de septiembre al 4º domingo de febrero en todas las modalidades.',
    'JABALÍ': '1 de abril al 1er domingo de agosto (rececho y aguardo/espera); 1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera); 4º domingo de septiembre al 4º domingo de febrero (todas las modalidades).',
    'LIEBRE': 'Liebre con galgo: 12 de octubre al 4º domingo de enero.',
    'LOBO': 'Según el plan cinegético aprobado.',
    'MUFLÓN': 'Rececho y aguardo/espera durante todo el año; 4º domingo de septiembre al 4º domingo de febrero en todas las modalidades.',
    'OTRAS AVES ACUÁTICAS': 'Desde el cuarto domingo de octubre hasta el cuarto domingo de enero del año siguiente.',
    'PALOMA BRAVÍA': '25 de agosto al 3er domingo de septiembre (media veda).',
    'PALOMA TORCAZ': '1 de octubre al 2º domingo de febrero.',
    'PALOMA ZURITA': '1 de octubre al 2º domingo de febrero.',
    'PATO REAL': 'Desde el cuarto domingo de octubre hasta el cuarto domingo de enero del año siguiente.',
    'PERDIZ ROJA': 'Desde el cuarto domingo de octubre hasta el cuarto domingo de enero del año siguiente.',
    'REBECO': '1 de mayo al 15 de julio; 1 de septiembre al 15 de noviembre.',
    'TÓRTOLA': 'Caza prohibida. Cupo: 0 ejemplares por cazador y día.',
    'URRACAS,GRAJILLAS': '15 de agosto al 3er domingo de septiembre (media veda).',
    'VENADO': '1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera); 4º domingo de septiembre al 4º domingo de febrero en todas las modalidades.',
    'ZORRO': 'Durante la temporada general, en media veda y en cualquier caza mayor. Media veda: 15 de agosto al 3er domingo de septiembre.',
    'ZORZALES': '1 de octubre al 2º domingo de febrero.'
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
        image_path = "images/" + animal + ".jpg"
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
        if nonzero_counts <= 10 or zero_counts >= 10:
          continue
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
      return st.warning("No se encontraron suficientes datos para generar una predicción. Por favor, reinicia la búsqueda con otros parámetros.")
    # If there are results:
    else: 
      resultados = pd.DataFrame(resultados)
      resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]] = resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]].astype(int)   
      return st.table(resultados)
  
  # RESULTADOS
  if result:
    if not opcion1 or not opcion2:
          st.warning("Es obligatorio seleccionar al menos una provincia y un animal.")
    else:
      st.balloons()
      st.markdown("""---""")
      st.subheader("🏆 ¡Tus resultados!")
      match = predecir_caza(opcion1, opcion2)
      
# Sección de Caza Responsable
if seleccion == "Consejos de Caza Sostenible":
    st.title("Consejos para una Caza Responsable")
    st.subheader("Períodos de caza legal en Castilla y León")
    st.table(periodos)
    st.write("Fuente: **Junta de Castilla y León** (https://medioambiente.jcyl.es/web/es/caza-pesca/periodos-habiles.html#:~:text=Corzo%3A,el%20cuarto%20domingo%20de%20febrero).")
    
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


