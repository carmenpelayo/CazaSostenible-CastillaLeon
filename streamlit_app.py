import streamlit as st

st.title("🔍 Tu estrategia de caza")
st.write("""¡Encuentra la mejor forma de cazar en Castilla y La Mancha!""")
st.markdown("""---""")

# DIMENSION 1: Ubicación
st.subheader("💼 Paso 1: Ubicación")
st.write('**¿En qué provincia quieres cazar?**')
provincias = 'BURGOS','SEGOVIA','SORIA','AVILA','LEON','VALLADOLID','PALENCIA','ZAMORA','SALAMANCA']
D1 = st.multiselect("", provincias, provincias)
