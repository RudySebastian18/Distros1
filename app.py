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
                    title=f"<b>{distro['nombre']}</b><br>{distro['descripcion']}",  # Tooltip con descripción
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

    # Mostrar el grafo
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
import streamlit as st
import json
import streamlit.components.v1 as components
from pyvis.network import Network
import plotly.express as px
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image

# ===============================
# 📊 SECCIÓN: Gráficos estadísticos
# ===============================
st.markdown("---")
st.header("📊 Estadísticas de las Distribuciones")

if distros:
    df = pd.DataFrame(distros)

    # Conteo de derivadas
    df["num_ramas"] = df["ramas"].apply(lambda x: len(x) if x else 0)
    fig = px.bar(df, x="nombre", y="num_ramas", 
                 title="Cantidad de derivadas por distribución madre",
                 labels={"nombre":"Distribución", "num_ramas":"Número de derivadas"})
    st.plotly_chart(fig, use_container_width=True)

    # Pie chart de filosofías
    filosofias = df["filosofia"].value_counts()
    fig2 = px.pie(values=filosofias.values, names=filosofias.index, 
                  title="Distribución por filosofías")
    st.plotly_chart(fig2, use_container_width=True)

# ===============================
# 🎨 SECCIÓN: Galería de Logos
st.markdown("---")
st.header("🎨 Galería de Logos")

cols = st.columns(3)  # mostrar en 3 columnas
for i, distro in enumerate(distros):
    if "logo" in distro and distro["logo"]:
        try:
            with cols[i % 3]:
                img = Image.open(distro["logo"])
                img = img.resize((150, 150))  # 👈 todos iguales
                st.image(img, caption=distro["nombre"], use_container_width=False)
        except FileNotFoundError:
            st.warning(f"⚠️ No se encontró el logo para {distro['nombre']}")

# ===============================
# 🌐 SECCIÓN: Popularidad en el tiempo (ejemplo fake data)
# ===============================
st.markdown("---")
st.header("🌐 Popularidad en el tiempo")

# 🔹 Datos simulados (puedes reemplazar con dataset real)
data_popularidad = {
    "Año": [2018,2019,2020,2021,2022,2023],
    "Debian": [20,22,21,19,18,17],
    "Ubuntu": [40,38,37,35,34,32],
    "Arch Linux": [10,12,14,16,17,18],
    "Slackware": [8,7,6,5,4,3]
}
df_pop = pd.DataFrame(data_popularidad)
df_melt = df_pop.melt(id_vars="Año", var_name="Distro", value_name="Popularidad (%)")

fig3 = px.line(df_melt, x="Año", y="Popularidad (%)", color="Distro", markers=True,
               title="Popularidad relativa de algunas distribuciones")
st.plotly_chart(fig3, use_container_width=True)

# ===============================
# 🖥️ SECCIÓN: Recomendador interactivo
# ===============================
st.markdown("---")
st.header("🖥️ Recomendador de Distribuciones")

uso = st.radio("👉 ¿Para qué quieres la distro?", ["Escritorio", "Servidor"])
experiencia = st.radio("👉 ¿Nivel de experiencia?", ["Principiante", "Avanzado"])
filo = st.radio("👉 ¿Prefieres estabilidad o lo último?", ["Estabilidad", "Últimas novedades"])

if st.button("🔍 Recomiéndame una distro"):
    if uso == "Escritorio" and experiencia == "Principiante":
        st.success("✅ Te recomiendo **Ubuntu** o **Linux Mint**")
    elif uso == "Servidor" and filo == "Estabilidad":
        st.success("✅ Te recomiendo **Debian** o **CentOS/RHEL**")
    elif experiencia == "Avanzado" and filo == "Últimas novedades":
        st.success("✅ Te recomiendo **Arch Linux** o **Fedora**")
    else:
        st.success("✅ Una buena opción es **Debian**, balance entre estabilidad y soporte")

# ===============================
# 🌍 SECCIÓN: Mapa interactivo
# ===============================
st.markdown("---")
st.header("🌍 Origen de las Distribuciones")

# Coordenadas de ejemplo (puedes agregar más distros y coordenadas reales)
coords = {
    "Slackware": [39.7392, -104.9903],  # Denver, EE.UU.
    "Debian": [48.1351, 11.5820],       # Múnich, Alemania
    "Arch Linux": [45.5231, -122.6765], # Portland, EE.UU.
    "Ubuntu": [-25.7461, 28.1881]       # Sudáfrica
}

m = folium.Map(location=[20,0], zoom_start=2)

for distro, (lat, lon) in coords.items():
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{distro}</b>",
        tooltip=f"Origen: {distro}",
        icon=folium.Icon(color="blue", icon="linux", prefix="fa")
    ).add_to(m)

st_folium(m, width=800, height=500)

### Cambios realizados:

#1.  **Uso de `st.session_state`**: El gráfico de Pyvis se genera una sola vez y se almacena en `st.session_state`. Esto evita que el código se ejecute repetidamente y cause errores. La línea `if 'grafo_html' not in st.session_state:` asegura que el gráfico solo se cree la primera vez que se carga la página.
#2.  **`net.generate_html()` en lugar de `net.save_graph()`**: Esta función crea el código HTML directamente en la memoria, sin necesidad de guardar un archivo. Es la forma recomendada para integrar Pyvis con Streamlit.
#3.  **Refactorización de la carga de datos**: Aunque tu función estaba bien, he movido el código de carga del archivo `distros.json` al bloque principal para simplificar.

#Con este código, el gráfico de Pyvis debería cargarse sin problemas y la aplicación será más estable.
