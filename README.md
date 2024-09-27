# Introducción

## Memoria: "Caza Sostenible en Castilla y León"

La aplicación "Caza Sostenible en Castilla y León" (accesible en [caza-castillayleon.streamlit.app](https://caza-castillayleon.streamlit.app/)) ha sido diseñada como un recurso didáctico innovador que combina tecnología y educación en el ámbito de la caza responsable. Su objetivo principal es predecir las capturas de diversas especies de caza en Castilla y León, basándose en datos históricos, para promover prácticas respetuosas con el medio ambiente. Esta herramienta se alinea con los Objetivos de Desarrollo Sostenible (ODS), en particular, el Objetivo 15 (Vida de Ecosistemas Terrestres).

## Motivación

La caza sostenible es esencial para la preservación de los ecosistemas y el mantenimiento de las poblaciones de fauna silvestre. La aplicación busca no solo proporcionar información útil a los cazadores, sino también educarlos sobre la importancia de respetar las regulaciones y los ciclos naturales de reproducción. Al hacerlo, se fomenta un enfoque consciente que cumple con las normativas vigentes y contribuye al bienestar de la naturaleza.

## Estructura Técnica de la Aplicación

1. **Base de Datos Utilizada**  
   La aplicación se basa en un conjunto de datos que incluye registros históricos de capturas de diversas especies en Castilla y León. Este conjunto de datos, denominado `resultados-temporadas-cinegeticas.csv`, fue obtenido del [Portal de Datos Abiertos de la Junta de Castilla y León](https://datosabiertos.jcyl.es/web/es/datos-abiertos-castilla-leon.html).

2. **Framework Utilizado**  
   La aplicación está desarrollada utilizando `streamlit`, un framework de código abierto que permite crear aplicaciones con Python. Las funcionalidades clave utilizadas en la aplicación incluyen:
   - **Componentes Interactivos**: La aplicación utiliza select boxes y multiselects para permitir a los usuarios seleccionar las provincias y las especies de caza de su interés.
   - **Visualización**: Streamlit facilita la visualización de gráficos generados con `matplotlib`, permitiendo a los usuarios observar las tendencias históricas y las predicciones de capturas de forma clara y atractiva.
   - **Manejo de Estado**: Los botones y las interacciones de usuario permiten gestionar el flujo de la aplicación y la presentación de resultados en tiempo real.

3. **Modelo Predictivo**  
   El núcleo de la funcionalidad de la aplicación es su modelo predictivo, que utiliza el algoritmo ARIMA (Autoregressive Integrated Moving Average) para realizar pronósticos sobre las capturas de caza. A continuación, se detallan los pasos técnicos del proceso de modelización:
   - **Preparación de Datos**: Los datos de capturas se filtran para cada combinación de provincia y especie. Se requiere un mínimo de 10 observaciones no nulas para asegurar la validez del modelo, lo que ayuda a identificar patrones significativos en las series temporales.
   - **Ajuste del Modelo**: Se ajusta un modelo ARIMA con parámetros (2,0,2). Este modelo es adecuado para datos que presentan características de autocorrelación y estacionalidad, comunes en las series de tiempo relacionadas con la caza.
   - **Predicción**: Una vez ajustado el modelo, se generan pronósticos para la próxima temporada de caza (en este caso, de la temporada 2023-2024, pues solo se disponen de datos hasta 2022). La aplicación proporciona no solo una previsión puntual de las capturas, sino también un intervalo de confianza del 95%, permitiendo a los usuarios entender la incertidumbre inherente a las predicciones.
   - **Resultados y Visualización**: La aplicación utiliza gráficos de líneas para mostrar las capturas históricas y las predicciones futuras. Se incluye un intervalo de confianza que destaca la variabilidad de las previsiones, facilitando una interpretación más rica de los datos.

4. **Interacción y Usabilidad**  
   La aplicación ha sido diseñada con un enfoque en la experiencia del usuario. La interfaz intuitiva permite a los usuarios:
   - **Consultar Información Específica**: Los cazadores pueden seleccionar fácilmente provincias y especies para obtener pronósticos personalizados.
   - **Recibir Recomendaciones**: Basándose en las predicciones, se ofrecen recomendaciones sobre las mejores prácticas de caza, ayudando a los cazadores a maximizar su éxito sin comprometer la sostenibilidad.
   - **Acceder a Consejos de Caza Responsable**: La sección dedicada a consejos proporciona a los usuarios pautas sobre la caza respetuosa con el medio ambiente.

## Integración con la Vida Real

La aplicación se puede utilizar en diferentes momentos del ciclo de la actividad cinegética:
- **Antes de la Temporada**: Los cazadores pueden utilizar la aplicación para planificar sus actividades, verificando qué especies pueden cazar legalmente y cuáles son las previsiones de captura en diferentes provincias.
- **Durante la Temporada**: La app permite a los cazadores consultar la información sobre regulaciones y prácticas sostenibles, lo que facilita el cumplimiento de las normativas locales.
- **Educación Continua**: A través de la aplicación, se promueve una cultura de respeto hacia la naturaleza y la sostenibilidad, contribuyendo a formar una comunidad de cazadores más informada y responsable.

## Conclusiones

La aplicación "Caza Sostenible en Castilla y León" es un avance significativo en la intersección de la caza y la tecnología. Al integrar un modelo predictivo robusto con una interfaz de usuario accesible, proporciona una herramienta valiosa para los cazadores que desean practicar de manera responsable y sostenible. Este enfoque no solo ayuda a maximizar el éxito de las cacerías, sino que también fomenta un respeto más profundo por el medio ambiente, garantizando que las futuras generaciones puedan disfrutar de la caza y la naturaleza.

## Referencias
- Junta de Castilla y León, 2024. Portal de Datos Abiertos. [Enlace](https://datosabiertos.jcyl.es/web/es/datos-abiertos-castilla-leon.html)
- Junta de Castilla y León, 2024. Períodos de caza legal. [Enlace](https://medioambiente.jcyl.es/web/es/caza-pesca/periodos-habiles.html) (Accedido: 12 de agosto de 2024).
- Organización de las Naciones Unidas (ONU), 2015. Objetivos de Desarrollo Sostenible. [Enlace] disponible en: [https://www.un.org/sustainabledevelopment/es/](https://www.un.org/sustainabledevelopment/es/) (Accedido: 13 de agosto de 2024).
- Statsmodels Documentation, 2023. Statsmodels. [Enlace] disponible en: [https://www.statsmodels.org/stable/index.html](https://www.statsmodels.org/stable/index.html) (Accedido: 23 de agosto de 2024).
- Streamlit Documentation, 2023. Streamlit. [Enlace] disponible en: [https://docs.streamlit.io/](https://docs.streamlit.io/) (Accedido: 23 de agosto de 2024).

