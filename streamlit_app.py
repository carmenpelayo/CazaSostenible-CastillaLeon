import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Define las secciones de la app
secciones = ["🏆 ¡Traza tu estrategia de caza sostenible!", "🎓 ¡Aprende más sobre la caza sostenible!", "ℹ️ Más información"]

# Selecciona la sección con un selectbox en el sidebar o en la parte superior
seleccion = st.sidebar.selectbox("Selecciona una sección.", secciones)

# Periodos de caza
periodos_caza = {
    'ÁNADE REAL O AZULÓN': 'No se dispone de información específica.',
    'BECADA': 'Desde el 4º domingo de octubre hasta el 4º domingo de enero del año siguiente (modalidades al salto, a rabo y en mano), con un cupo máximo de 3 ejemplares por cazador y día.',
    'CABRA MONTÉS': 'Del 1 de marzo al 30 de junio y del 15 de septiembre al 15 de diciembre.',
    'CIERVO': 'Del 1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera), y del 4º domingo de septiembre al 4º domingo de febrero (todas las modalidades).',
    'CODORNIZ': 'Del 15 de agosto al 3er domingo de septiembre, con un cupo máximo de 20 ejemplares por cazador y día.',
    'CONEJO': 'Del 15 de agosto al 3er domingo de septiembre (media veda).',
    'CORNEJAS': 'Del 15 de agosto al 3er domingo de septiembre (media veda).',
    'CÓRVIDOS': 'Del 15 de agosto al 3er domingo de septiembre (media veda).',
    'CORZO': 'Ambos sexos: del 1 de abril al 1er domingo de agosto, y del 1 de septiembre al 2º domingo de octubre. Sólo hembras: del 1 de enero al 4º domingo de febrero.',
    'FAISÁN': 'Del 4º domingo de octubre al 4º domingo de enero del año siguiente.',
    'GAMO': 'Del 1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera), y del 4º domingo de septiembre al 4º domingo de febrero (todas las modalidades).',
    'JABALÍ': 'Del 1 de abril al 1er domingo de agosto y del 1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera), y del 4º domingo de septiembre al 4º domingo de febrero (todas las modalidades).',
    'LIEBRE': 'Del 12 de octubre al 4º domingo de enero (con galgo).',
    'LOBO': 'La caza de lobo no está permitida en Castilla y León (ver la Sentencia del Tribunal de Justicia en el asunto C-436/22).',
    'MUFLÓN': 'Durante todo el año (rececho y aguardo/espera), y del 4º domingo de septiembre al 4º domingo de febrero (todas las modalidades).',
    'OTRAS AVES ACUÁTICAS': 'Desde el 4º domingo de octubre hasta el 4º domingo de enero del año siguiente.',
    'PALOMA BRAVÍA': 'Del 25 de agosto al 3er domingo de septiembre (media veda).',
    'PALOMA TORCAZ': 'Del 1 de octubre al 2º domingo de febrero.',
    'PALOMA ZURITA': 'Del 1 de octubre al 2º domingo de febrero.',
    'PATO REAL O AZULÓN': 'Desde el 4º domingo de octubre hasta el 4º domingo de enero del año siguiente.',
    'PERDIZ ROJA': 'Desde el 4º domingo de octubre hasta el 4º domingo de enero del año siguiente.',
    'REBECO': 'Del 1 de mayo al 15 de julio y del 1 de septiembre al 15 de noviembre.',
    'TÓRTOLA': 'La caza de tórtola no está permitida en Castilla y León (ver la ORDEN FYM/811/2021 del Boletín Oficial del Estado).',
    'URRACAS,GRAJILLAS': 'Del 15 de agosto al 3er domingo de septiembre (media veda).',
    'VENADO': 'Del 1er domingo de septiembre al 4º sábado de septiembre (rececho y aguardo/espera), y del 4º domingo de septiembre al 4º domingo de febrero (todas las modalidades).',
    'ZORRO': 'Durante la temporada general (media veda y cualquier caza mayor), y del 15 de agosto al 3er domingo de septiembre (media veda).',
    'ZORZALES': 'Del 1 de octubre al 2º domingo de febrero.'
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
    "URRACAS,GRAJILLAS": "Las urracas y grajillas son córvidos conocidos por su habilidad para sobrevivir en entornos cambiantes.",
    "VENADO":"El venado, también conocido como ciervo, es una especie majestuosa que habita en bosques y praderas.",
    "ZORRO": "El zorro es un depredador versátil, conocido por su astucia y adaptación a diversos entornos.",
    "ZORZAL": "El zorzal es un ave migratoria que se alimenta de insectos y frutos, migrando grandes distancias."
}
descripciones = pd.DataFrame.from_dict(descripciones, orient='index', columns=['Descripción del animal'])

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
    "OTRAS AVES ACUÁTICAS": "No se dispone de información específica.",
    "PALOMA BRAVÍA": "Se caza en puestos fijos, a menudo con cimbeles o desde escondites estratégicos.",
    "PALOMA TORCAZ": "Se caza en pasos migratorios desde puestos fijos o al vuelo.",
    "PALOMA ZURITA": "Similar a la torcaz, se caza al vuelo en pasos migratorios o en cercanías de cultivos.",
    "PATO REAL O AZULÓN": "Se caza en humedales o lagunas mediante la técnica de puesto fijo o al vuelo.",
    "PERDIZ ROJA": "Se caza al salto con perros o en ojeo, una modalidad donde los cazadores esperan su salida.",
    "REBECO": "Se caza en rececho en alta montaña, siguiendo rastros y observando desde lejos.",
    "TÓRTOLA": "Se caza al vuelo en puestos fijos durante la migración, frecuentemente cerca de cultivos.",
    "URRACAS,GRAJILLAS": "Se cazan con escopeta, a menudo mediante reclamo o en batidas.",
    "VENADO": "Se caza en montería, batida o rececho, aprovechando el celo y las grandes extensiones de monte.",
    "ZORRO": "Se caza en batidas, aguardos o al salto, a menudo en zonas donde causa daños.",
    "ZORZAL": "Se caza en pasos migratorios desde puestos fijos o al vuelo en zonas de olivares."
}
modo_caza = pd.DataFrame.from_dict(modo_caza, orient='index', columns=['Método de captura'])

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
      elif animal == "CORNEJAS":
        image_path = "images/CORNEJAS.png"
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
      st.image(image_path, use_column_width=True)

      st.write("✏️ **Descripción**: ", descripciones[animal])
      st.write("🎯 **Cómo cazar**: ", modo_caza[animal])
      st.write("📆 **Periodo de caza legal**: ", periodos_caza[animal])
      
      for provincia in provincias:
        st.write("📈 **Previsión de capturas** en ", provincia, " para la próxima temporada:")
        # Time series preparation
        animal_provincia = caza[(caza.Provincia == provincia) & (caza.ESPECIE == animal)]
        capturas = animal_provincia['capturas']
        capturas = capturas.fillna(0)
        nonzero_counts = (capturas > 0).sum() 
        zero_counts = (capturas == 0).sum()
        if nonzero_counts <= 7 or zero_counts >= 7:
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
      st.image("images/ODS.png", width=300)
      
# Sección de Caza Responsable
if seleccion == "🎓 ¡Aprende más sobre la caza sostenible!":
    st.title("¡Aprende más sobre la caza sostenible!")
    st.markdown("¿Sabías que...")
    st.markdown("           ...más del **80% del territorio nacional** es coto de caza?")
    st.markdown("           ...hay más de **800.000 cazadores** en España?")
    st.markdown("           ...el total económico que mueve la caza anualmente es de **4.000 millones de euros**?")
    st.write("Dada la **relevancia de la caza en España**, es importante asegurar que ésta sea sostenible. De esta forma, podremos **preservar los ecosistemas** y **mantener de las poblaciones de fauna silvestre**.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["✏️ Buenas prácticas", "🐗 Descripción de animales", "📆 Períodos de caza", "🎯 Métodos de caza", "🌎 Organizaciones"])

    with tab1:
        st.subheader("✏️ Buenas prácticas de caza sostenible")
        st.write("La caza sostenible no sólo implica seguir las normativas, sino también adoptar prácticas que promuevan la conservación del medio ambiente. A continuación, se presentan algunas recomendaciones:")
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

    # Descripciones de animales
    with tab2:
        st.subheader("🐗 Descripción de animales")
        st.table(descripciones)
    
    # Periodos de caza
    with tab3:
        st.subheader("📆 Períodos de caza legal en Castilla y León")
        st.write("Limitando tus sesiones de caza a los periodos permitidos, estás **respetando el ciclo natural de reproducción de los animales**, contribuyendo así a la **conservación de la biodiversidad en Castilla y León**.")
        st.table(periodos)
        st.image("images/periodos.png", use_column_width=True)
        st.write("Fuente: **Junta de Castilla y León** (https://medioambiente.jcyl.es/web/es/caza-pesca/periodos-habiles.html).")

    # Métodos de caza
    with tab4:
        st.subheader("🎯 Métodos de caza")
        st.table(modo_caza)

    with tab5:
        respaldos = {
            "INSTITUCIÓN": [
                "NACIONES UNIDAS (ONU)",
                "NACIONES UNIDAS (ONU)",
                "NACIONES UNIDAS (ONU)",
                "NACIONES UNIDAS (ONU)",
                "UNIÓN INTERNACIONAL PARA LA CONSERVACIÓN DE LA NATURALEZA (UICN)",
                "UNIÓN INTERNACIONAL PARA LA CONSERVACIÓN DE LA NATURALEZA (UICN)",
                "UNIÓN INTERNACIONAL PARA LA CONSERVACIÓN DE LA NATURALEZA (UICN)",
                "UNIÓN INTERNACIONAL PARA LA CONSERVACIÓN DE LA NATURALEZA (UICN)",
                "UNIÓN INTERNACIONAL PARA LA CONSERVACIÓN DE LA NATURALEZA (UICN)",
                "UNIÓN INTERNACIONAL PARA LA CONSERVACIÓN DE LA NATURALEZA (UICN)",
                "CONSEJO DE EUROPA (COE)",
                "CONSEJO DE EUROPA (COE)",
                "CONSEJO DE EUROPA (COE)",
                "CONSEJO DE EUROPA (COE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "UNIÓN EUROPEA (UE)",
                "EUROPEAN LANDOWNER ORGANIZATION (ELO)",
                "EUROPEAN LANDOWNER ORGANIZATION (ELO)",
                "AGENCIA FEDERAL DE MEDIOAMBIENTE DE AUSTRIA",
                "AGENCIA FEDERAL DE MEDIOAMBIENTE DE AUSTRIA",
                "AGENCIA FEDERAL DE MEDIOAMBIENTE DE AUSTRIA",
                "BIRDLIFE INTERNATIONAL",
                "CONSEJO INTERNACIONAL DE LA CAZA Y CONSERVACIÓN DE LA FAUNA (CIC)",
                "CONSEJO INTERNACIONAL DE LA CAZA Y CONSERVACIÓN DE LA FAUNA (CIC)",
                "CONSEJO INTERNACIONAL DE LA CAZA Y CONSERVACIÓN DE LA FAUNA (CIC)"
            ],
            "AÑO": [
                1987,
                1992,
                2000,
                2004,
                1980,
                2000,
                2004,
                2006,
                2008,
                2012,
                1979,
                2004,
                2007,
                2007,
                1979,
                2001,
                2004,
                2004,
                2008,
                2009,
                1992,
                2008,
                2009,
                2006,
                2008,
                2003,
                2008,
                1997,
                2001,
                2006,
                2006,
                2008,
                2009,
                2011
            ],
            "INSTRUMENTO": [
                "Informe Brundtland",
                "Convenio sobre Diversidad Biológica (CDB)",
                "CDB: Enfoque por Ecosistemas",
                "CDB: Principios y Directrices de Addis Abeba",
                "Estrategia Mundial para la Conservación",
                "Resolución 2.29 del II Congreso Mundial de la UICN: Declaración de la política de la UICN acerca del uso sostenible de los recursos vivos silvestres (Declaración de Amman)",
                "Resolución 3.093 del III Congreso Mundial de la UICN: Aplicación de la política de la UICN sobre el uso consuntivo de la fauna silvestre y la caza recreativa en África meridional",
                "Directrices de Caza Sostenible en Europa",
                "Resolución 4.026 del IV Congreso Mundial de la UICN: Fomento de la confianza para la conservación de la biodiversidad y la utilización sostenible en consonancia con la Carta Europea sobre Caza y Biodiversidad",
                "Directrices de la Comisión de Supervivencia de Especies (CSE) de la UICN sobre la caza de trofeos como instrumento para crear incentivos para la conservación",
                "Convenio de Berna",
                "Recomendación PACE 1689 La caza y el equilibrio ambiental de Europa",
                "Carta Europea sobre Caza y Biodiversidad",
                "Recomendación 128 del Comité Permanente del Convenio de Berna de la Carta Europea sobre Caza y Biodiversidad a los Estados firmantes del Convenio",
                "Directiva Aves",
                "Directiva Aves: Iniciativa Caza Sostenible (Sustainable Hunting Initiative, SHI)",
                "Directiva Aves: Acuerdo sobre Caza Sostenible entre FACE y BirdLife Internacional",
                "Directiva Aves: Guía sobre la caza en virtud de la Directiva Aves",
                "Directiva Aves: Guía para la caza sostenible de las aves silvestres",
                "Estrategia de la Unión Europea para el Desarrollo Sostenible",
                "Directiva Hábitats",
                "Directiva Hábitats: Iniciativa Caza y Pesca Sostenible (Sustainable Hunting and Angling Initiative, SHAI)",
                "Directiva Hábitats: Conferencia “Promoción de Natura 2000 y el Uso Sostenible de la Fauna” (Promoting Natura 2000 & Sustainable Wildlife Use)",
                "Red Natura 2000: Proyecto “Fomento de la Red Natura 2000 entre sus usuarios, en particular los cazadores”",
                "Proyecto “Hunting for Sustainability”",
                "Pilot Wildlife Estates initiative (PWEi)",
                "Iniciativa Cotos Faunísticos (Wildlife Estates initiative, WEi)",
                "Reunión de trabajo “Caza y Sostenibilidad” del cual deriva el documento “Fundamentos de Criterios e Indicadores de Caza Sostenible”",
                "Criterios e Indicadores de Caza Sostenible",
                "Caza Sostenible. Principios, Criterios e Indicadores",
                "Proyecto Caza Sostenible: Directrices para avanzar hacia la caza sostenible de aves migratorias en el Mediterráneo",
                "Programa “Turismo de caza sostenible” (incluye el libro “Buenas prácticas en caza sostenible”)",
                "Estudio (junto con FAO): “Principios para el Desarrollo Sostenible de Leyes de Gestión de Fauna)",
                "Fauna y Cría Comercial de Animales Anteriormente Silvestres"
            ]
        }
        respaldos = pd.DataFrame(respaldos)
        st.subheader("🌎 Organizaciones Internacionales")
        st.write("Las siguientes instituciones y organizacions internacionales **promueven la caza sostenible** mediante la ordenanza de las siguientes **normativas** y **códigos de práctica**:")
        st.table(respaldos)

if seleccion == "ℹ️ Más información":
    st.header("ℹ️ Más información")
    st.write("Aquí puedes consultar más información sobre la aplicación, incluyendo una **explicación detallada del modelo de predicción** utilizado, **recursos adicionales de caza** y **links de referencia** al contacto de la desarrolladora y el código fuente.")
    tab1, tab2, tab3 = st.tabs(["📈 Modelo Predictivo", "🎒 Más recursos", "👤 Referencia"])
    # Modelo predictivo
    with tab1:
        st.subheader("📈 Modelo de predicción de capturas")
        st.markdown("""El objetivo de nuestro modelo predictivo aplicado es **predecir el número de capturas en una temporada de caza**, basándonos en los datos históricos de capturas previas. 
                       Estas previsiones permiten a los cazadores planificar sus sesiones cinegéticas de manera más efectiva, **aumentando así las probabilidades de éxito**.""")
        st.markdown("Para esto usamos el **modelo ARIMA (Autoregressive Integrated Moving Average)**, una técnica estadística ampliamente utilizada para el análisis de series temporales.") 
        st.markdown("""
                       #### Configuración del Modelo
                       El modelo utilizado ha sido configurado como `ARIMA(capturas, order=(2,0,2))`. Esto indica que:
                       - \( p = 2 \): Se utilizan dos **términos autoregresivos** (*Auto-Regressive*), es decir, los dos valores de capturas anteriores influyen en la predicción.
                       - \( d = 0 \): No se aplica ninguna diferenciación (*Integrated*) porque los datos son estacionarios.
                       - \( q = 2 \): Se utilizan dos términos de **promedio móvil** (*Moving-Average*), lo que significa que los errores de predicción de los dos periodos anteriores también se tienen en cuenta.""")
        st.image("images/arima.png")
        st.markdown("Aplicando esta fórmula, podemos **estimar la cantidad de capturas *Yt* en la siguiente temporada** de caza, basándonos en el **patrón de capturas históricas** del animal y provincia seleccionados.") 
    # Más recursos
    with tab2:
        st.subheader("🎒 Más recursos")
        st.markdown("- [**Normativa vigente en Castilla y León**](%s)" % "http://medioambiente.jcyl.es/web/jcyl/MedioAmbiente/es/Plantilla100DetalleFeed/1246988359553/Normativa/1175259754359/Redaccion", unsafe_allow_html=True)
        st.markdown("- [**Guía práctica del cazador**](%s)" % "https://medioambiente.jcyl.es/web/es/caza-pesca/guia-practica-cazador.html", unsafe_allow_html=True)
    # Autor
    with tab3:
        st.subheader("👤 Referencia")
        st.write("El presente trabajo ha sido construído por **[Carmen Pelayo Fernández](%s)**. Puedes contactarle mandando un correo a *carmenpelayofdez@gmail.com*." % "https://www.linkedin.com/in/carmenpelayofernandez/", unsafe_allow_html=True)
        st.write("Todos los códigos fuente pueden ser consultados en **[GitHub](%s)**" % "https://github.com/carmenpelayo/HuntPrediction", unsafe_allow_html=True)
        
    


