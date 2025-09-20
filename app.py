import streamlit as st
import json
import streamlit.components.v1 as components
from pyvis.network import Network

# Título y descripción de la página
st.set_page_config(layout="wide") # Opcional: para usar todo el ancho de la pantalla
st.title("Cronología y Desarrollo de las Distribuciones Linux")
st.markdown("---")
st.markdown("Este proyecto es una página web dedicada a la **cronología y el desarrollo de las principales distribuciones de Linux**...")

# Cargar los datos
try:
    with open('distros.json', 'r', encoding='utf-8') as f:
        distros = json.load(f)
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

#---

# 🌳 Sección de Árboles Genealógicos
st.header("🌳 Árboles Genealógicos")
st.markdown("Descubre cómo las distribuciones están relacionadas...")

if distros:
    if 'grafo_html' not in st.session_state:
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

    nodos_existentes = set() 
    for distro in distros:
        if distro['nombre'] not in nodos_existentes:
            net.add_node(
                distro['nombre'], 
                title=f"<b>{distro['nombre']}</b><br>{distro['descripcion']}", 
                color="lightblue"
            )
            nodos_existentes.add(distro['nombre'])

        if distro['basado_en']:
            if distro['basado_en'] not in nodos_existentes:
                net.add_node(
                    distro['basado_en'], 
                    title=f"<b>{distro['basado_en']}</b>", 
                    color="orange"
                )
                nodos_existentes.add(distro['basado_en'])
            net.add_edge(distro['basado_en'], distro['nombre'])
    
    st.session_state.grafo_html = net.generate_html()


    components.html(st.session_state.grafo_html, height=750)

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

#---

# En la sección de principiantes
st.header("📚 Guía para principiantes: ¿Cuál elegir?")
principiantes_distros = [d for d in distros if d.get('publico_objetivo') == 'Principiantes']

if principiantes_distros:
    opcion = st.selectbox(
        "Selecciona una distribución para saber más:",
        options=[d['nombre'] for d in principiantes_distros]
    )
    
    distro_elegida = next((d for d in principiantes_distros if d['nombre'] == opcion), None)
    if distro_elegida:
        st.subheader(f"✅ {distro_elegida['nombre']}")
        st.write(f"**Descripción:** {distro_elegida['descripcion']}")
        st.write(f"**Paquetería:** {distro_elegida['paqueteria']}")
        st.write(f"**Filosofía:** {distro_elegida['filosofia']}")

#---

### Cambios realizados:

#1.  **Uso de `st.session_state`**: El gráfico de Pyvis se genera una sola vez y se almacena en `st.session_state`. Esto evita que el código se ejecute repetidamente y cause errores. La línea `if 'grafo_html' not in st.session_state:` asegura que el gráfico solo se cree la primera vez que se carga la página.
#2.  **`net.generate_html()` en lugar de `net.save_graph()`**: Esta función crea el código HTML directamente en la memoria, sin necesidad de guardar un archivo. Es la forma recomendada para integrar Pyvis con Streamlit.
#3.  **Refactorización de la carga de datos**: Aunque tu función estaba bien, he movido el código de carga del archivo `distros.json` al bloque principal para simplificar.

#Con este código, el gráfico de Pyvis debería cargarse sin problemas y la aplicación será más estable.
