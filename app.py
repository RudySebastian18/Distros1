import streamlit as st
import json
import streamlit.components.v1 as components
from pyvis.network import Network

# Función para cargar los datos del archivo JSON
def cargar_datos_distros(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Título y descripción de la página
st.title("Cronología y Desarrollo de las Distribuciones Linux")
st.markdown("---")
st.markdown("Este proyecto es una página web dedicada a la **cronología y el desarrollo de las principales distribuciones de Linux**...")

# Cargar los datos
try:
    distros = cargar_datos_distros('distros.json')
except FileNotFoundError:
    st.error("No se encontró el archivo 'distros.json'. Asegúrate de que está en el mismo directorio.")
    distros = []

# ⏳ Sección de Cronología
st.header("⏳ Cronología Interactiva")
st.markdown("Un viaje visual a través del tiempo...")

if distros:
    distros_ordenadas = sorted(distros, key=lambda x: x['fecha_lanzamiento'])
    for distro in distros_ordenadas:
        with st.expander(f"**{distro['nombre']}** - ({distro['fecha_lanzamiento']})"):
            st.write(f"**Descripción:** {distro['descripcion']}")
            st.write(f"**Paquetería:** {distro['paqueteria']}")
            st.write(f"**Filosofía:** {distro['filosofia']}")
            if distro['basado_en']:
                st.write(f"**Basada en:** {distro['basado_en']}")
            if distro['ramas']:
                st.write(f"**Ramas derivadas:** {', '.join(distro['ramas'])}")

# 🌳 Sección de Árboles Genealógicos
st.markdown("---")
st.header("🌳 Árboles Genealógicos")
st.markdown("Descubre cómo las distribuciones están relacionadas...")

# **Aquí está el código corregido y funcional para el gráfico con Pyvis**
if distros:
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

    # Añadir nodos y aristas dinámicamente desde los datos JSON
    for distro in distros:
        net.add_node(distro['nombre'], title=distro['descripcion'], color="lightblue")
        if distro['basado_en']:
            # Asegúrate de que la distro base también esté como un nodo
            net.add_node(distro['basado_en'], color="orange") 
            net.add_edge(distro['basado_en'], distro['nombre'])

    # Guardar y mostrar el gráfico
    net.save_graph("grafo.html")
    with open("grafo.html", "r", encoding="utf-8") as html_file:
        source_code = html_file.read()
        components.html(source_code, height=750)

# ⚖️ Sección de Comparativas
st.markdown("---")
st.header("⚖️ Comparativas Detalladas")
st.markdown("Secciones dedicadas a las diferencias entre los grupos de distros más populares...")

distros_comparar = {
    "Debian": next((d for d in distros if d['nombre'] == 'Debian'), None),
    "Fedora": next((d for d in distros if d['nombre'] == 'Fedora'), None),
    "Arch Linux": next((d for d in distros if d['nombre'] == 'Arch Linux'), None)
}

if all(distros_comparar.values()):
    st.subheader("Comparación de Gestión de Paquetes")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Debian", value=distros_comparar['Debian']['paqueteria'])
    with col2:
        st.metric(label="Fedora", value="RPM")
    with col3:
        st.metric(label="Arch Linux", value=distros_comparar['Arch Linux']['paqueteria'])

# 📚 Sección de Introducción para Principiantes
st.markdown("---")
st.header("📚 Introducción para Principiantes")
st.markdown("Un área con información básica para aquellos que recién comienzan...")
st.write("¿Qué es una distribución de Linux? ¿Cuál es la mejor para empezar?")
st.info("Una distribución es una colección de software basada en el kernel de Linux...")
