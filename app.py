import streamlit as st
import json
from pyvis.network import Network
import streamlit.components.v1 as components
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
    distros = [] # Si no se encuentra, la lista está vacía

# ⏳ Sección de Cronología
st.header("⏳ Cronología Interactiva")
st.markdown("Un viaje visual a través del tiempo...")

if distros:
    # Ordenar las distros por fecha de lanzamiento
    distros_ordenadas = sorted(distros, key=lambda x: x['fecha_lanzamiento'])
    
    # Mostrar la cronología en un formato de expansión para no saturar la pantalla
    for distro in distros_ordenadas:
        with st.expander(f"**{distro['nombre']}** - ({distro['fecha_lanzamiento']})"):
            st.write(f"**Descripción:** {distro['descripcion']}")
            st.write(f"**Paquetería:** {distro['paqueteria']}")
            st.write(f"**Filosofía:** {distro['filosofia']}")
            if distro['basado_en']:
                st.write(f"**Basada en:** {distro['basado_en']}")
            if distro['ramas']:
                st.write(f"**Ramas derivadas:** {', '.join(distro['ramas'])}")

# 🌳 Sección de Árboles Genealógicos (simulado)
st.markdown("---")
st.header("🌳 Árboles Genealógicos")
st.markdown("Descubre cómo las distribuciones están relacionadas...")
# En la sección de "Árboles Genealógicos"
net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
net.add_node("Debian", title="Debian GNU/Linux", color="orange")
net.add_node("Ubuntu", title="Basado en Debian", color="red")
net.add_node("Linux Mint", title="Basado en Ubuntu", color="green")
net.add_edge("Debian", "Ubuntu")
net.add_edge("Ubuntu", "Linux Mint")
# Guarda el gráfico como un archivo HTML temporal
net.save_graph("grafo.html")
# Muestra el gráfico en Streamlit
st.subheader("Visualización con Pyvis")
with open("grafo.html", "r", encoding="utf-8") as html_file:
    source_code = html_file.read()
    components.html(source_code, height=750)

# Este es un ejemplo simplificado de un gráfico. Para uno real, necesitarías librerías como `pyvis` o `graphviz`
if distros:
    st.subheader("Relación entre Debian y Ubuntu")
    st.write("Debian (1993) -> Ubuntu (2004) -> Linux Mint (2006)")
    st.info("Para un gráfico interactivo, se necesitarían librerías de visualización de grafos.")

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
        st.metric(label="Fedora", value="RPM") # No está en el JSON, se añade manualmente
    with col3:
        st.metric(label="Arch Linux", value=distros_comparar['Arch Linux']['paqueteria'])

# 📚 Sección de Introducción para Principiantes
st.markdown("---")
st.header("📚 Introducción para Principiantes")
st.markdown("Un área con información básica para aquellos que recién comienzan...")
st.write("¿Qué es una distribución de Linux? ¿Cuál es la mejor para empezar?")
st.info("Una distribución es una colección de software basada en el kernel de Linux...")
