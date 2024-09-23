import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Define las secciones de la app
secciones = ["🏆 ¡Traza tu estrategia de caza sostenible!", "🎓 ¡Aprende más sobre la caza sostenible!"]

# Selecciona la sección con un selectbox en el sidebar o en la parte superior
seleccion = st.sidebar.selectbox("Selecciona una sección.", secciones)

# Periodos de caza
periodos_caza = {
    'ÁNADE REAL O AZULÓN': '(No se dispone de información).',
    'BECADA': 'desde el cuarto domingo de Octubre hasta el cuarto domingo de Enero del año siguiente (modalidades al salto, a rabo y en mano), con un cupo máximo de **3 ejemplares por cazador y día**.',
    'CABRA MONTÉS': 'del 1 de Marzo al 30 de Junio y del 15 de Septiembre al 15 de Diciembre.',
    'CIERVO': 'del primer domingo de Septiembre al cuarto sábado de Septiembre (rececho y aguardo/espera); y del cuarto domingo de Septiembre al cuarto domingo de Febrero en todas las modalidades.',
    'CODORNIZ': 'del 15 de Agosto al tercer domingo de Septiembre, con un cupo máximo de 20 ejemplares por cazador y día.',
    'CONEJO': 'del 15 de Agosto al tercer domingo de Septiembre (media veda).',
    'CORNEJAS': 'del 15 de Agosto al tercer domingo de Septiembre (media veda).',
    'CÓRVIDOS': 'del 15 de Agosto al tercer domingo de septiembre (media veda).',
    'CORZO': 'del 1 de abril al primer domingo de Agosto y del 1 de Septiembre al segundo domingo de Octubre (para ambos sexos); del 1 de enero al cuarto domingo de febrero (sólo hembras).',
    'FAISÁN': 'desde el cuarto domingo de Octubre hasta el cuarto domingo de Enero del año siguiente.',
    'GAMO': 'desde el primer domingo de Septiembre al cuarto sábado de septiembre (rececho y aguardo/espera) y del cuarto domingo de Septiembre al cuarto domingo de Febrero (en todas las modalidades).',
    'JABALÍ': 'del 1 de Abril al primer domingo de agosto (rececho y aguardo/espera); 1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera); 4º domingo de septiembre al 4º domingo de febrero (todas las modalidades).',
    'LIEBRE': 'del 12 de Octubre al cuarto domingo de Enero (con galgo).',
    'LOBO': '(No existe periodo caza legal del lobo).',
    'MUFLÓN': 'durante todo el año (rececho y aguardo/espera); y del 4º domingo de septiembre al 4º domingo de febrero en todas las modalidades.',
    'OTRAS AVES ACUÁTICAS': 'desde el cuarto domingo de octubre hasta el cuarto domingo de enero del año siguiente.',
    'PALOMA BRAVÍA': 'del 25 de agosto al 3er domingo de septiembre (media veda).',
    'PALOMA TORCAZ': 'del 1 de octubre al 2º domingo de febrero.',
    'PALOMA ZURITA': 'del 1 de octubre al 2º domingo de febrero.',
    'PATO REAL O AZULÓN': 'desde el cuarto domingo de octubre hasta el cuarto domingo de enero del año siguiente.',
    'PERDIZ ROJA': 'desde el cuarto domingo de octubre hasta el cuarto domingo de enero del año siguiente.',
    'REBECO': 'del 1 de mayo al 15 de julio y del 1 de septiembre al 15 de noviembre.',
    'TÓRTOLA': '(No existe periodo caza legal de la tórtola).',
    'URRACAS,GRAJILLAS': 'del 15 de agosto al 3er domingo de septiembre (media veda).',
    'VENADO': 'del 1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera) y del 4º domingo de septiembre al 4º domingo de febrero (todas las modalidades).',
    'ZORRO': 'durante la temporada general (en media veda y en cualquier caza mayor) y del 15 de agosto al 3er domingo de septiembre (media veda).',
    'ZORZAL': 'del 1 de octubre al 2º domingo de febrero.'
}
periodos = pd.DataFrame.from_dict(periodos_caza, orient='index', columns=['Período de caza legal'])

descripciones = {
    "ÁNADE REAL O AZULÓN": "El ánade real es el pato más común en Europa, reconocido por la cabeza verde del macho.",
    "BECADA": "La becada es un ave migratoria de hábitos nocturnos que se oculta en bosques densos.",
    "CABRA MONTÉS": "La cabra montés habita en terrenos montañosos y se caracteriza por su agilidad en zonas escarpadas.",
    "CIERVO": "El ciervo es el mayor herbívoro de los bosques europeos, famoso por su majestuosa cornamenta.",
    "CODORNIZ": "La codorniz es un ave pequeña y migratoria que prefiere zonas abiertas como campos de cultivo.",
    "CONEJO": "El conejo es una especie clave en los ecosistemas ibéricos, siendo presa de muchos depredadores.",
    "CORNEJAS": "Las cornejas son aves oportunistas y carroñeras que pueden afectar cultivos.",
    "CORZO": "El corzo es el cérvido más pequeño de Europa, conocido por su agudo sentido del olfato.",
    "CÓRVIDOS": "Los córvidos son aves inteligentes y sociales que a menudo son cazadas por su impacto en cultivos.",
    "FAISÁN": "El faisán, de plumaje colorido, es una especie introducida que se cría para la caza en Europa.",
    "GAMO": "El gamo se distingue por su cornamenta en forma de pala y su pelaje moteado.",
    "JABALÍ": "El jabalí es un animal omnívoro y adaptable, cuya población ha crecido rápidamente en algunas regiones.",
    "LIEBRE": "La liebre es un corredor veloz que se desplaza en hábitats abiertos como pastizales y cultivos.",
    "LOBO": "El lobo es un depredador clave para el equilibrio de los ecosistemas, controlando las poblaciones de herbívoros.",
    "MUFLÓN": "El muflón es un carnero salvaje originario de Europa que habita en zonas montañosas.",
    "OTRAS AVES ACUÁTICAS": "Las aves acuáticas dependen de humedales para su supervivencia, lo que las hace vulnerables a la pérdida de hábitat.",
    "PALOMA BRAVÍA": "La paloma bravía es conocida por su capacidad para adaptarse a entornos urbanos y rurales.",
    "PALOMA TORCAZ": "La paloma torcaz es la mayor de las palomas ibéricas, famosa por su vuelo rápido y poderoso.",
    "PALOMA ZURITA": "La paloma zurita es más pequeña que la torcaz y se distingue por su pecho grisáceo.",
    "PATO REAL O AZULÓN": "El pato real es fácilmente reconocible por su cabeza verde iridiscente en los machos.",
    "PERDIZ ROJA": "La perdiz roja es una especie emblemática en España, conocida por su resistencia y comportamiento gregario.",
    "REBECO": "El rebeco es un animal ágil de alta montaña, con cuernos curvados característicos.",
    "TÓRTOLA": "La tórtola es un ave migratoria cuyo canto melódico es característico del verano.",
    "URRACAS, GRAJILLAS": "Las urracas y grajillas son córvidos conocidos por su habilidad para sobrevivir en entornos cambiantes.",
    "VENADO":"El venado, también conocido como ciervo, es una especie majestuosa que habita en bosques y praderas.",
    "ZORRO": "El zorro es un depredador versátil, conocido por su astucia y adaptación a diversos entornos.",
    "ZORZAL": "El zorzal es un ave migratoria que se alimenta de insectos y frutos, migrando grandes distancias."
}

modo_caza = {
    "ÁNADE REAL O AZULÓN": "Se caza en humedales o ríos mediante puestos fijos o al vuelo.",
    "BECADA": "Se caza principalmente mediante la técnica de caza al salto con perros de muestra, en bosques y zonas húmedas.",
    "CABRA MONTÉS": "Se caza mediante rececho en terrenos montañosos, siguiendo su rastro y observando desde largas distancias.",
    "CIERVO": "Se caza principalmente en montería, batida o rececho, dependiendo de la zona y las condiciones.",
    "CODORNIZ": "Se caza al salto, normalmente con la ayuda de perros, en terrenos abiertos o campos de cultivo.",
    "CONEJO": "Se caza al salto o con hurones, a menudo en zonas de matorrales o campos de cultivo.",
    "CORNEJAS": "Se caza con escopeta, atrayéndolas mediante reclamo o en batidas organizadas.",
    "CORZO": "Se caza mediante rececho o en batidas, especialmente durante la temporada de celo en zonas boscosas.",
    "CÓRVIDOS": "Se cazan en batidas o con cimbeles (reclamos), sobre todo en cultivos donde pueden causar daños.",
    "FAISÁN": "Se caza al salto con perros o en sueltas organizadas en terrenos abiertos y de caza menor.",
    "GAMO": "Se caza en monterías, batidas o rececho en terrenos amplios y de monte bajo.",
    "JABALÍ": "Se caza en monterías, batidas o aguardos nocturnos, aprovechando su actividad nocturna.",
    "LIEBRE": "Se caza al salto con perros de rastro o de carrera (galgos) en llanuras o campos abiertos.",
    "LOBO": "Se caza mediante aguardos, rececho o batida en terrenos montañosos o boscosos.",
    "MUFLÓN": "Se caza en rececho, sobre todo en zonas montañosas o de difícil acceso.",
    "PALOMA BRAVÍA": "Se caza en puestos fijos, a menudo con cimbeles o desde escondites estratégicos.",
    "PALOMA TORCAZ": "Se caza en pasos migratorios desde puestos fijos o al vuelo.",
    "PALOMA ZURITA": "Similar a la torcaz, se caza al vuelo en pasos migratorios o en cercanías de cultivos.",
    "PATO REAL O AZULÓN": "Se caza en humedales o lagunas mediante la técnica de puesto fijo o al vuelo.",
    "PERDIZ ROJA": "Se caza al salto con perros o en ojeo, una modalidad donde los cazadores esperan su salida.",
    "REBECO": "Se caza en rececho en alta montaña, siguiendo rastros y observando desde lejos.",
    "TÓRTOLA": "Se caza al vuelo en puestos fijos durante la migración, frecuentemente cerca de cultivos.",
    "URRACAS": "Se cazan con escopeta, a menudo mediante reclamo o en batidas.",
    "VENADO": "Se caza en montería, batida o rececho, aprovechando el celo y las grandes extensiones de monte.",
    "ZORRO": "Se caza en batidas, aguardos o al salto, a menudo en zonas donde causa daños.",
    "ZORZAL": "Se caza en pasos migratorios desde puestos fijos o al vuelo en zonas de olivares."
}

# Sección de Caza Responsable
if seleccion == "🏆 ¡Traza tu estrategia de caza sostenible!":
  st.title("¡Configura tu estrategia de caza sostenible en Castilla y León en 10 segundos!")
  st.write("""Con esta herramienta, podrás trazar tu **estrategia de caza sostenible**, la cual **maximizará tu probabilidad de éxito** en tus sesiones de caza 
              (mediante la predicción de la combinación ubicación-animal que optimiza la captura de animales), además de **preservar los ciclos naturales de reproducción animal**
              (mediante la limitación de las sesiones a los periodos legales de captura de animales).""")
  
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
      st.markdown("---")
      st.subheader(animal)
      if animal == "CABRA MONTÉS":
        image_path = "images/CABRA_MONTES.jpg"
      elif animal == "CÓRVIDOS":
        image_path = "images/CORVIDOS.png"
      elif animal == "CORZO":
        image_path = "images/CORZO.png"
      elif animal == "FAISÁN":
        image_path = "images/FAISAN.jpg"
      elif animal == "JABALÍ":
        image_path = "images/JABALI.jpg"
      elif animal == "LOBO":
        image_path = "images/LOBO.png"
      elif animal == "MUFLÓN":
        image_path = "images/MUFLON.jpg"
      elif animal == "OTRAS AVES ACUÁTICAS":
        image_path = "images/OTRAS-AVES-ACUATICAS.jpg"
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

      st.write("✏️ ", descripciones[animal])
      st.write("🎯 ", modo_caza[animal])
      st.write("📆 El **periodo de caza legal** es ", periodos_caza[animal])
      
      for provincia in provincias:
        st.write("📈 La **previsión de caza** en ", provincia, " para la próxima temporada:")
        # Time series preparation
        animal_provincia = caza[(caza.Provincia == provincia) & (caza.ESPECIE == animal)]
        capturas = animal_provincia['capturas']
        capturas = capturas.fillna(0)
        nonzero_counts = (capturas > 0).sum() 
        zero_counts = (capturas == 0).sum()
        if nonzero_counts <= 10 or zero_counts >= 10:
            st.warning(f"Información insuficiente para predecir la caza de {animal} en {provincia}.")
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
        return None
    # If there are results:
    else: 
        st.write("⭐ Para **maximizar tus probabilidades de éxito**, te recomendamos que caces...")
        resultados = pd.DataFrame(resultados)
        resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]] = resultados[["Previsión de caza mínima", "Previsión de caza media", "Previsión de caza máxima"]].astype(int)
        resultados = resultados.sort_values(by=['Previsión de caza media'], ascending=False)
        return st.table(resultados)
  
  # RESULTADOS
  if result:
    if not opcion1 or not opcion2:
          st.warning("Es obligatorio seleccionar al menos una provincia y un animal.")
    else:
      st.balloons()
      st.subheader("🏆 ¡Tus resultados!")
      match = predecir_caza(opcion1, opcion2)
      st.write("Siguiendo una estrategia de caza sostenible, estás contribuyendo al Objetivo 15 (*Vida de Ecosistemas Terrestres*) de los **Objetivos de Desarrollo Sostenible de las Naciones Unidas**.")
      st.image("images/ODS.png", width=500)
      
# Sección de Caza Responsable
if seleccion == "🎓 ¡Aprende más sobre la caza sostenible!":
    st.title("Aprende más sobre la caza sostenible")
    st.write("La caza sostenible es esencial para la **preservación de los ecosistemas** y el **mantenimiento de las poblaciones de fauna silvestre**. Estos objetivos están en línea con el Objetivo 15 de los Objetivos de Desarrollo Sostenible de las Naciones Unidas.")
    st.image("images/ODS.png", width=500)
    
    # Buenas prácticas y consejos
    st.subheader("✏️ Buenas prácticas")
    st.write("La caza sostenible no sólo implica seguir las normativas, sino también adoptar prácticas que promuevan la sostenibilidad y la conservación del medio ambiente. A continuación, se presentan recomendaciones detalladas para llevar a cabo una caza ética y consciente:")
    
    # Consejos detallados
    consejos = {
        "Respetar los periodos de caza": (
            "Conocer y seguir las fechas legales para cada especie es fundamental para asegurar su conservación. "
            "Los periodos de caza están diseñados para proteger las especies durante su época de reproducción, "
            "por lo que es crucial respetarlos para mantener el equilibrio ecológico."
        ),
        "Licencias y permisos": (
            "Asegúrate de contar con la licencia de caza actualizada y de cumplir con los requisitos específicos "
            "para la especie que planeas cazar. Las licencias no solo son un requisito legal, sino que también "
            "garantizan que los cazadores están informados sobre las regulaciones vigentes y las buenas prácticas."
        ),
        "Evitar la sobrecaza": (
            "Respeta los cupos de captura establecidos y mantente informado sobre el estado de conservación de las especies. "
            "La sobrecaza puede llevar a la extinción local de especies y a desequilibrios en los ecosistemas."
        ),
        "Uso adecuado del equipamiento": (
            "Utiliza armas y munición adecuadas para cada especie, y asegúrate de realizar un disparo limpio y ético. "
            "Conocer tu equipo y tener la habilidad necesaria para usarlo de manera responsable es clave para "
            "minimizar el sufrimiento del animal."
        ),
        "Recuperación de las piezas": (
            "Siempre intenta recuperar la pieza cazada. No dejar restos en el campo es importante para el bienestar "
            "de otros animales y para la salud del ecosistema."
        ),
        "Conservación del hábitat": (
            "Minimiza el impacto ambiental durante la caza cuidando la flora y fauna local. Evita dañar áreas sensibles "
            "y sigue prácticas que protejan los hábitats naturales."
        ),
        "Recoge tus residuos": (
            "No dejes basura en la naturaleza, incluyendo cartuchos de munición y cualquier otro tipo de residuos. "
            "La limpieza del entorno es responsabilidad de cada cazador y contribuye a la salud del ecosistema."
        ),
        "Educación y formación continua": (
            "Participa en talleres, seminarios y cursos sobre caza sostenible y conservación de la naturaleza. "
            "La educación es clave para estar al tanto de las mejores prácticas y nuevas regulaciones."
        ),
        "Informar a otros cazadores": (
            "Comparte tus conocimientos y experiencias con otros cazadores. La comunicación y la sensibilización son "
            "fundamentales para fomentar una cultura de caza responsable."
        )
    }

    for consejo, descripcion in consejos.items():
        st.write(f"- **{consejo}**: {descripcion}")

    # Periodos de caza
    st.subheader("📆 Períodos de caza legal en Castilla y León")
    st.write("Limitando tus sesiones de caza a los periodos permitidos, estás **respetando el ciclo natural de reproducción de los animales**, contribuyendo así a la **conservación de la biodiversidad en Castilla y León**.")
    st.table(periodos)
    st.write("Fuente: **Junta de Castilla y León** (https://medioambiente.jcyl.es/web/es/caza-pesca/periodos-habiles.html).")
    
    


