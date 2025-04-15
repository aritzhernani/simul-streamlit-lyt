# Importación de librerías
import streamlit as st
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from contextlib import contextmanager
import os
import time
import random

# Configuración de la aplicación
st.set_page_config(page_title='Simulación', layout='centered', initial_sidebar_state='collapsed')


# The custom HTML for hiding elements and styling buttons horizontally
HORIZONTAL_STYLE = """
<style class="hide-element">
    /* Hides the style container and removes the extra spacing */
    .element-container:has(.hide-element) {
        display: none;
    }
    /*
        The selector for >.element-container is necessary to avoid selecting the whole
        body of the streamlit app, which is also a stVerticalBlock.
    */
    div[data-testid="stVerticalBlock"]:has(> .element-container .horizontal-marker) {
        display: flex;
        flex-direction: row !important;
        flex-wrap: wrap;
        gap: 0.5rem;
        align-items: baseline;
    }
    /* Buttons and their parent container all have a width of 704px, which we need to override */
    div[data-testid="stVerticalBlock"]:has(> .element-container .horizontal-marker) div {
        width: max-content !important;
    }
    /* Just an example of how you would style buttons, if desired */
    /*
    div[data-testid="stVerticalBlock"]:has(> .element-container .horizontal-marker) button {
        border-color: red;
    }
    */
</style>
"""

# Context manager for horizontally aligned buttons
@contextmanager
def st_horizontal():
    st.markdown(HORIZONTAL_STYLE, unsafe_allow_html=True)
    with st.container():
        st.markdown('<span class="hide-element horizontal-marker"></span>', unsafe_allow_html=True)
        yield

# Título de la aplicación
st.title('')
st.markdown('')
st.write('')

tab1, tab2, tab3 = st.tabs(["Usuarios", "% Partners", "Datos demográficos y análisis de impacto"])#, "Simulación de escenarios"])

##### Usuarios
with tab1:
    st.sidebar.title('Arquetipos')
    st.sidebar.markdown('## Usuarios')
    # st.write('En esta sección detallamos y elegimos los gastos mensuales categorizados para cada arquetipo.')
    # Write a message in Spansh explaining that this tab is for defining the monthly expenses for each archetype for each expense category.
    #st.write('Selecciona los importes medios de cada categoría de gasto para cada arquetipo. Estos importes se utilizarán para calcular el cashback mensual estimado por fan y por arquetipo. Puedes modificar los valores por defecto para adaptarlos a tu caso específico.')
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2a2a40, #1e1e2f);
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
    ">
        <p style="margin: 0; font-size: 14px; color: #f0f0f0;">
            Selecciona los importes medios de cada categoría de gasto por cada usuario y graba los datos introducidos.
            Estos importes se utilizarán para calcular el <strong style="color: #f5c542;">cashback mensual estimado</strong> por fan y tipo de usuario.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Valores generales de las categorías (v1)
    #CATEGORIAS_RANGO = {
    #    "Alimentación y bebidas no alcohólicas": (0, 1000),
    #    "Transporte (gasolina, coche)": (0, 500),
    #    "Suministros: electricidad, gas": (0, 2000),
    #    "Sanidad (Seguros médicos)": (0, 500),
    #    "Restaurantes, ocio y cultura": (0, 500),
    #    "Ropa y calzado": (0, 500),
    #    "Educación (colegios, actividades)": (0, 1000),
    #    "Deporte y bienestar (gimnasio, clubs)": (0, 300),
    #    "Tecnología y telecomunicaciones": (0, 300),
    #    "Otros bienes y servicios": (0, 300),
    #    "Abono (deportivo)": (0, 100),
    #    "Merchandising y compras esporádicas": (0, 100)
    #}

    # Valores generales de las categorías (v2): Alimentación, Combustible, Salud, Ocio, Otros seguros, Automoción, Suministros/Luz, Telco/Tech, Centros deportivos, Otros
    CATEGORIAS_RANGO = {
        "Alimentación": (0, 1000),
        "Combustible": (0, 500),
        "Salud": (0, 500),
        "Ocio": (0, 500),
        "Otros seguros": (0, 500),
        "Automoción": (0, 500),
        "Suministros/Luz": (0, 2000),
        "Telco/Tech": (0, 300),
        "Centros deportivos": (0, 300),
        "Otros": (0, 300)
    }


    # Valores mínimos y máximos por arquetipo
    #ARQUETIPOS_ORIGINALES = {
    #    "Fan casual (joven adulto)": {
    #        "Alimentación y bebidas no alcohólicas": (150, 250),
    #        "Transporte (gasolina, coche)": (20, 50),
    #        "Suministros: electricidad, gas": (0, 50),
    #        "Sanidad (Seguros médicos)": (0, 0),
    #        "Restaurantes, ocio y cultura": (100, 150),
    #
    #        "Ropa y calzado": (10, 50),
    #        "Educación (colegios, actividades)": (0, 0),
    #        "Deporte y bienestar (gimnasio, clubs)": (25, 60),
    #        "Tecnología y telecomunicaciones": (10, 30),
    #        "Otros bienes y servicios": (20, 80),
    #        "Abono (deportivo)": (0, 0),
    #        "Merchandising y compras esporádicas": (0, 0)
    #    },
    #    "Adulto profesional soltero": {
    #        "Alimentación y bebidas no alcohólicas": (200, 300),
    #        "Transporte (gasolina, coche)": (50, 100),
    #        "Suministros: electricidad, gas": (0, 100),
    #        "Sanidad (Seguros médicos)": (0, 50),
    #        "Restaurantes, ocio y cultura": (150, 200),
    #
    #        "Ropa y calzado": (50, 100),
    #        "Educación (colegios, actividades)": (0, 0),
    #        "Deporte y bienestar (gimnasio, clubs)": (30, 60),
    #        "Tecnología y telecomunicaciones": (20, 40),
    #        "Otros bienes y servicios": (50, 100),
    #        "Abono (deportivo)": (0, 80),
    #        "Merchandising y compras esporádicas": (0, 20)
    #    },
    #    "Familia de clase media con dos hijos": {
    #        "Alimentación y bebidas no alcohólicas": (500, 600),
    #        "Transporte (gasolina, coche)": (100, 200),
    #        "Suministros: electricidad, gas": (0, 200),
    #        "Sanidad (Seguros médicos)": (0, 80),
    #        "Restaurantes, ocio y cultura": (200, 300),
    #
    #        "Ropa y calzado": (100, 200),
    #        "Educación (colegios, actividades)": (300, 400),
    #        "Deporte y bienestar (gimnasio, clubs)": (50, 100),
    #        "Tecnología y telecomunicaciones": (30, 60),
    #        "Otros bienes y servicios": (50, 150),
    #        "Abono (deportivo)": (0, 0),
    #        "Merchandising y compras esporádicas": (0, 20),
    #    },
    #    "Pareja de jubilados": {
    #        "Alimentación y bebidas no alcohólicas": (300, 400),
    #        "Transporte (gasolina, coche)": (0, 50),
    #        "Suministros: electricidad, gas": (0, 150),
    #        "Sanidad (Seguros médicos)": (50, 120),
    #        "Restaurantes, ocio y cultura": (50, 100),
    #        
    #        "Ropa y calzado": (20, 50),
    #        "Educación (colegios, actividades)": (0, 0),
    #        "Deporte y bienestar (gimnasio, clubs)": (25, 50),
    #        "Tecnología y telecomunicaciones": (20, 40),
    #        "Otros bienes y servicios": (50, 150),
    #        "Abono (deportivo)": (0, 0),
    #        "Merchandising y compras esporádicas": (0, 20)
    #    }
    #}

    # Valores mínimos y máximos por arquetipo
    ARQUETIPOS_ORIGINALES = {
        "Fan casual (joven adulto)": {
            "Alimentación": (150, 250),
            "Combustible": (20, 50),
            "Suministros/Luz": (0, 0),
            "Salud": (0, 0),
            "Ocio": (0, 50),
            "Otros seguros": (0, 0),
            "Telco/Tech": (10, 30),
            "Automoción": (0, 0),
            "Centros deportivos": (20, 40),
            "Otros": (20, 50)
        },
        "Adulto profesional soltero": {
            "Alimentación": (200, 300),
            "Combustible": (50, 150),
            "Suministros/Luz": (0, 0),
            "Salud": (0, 50),
            "Ocio": (0, 200),
            "Otros seguros": (0, 0),
            "Telco/Tech": (20, 40),
            "Automoción": (0, 0),
            "Centros deportivos": (0, 100),
            "Otros": (50, 100)
        },
        "Familia de clase media con dos hijos": {
            "Alimentación": (400, 600),
            "Combustible": (50, 200),
            "Suministros/Luz": (0, 150),
            "Salud": (0, 250),
            "Ocio": (0, 150),
            "Otros seguros": (0, 100),
            "Telco/Tech": (20, 40),
            "Automoción": (0, 0),
            "Centros deportivos": (0, 100),
            "Otros": (50, 100)
        },
        "Pareja de jubilados": {
            "Alimentación": (200, 300),
            "Combustible": (0, 0),
            "Suministros/Luz": (0, 50),
            "Salud": (0, 200),
            "Ocio": (0, 0),
            "Otros seguros": (0, 100),
            "Telco/Tech": (0, 0),
            "Automoción": (0, 0),
            "Centros deportivos": (0, 0),
            "Otros": (0, 0)
        }
    }

    # Inicializar session_state
    if "arquetipo_seleccionado" not in st.session_state:
        st.session_state.arquetipo_seleccionado = None

    if "valores_modificados" not in st.session_state:
        st.session_state.valores_modificados = {}

    if "valores_actuales" not in st.session_state:
        st.session_state.valores_actuales = {}

    # Función para obtener valores (modificados o originales)
    def obtener_valores(arquetipo):
        if arquetipo in st.session_state.valores_modificados:
            return st.session_state.valores_modificados[arquetipo]
        return ARQUETIPOS_ORIGINALES[arquetipo].copy()


    ###########
    cols = st.columns(4)
    for idx, arquetipo in enumerate(ARQUETIPOS_ORIGINALES.keys()):
        with cols[idx % 4]:
            if st.button(arquetipo, key=f"btn_{idx}"):
                st.session_state.arquetipo_seleccionado = arquetipo
                st.session_state.valores_actuales = obtener_valores(arquetipo)
                st.rerun()

    # Mostrar controles si hay arquetipo seleccionado
    arquetipo = st.session_state.arquetipo_seleccionado
    #st.write(f"Arquetipo seleccionado: **{arquetipo}**")
    
    # Sliders con valores actuales
    # nuevos_valores = {}
    # for categoria, (min_val, max_val) in CATEGORIAS_RANGO.items():
    #    valor_actual = st.session_state.valores_actuales.get(categoria, (min_val, max_val))
    #    
    #    # Asegurar que es una tupla
    #    if isinstance(valor_actual, int):
    #        valor_actual = (valor_actual, valor_actual)
        
        #nuevos_valores[categoria] = st.slider(
        #    f"{categoria}",
        #    min_value=min_val,
        #    max_value=max_val,
        #    value=valor_actual,
        #    key=f"slider_{arquetipo}_{categoria}"
        #)

    if arquetipo:
        nuevos_valores = {}  # Inicialización de la variable fuera de cualquier condicional
        categorias = list(CATEGORIAS_RANGO.items())

        for i in range(0, len(categorias), 2):
            col1, col2 = st.columns(2)

            # Primer input
            categoria1, (min_val1, max_val1) = categorias[i]
            valor_actual1 = st.session_state.valores_actuales.get(categoria1, (min_val1, max_val1))
            value1 = valor_actual1[1] if isinstance(valor_actual1, tuple) else valor_actual1

            with col1:
                nuevos_valores[categoria1] = st.number_input(
                    f"{categoria1} (€)", 
                    min_value=min_val1,
                    max_value=max_val1,
                    value=value1,
                    step=1,
                    format="%d",
                    key=f"input_{arquetipo}_{categoria1}_{i}_col1"
                )

            # Segundo input (si existe)
            if i + 1 < len(categorias):
                categoria2, (min_val2, max_val2) = categorias[i + 1]
                valor_actual2 = st.session_state.valores_actuales.get(categoria2, (min_val2, max_val2))
                value2 = valor_actual2[1] if isinstance(valor_actual2, tuple) else valor_actual2

                with col2:
                    nuevos_valores[categoria2] = st.number_input(
                        f"{categoria2} (€)",
                        min_value=min_val2,
                        max_value=max_val2,
                        value=value2,
                        step=1,
                        format="%d",
                        key=f"input_{arquetipo}_{categoria2}_{i}_col2"
                    )

        # Ahora, solo asigna nuevos_valores a session_state después de llenarlo
        st.session_state.valores_actuales = nuevos_valores

        ### NEW BUTTONS
        button_list_usuarios = ['Guardar cambios', 'Restablecer original']

        # Button logic
        with st_horizontal():
            buttons = {}
            for button_text in button_list_usuarios:
                # Store button states in a dictionary
                buttons[button_text] = st.button(button_text)

        if buttons['Guardar cambios']:
            st.session_state.valores_modificados[arquetipo] = nuevos_valores
            st.success("Cambios guardados para este arquetipo!")

        if buttons['Restablecer original']:
            st.session_state.valores_actuales = ARQUETIPOS_ORIGINALES[arquetipo].copy()
            if arquetipo in st.session_state.valores_modificados:
                del st.session_state.valores_modificados[arquetipo]
            st.rerun()

        # Botones de acción
        #if st.button("Guardar cambios"):
        #    st.session_state.valores_modificados[arquetipo] = nuevos_valores
        #    st.info("Cambios guardados para este arquetipo!")

        #if st.button("Restablecer original"):
        #    st.session_state.valores_actuales = ARQUETIPOS_ORIGINALES[arquetipo].copy()
        #    if arquetipo in st.session_state.valores_modificados:
        #        del st.session_state.valores_modificados[arquetipo]
        #    st.rerun()

#### Cálculo de porcentajes
with tab2:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2a2a40, #1e1e2f);
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
    ">
        <p style="margin: 0; font-size: 14px; color: #f0f0f0;">
            Puedes editar la distribución de los porcentajes del total de ingresos que se derivarán al 
            <span style="color: #f5c542;">club</span>, a los <span style="color: #f5c542;">fans</span>, 
            y a los <span style="color: #f5c542;">proveedores del sistema de fidelización</span>. <br>
            También es posible editar los <span style="color: #f5c542;">% de comisión</span> por cada categoría que serán derivados 
            a los usuarios por cada transacción.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Distribución de comisiones"):
        def recalculate_weights(changed_weight, other_weight1, other_weight2):
            total = changed_weight + other_weight1 + other_weight2
            if total != 0:
                scale = 1 / total
                return changed_weight * scale, other_weight1 * scale, other_weight2 * scale
            return changed_weight, other_weight1, other_weight2

        col1, col2, col3 = st.columns(3)

        if 'club_weight' not in st.session_state:
            st.session_state['club_weight'] = 0.3
        if 'user_weight' not in st.session_state:
            st.session_state['user_weight'] = 0.5

        if 'proveedores_weight' not in st.session_state:
            st.session_state['proveedores_weight'] = 0.2

        with col1:
            club_weight = st.slider("Club", 0.0, 1.0, st.session_state['club_weight'], step=0.01)
        with col2:
            user_weight = st.slider("Fan", 0.0, 1.0, st.session_state['user_weight'], step=0.01)
        with col3:
            proveedores_weight = st.slider("Proveedores", 0.0, 1.0, st.session_state['proveedores_weight'], step=0.01)

        total_weight = club_weight + user_weight + proveedores_weight

        # Add a button for forcing the recalculation
        if total_weight != 1:
            # show message
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2a2a40, #1e1e2f);
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
            ">
                <p style="margin: 0; font-size: 14px; color: #f0f0f0;">
                    La suma de los pesos es <strong style="color: #f5c542;">{total_weight:.2f}</strong>.
                    Debe ser igual a <strong style="color: #f5c542;">1.0</strong> para que la distribución sea correcta.
                </p>
                <p style="margin: 0; font-size: 14px; color: #f0f0f0;">
                    Puedes ajustar los pesos y hacer clic en <strong style="color: #f5c542;">"Recalcular"</strong> para
                    normalizar automáticamente los pesos.
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Recalcular"):
                # Recalculate weights
                club_weight, user_weight, proveedores_weight = recalculate_weights(club_weight, user_weight, proveedores_weight)
                st.session_state['club_weight'] = club_weight
                st.session_state['user_weight'] = user_weight
                st.session_state['proveedores_weight'] = proveedores_weight

        # Add a button for resetting to default values
        if st.button("Restablecer valores por defecto"):
            # Reset to default values
            st.session_state['club_weight'] = 0.1
            st.session_state['user_weight'] = 0.6
            st.session_state['proveedores_weight'] = 0.3

    # Expander para editar las comisiones por categoría
    with st.expander("Comisión base por categoría"):
        categorias = [
            "Alimentación",
            "Combustible",
            "Suministros/Luz",
            "Salud",
            "Ocio",
            "Otros seguros",
            "Telco/Tech",
            "Automoción",
            "Centros deportivos",
            "Otros"
        ]

        base_df = pd.DataFrame({
            "Categoría": categorias,
            "Porc. base (%)": [1.5] * len(categorias)
        })

        # I want the following base percentage for each category: Alimentación: 1.5%, Combustible: 1.5%, Suministros/Luz: 1.5%, Salud: 4%, Ocio: 3%, Otros seguros: 3.5%, Telco/Tech: 3%, Automoción: 5%, Centros deportivos: 3%, Otros: 3%
        base_df.loc[base_df["Categoría"] == "Alimentación", "Porc. base (%)"] = 1.5
        base_df.loc[base_df["Categoría"] == "Combustible", "Porc. base (%)"] = 1.5
        base_df.loc[base_df["Categoría"] == "Suministros/Luz", "Porc. base (%)"] = 1.5
        base_df.loc[base_df["Categoría"] == "Salud", "Porc. base (%)"] = 4.0
        base_df.loc[base_df["Categoría"] == "Ocio", "Porc. base (%)"] = 3.0
        base_df.loc[base_df["Categoría"] == "Otros seguros", "Porc. base (%)"] = 3.5
        base_df.loc[base_df["Categoría"] == "Telco/Tech", "Porc. base (%)"] = 3.0
        base_df.loc[base_df["Categoría"] == "Automoción", "Porc. base (%)"] = 5.0
        base_df.loc[base_df["Categoría"] == "Centros deportivos", "Porc. base (%)"] = 3.0
        base_df.loc[base_df["Categoría"] == "Otros", "Porc. base (%)"] = 3.0


        num_columns = 2
        columns = st.columns(num_columns)

        for index, row in base_df.iterrows():
            col = columns[index % num_columns]
            with col:
                base_df.at[index, "Porc. base (%)"] = st.number_input(
                    f"{row['Categoría']}",
                    min_value=0.0,
                    max_value=10.0,
                    value=row["Porc. base (%)"],
                    step=0.1,
                    format="%.2f",
                    key=f"input_{index}"
                )

        # Calcula el porcentaje avg
        base_df["Porc. avg (%)"] = base_df["Porc. base (%)"].mean()
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2a2a40, #1e1e2f);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
        ">
            <p style="margin: 0; font-size: 14px; color: #f0f0f0;">
                ℹ️ El porcentaje base por categoría es el promedio de los porcentajes
                de cada categoría: <strong style="color: #f5c542;">{base_df["Porc. base (%)"].mean():.2f}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
     
#### Datos demográficos y Análisis de Impacto
with tab3:
    
    with st.expander("Distribución de población por arquetipos"):
        #st.subheader("Distribución de población por arquetipos")
        
        # Set city poblation in input
        city_population = st.number_input("Población de la ciudad/región", min_value=0, max_value=1000000000, value=250000)
        
        # Create columns, one for each archetype
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("Selecciona la población de cada arquetipo en la ciudad/región.")
        col1, col2 = st.columns(2)
        
        with col1:
            arquetipos_ciudad = {
                "Fan casual (joven adulto)": st.number_input("Fan casual (18-30 años)", min_value=0, max_value=100000, value=30000),
                "Adulto profesional soltero": st.number_input("Adulto profesional soltero", min_value=0, max_value=100000, value=70151)
            }
        
        with col2:
            arquetipos_ciudad.update({
                "Familia de clase media con dos hijos": st.number_input("Familia (padres + niños)", min_value=0, max_value=100000, value=22800),
                "Pareja de jubilados": st.number_input("Pareja de jubilados (65+)", min_value=0, max_value=100000, value=29100)
            })
                
        total_poblacion = sum(arquetipos_ciudad.values())
        porcentaje = total_poblacion / city_population * 100
        st.markdown("<br>", unsafe_allow_html=True)


        ## Create columns: one for "0%", one for the progress bar, one for "100%"
        #col1, col2, col3 = st.columns([1, 10, 1])
        #with col1:
        #    st.markdown(f"""<p style="text-align: center;font-size: 14px;">0%</p>""", unsafe_allow_html=True)
        #with col2:
        #    st.progress(int(porcentaje) / 100)
        #with col3:
        #    st.markdown(f"""<p style="text-align: center;font-size: 14px;">100%</p>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2a2a40, #1e1e2f);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
        ">
            <p style="margin: 0; font-size: 14px; color: #f0f0f0;">
                ℹ️ Estos arquetipos representan <strong style="color: #f5c542;">{total_poblacion:,} habitantes</strong> 
                (<strong style="color: #f5c542;">{porcentaje:.1f}%</strong>) de la población base de 
                <strong style="color: #f5c542;">{city_population:,} habitantes</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Base social inicial"):
        base_social = st.number_input("Base social", min_value=0, max_value=1000000000, value=40000)
        # base_social = 40000
        porcentaje_bs = base_social / 250000 * 100
        porcentaje_sc = base_social / total_poblacion * 100
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2a2a40, #1e1e2f);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
        ">
            <p style="margin: 0; font-size: 14px; color: #f0f0f0;">
                ℹ️ Base social inicial de <strong style="color: #f5c542;">{base_social:,} fans</strong>
                (<strong style="color: #f5c542;">{porcentaje_bs:.1f}%</strong> de la población total de
                <strong style="color: #f5c542;">{city_population:,} habitantes</strong>) y 
                <strong style="color: #f5c542;">{porcentaje_sc:.1f}%</strong> de la población objetivo/arquetipos de
                <strong style="color: #f5c542;">{total_poblacion:,} habitantes</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Add a line break after the box
        st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Participación de los arquetipos"):
        # ⬅️ Este bloque va antes de cualquier widget relacionado con los sliders
        if "reset" not in st.session_state:
            st.session_state.reset = False

        if st.session_state.reset:
            st.session_state.slider_fan_casual = 15
            st.session_state.slider_profesional = 15
            st.session_state.slider_familia = 15
            st.session_state.slider_jubilados = 15

            st.session_state.participacion_arquetipos = {
                "Fan casual (joven adulto)": 15,
                "Adulto profesional soltero": 15,
                "Familia de clase media con dos hijos": 15,
                "Pareja de jubilados": 15
            }

            st.session_state.participacion_merchants = 90

            st.session_state.reset = False
            st.rerun()

        st.write("Selecciona el porcentaje de participación de cada arquetipo")

        # Inicialización del estado
        if "participacion_arquetipos" not in st.session_state:
            st.session_state.participacion_arquetipos = {
                "Fan casual (joven adulto)": 15,
                "Adulto profesional soltero": 15,
                "Familia de clase media con dos hijos": 15,
                "Pareja de jubilados": 15
            }

        if "slider_fan_casual" not in st.session_state:
            st.session_state.slider_fan_casual = 15
        if "slider_profesional" not in st.session_state:
            st.session_state.slider_profesional = 15
        if "slider_familia" not in st.session_state:
            st.session_state.slider_familia = 15
        if "slider_jubilados" not in st.session_state:
            st.session_state.slider_jubilados = 15

        # Sliders individuales para cada arquetipo
        st.session_state.participacion_arquetipos["Fan casual (joven adulto)"] = st.slider(
            "% Fan casuales activos: ", 0, 100,
            key="slider_fan_casual",
            format="%d%%"
        )

        st.session_state.participacion_arquetipos["Adulto profesional soltero"] = st.slider(
            "% Profesionales solteros activos: ", 0, 100,
            key="slider_profesional",
            format="%d%%"
        )

        st.session_state.participacion_arquetipos["Familia de clase media con dos hijos"] = st.slider(
            "% Familias activas: ", 0, 100,
            key="slider_familia",
            format="%d%%"
        )

        st.session_state.participacion_arquetipos["Pareja de jubilados"] = st.slider(
            "% Jubilados activos: ", 0, 100,
            key="slider_jubilados",
            format="%d%%"
        )

        participacion_arquetipos = st.session_state.participacion_arquetipos

        # Calculamos el número de fans por arquetipo.
        fans_casual = arquetipos_ciudad["Fan casual (joven adulto)"] * participacion_arquetipos["Fan casual (joven adulto)"] / 100
        adultos_profesionales = arquetipos_ciudad["Adulto profesional soltero"] * participacion_arquetipos["Adulto profesional soltero"] / 100
        familias = arquetipos_ciudad["Familia de clase media con dos hijos"] * participacion_arquetipos["Familia de clase media con dos hijos"] / 100
        jubilados = arquetipos_ciudad["Pareja de jubilados"] * participacion_arquetipos["Pareja de jubilados"] / 100
        total_participacion = fans_casual + adultos_profesionales + familias + jubilados

        # store in new dict
        participacion_arquetipos_sum = {}
        participacion_arquetipos_sum["Fan casual (joven adulto)"] = fans_casual
        participacion_arquetipos_sum["Adulto profesional soltero"] = adultos_profesionales
        participacion_arquetipos_sum["Familia de clase media con dos hijos"] = familias
        participacion_arquetipos_sum["Pareja de jubilados"] = jubilados

        
        st.markdown("<br>", unsafe_allow_html=True)
        #st.progress(int(total_participacion)/total_poblacion)

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2a2a40, #1e1e2f);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
        ">
            <p style="margin: 0; font-size: 14px; color: #f0f0f0;">
                ℹ️ La selección suma un total de <strong style="color: #f5c542;">{total_participacion:,.0f} fans</strong>
                (<strong style="color: #f5c542;">{total_participacion / total_poblacion * 100:.1f}%</strong>) de la población objetivo/arquetipos de
                <strong style="color: #f5c542;">{total_poblacion:,} habitantes</strong>.
                <br>Esto representa un total de <strong style="color: #f5c542;">{total_participacion / city_population * 100:.1f}%</strong> de la población total de
                <strong style="color: #f5c542;">{city_population:,} habitantes</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Input "aumento % por año"
        # Porcentaje de aumento de fans por año
        st.session_state.aumento_fans = st.number_input("Aumento % por año", min_value=0, max_value=100, value=10)
        aumento_fans = st.session_state.aumento_fans

        # Show 3-year projection in number of fans. Calculate.
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2a2a40, #1e1e2f);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
        ">
            <p style="margin: 0; font-size: 14px; color: #f0f0f0;">
                ℹ️ Proyección de aumento de fans por año: <strong style="color: #f5c542;">{aumento_fans}%.</strong>
                Proyección de aumento de fans en 3 años: <strong style="color: #f5c542;">{total_participacion * (1 + aumento_fans / 100) ** 3:,.0f} fans.</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


        # Estimación de cuántos nuevos fans deberiamos captar al mes en 3 meses, 6 meses y 1 año para llegar a total_poblacion
        #meses = [3, 6, 12]
        #estimaciones = []
        #for mes in meses:
        #    nuevos_fans = (total_poblacion - total_participacion) / mes
        #    estimaciones.append(nuevos_fans)
        #    st.markdown(f"""
        #    <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
        #    <p style="margin:0;font-size:14px;">ℹ️ Para alcanzar la población total de 250,000 habitantes,
        #    deberíamos captar <strong>{nuevos_fans:,.0f} nuevos fans</strong> al mes durante {mes} meses.</p>
        #    </div>
        #    """, unsafe_allow_html=True)

    with st.expander("Margen de error previsiones de recurrencia/gasto sobre partners del programa"):
        # Slider para participación de merchants (agrupados, avg)
        st.session_state.participacion_merchants = st.slider("", 1, 100, 90)
        participacion_merchants = st.session_state.participacion_merchants

        # Alert box styled with yellow background for the warning
        st.markdown(f"""
        <div style="
            background-color: #f5c542; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
        ">
            <p style="margin: 0; font-size: 14px; color: #31333f;">
                Esto refiere al margen de error de las transacciones que pueden no ser contabilizadas por los merchants en el programa de cashback.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


    # The list of buttons
    button_list = ['Calcular', 'Reiniciar', 'Exportar']

    # Button logic
    with st_horizontal():
        buttons = {}
        for button_text in button_list:
            # Store button states in a dictionary
            buttons[button_text] = st.button(button_text)
        

    # Execute button 'Calcular'
    if buttons['Calcular']:
        st.markdown("<br>", unsafe_allow_html=True)

        # Generata a random (1-10 secs) delay for charging the content (loading)
        with st.spinner("Calculando..."):
            time.sleep(random.randint(1, 1))



        # Mostrar mensaje de carga
        # Cálculo de beneficios usando gastos de arquetipos
        users_por_arquetipo = {
            k: arquetipos_ciudad[k] * v / 100
            for k, v in participacion_arquetipos.items()
        }
        total_users = sum(users_por_arquetipo.values())
        
        # Obtener gastos por categoría de cada arquetipo
        gastos_por_arquetipo = {
            arquetipo: {
                categoria: (min_val, max_val)
                for categoria, (min_val, max_val) in ARQUETIPOS_ORIGINALES[arquetipo].items()
            }
            for arquetipo in ARQUETIPOS_ORIGINALES
        }
            
        # Calcular cashback total
        cashback_total = 0
        detalle_cashback = []

        for arquetipo, num_users in users_por_arquetipo.items():
            if arquetipo in ARQUETIPOS_ORIGINALES:
                for _, comision_row in base_df.iterrows():
                    categoria_pest1 = comision_row["Categoría"]
                    if categoria_pest1 and categoria_pest1 in gastos_por_arquetipo[arquetipo]:
                        gasto_min, gasto_max = gastos_por_arquetipo[arquetipo][categoria_pest1]
                        gasto_promedio = (gasto_min + gasto_max) / 2
                        comision = comision_row["Porc. base (%)"] / 100
                        cashback_arquetipo = num_users * gasto_promedio * comision
                        cashback_total += cashback_arquetipo

                        detalle_cashback.append({
                            "Arquetipo": arquetipo,
                            "Categoría": comision_row["Categoría"],
                            "Fans": num_users,
                            "Gasto promedio": f"{gasto_promedio:,.2f}€",
                            "Participación merchants (%)": f"{participacion_merchants:.2f}%",
                            "Comisión Total (%)": f"{comision_row['Porc. base (%)']:.2f}%",
                            "Comisión Club (%)": f"{club_weight * 100:.2f}%",
                            "Comisión Proveedores (%)": f"{proveedores_weight * 100:.2f}%",
                            "Comisión Fans (%)": f"{user_weight * 100:.2f}%",
                            "Comisión Total (€)": f"{cashback_arquetipo * participacion_merchants / 100 * total_weight:,.2f}€",
                            "Comisión Club (€)": f"{cashback_arquetipo * participacion_merchants / 100 * club_weight:,.2f}€",
                            "Comisión Proveedores (€)": f"{cashback_arquetipo * participacion_merchants / 100 * proveedores_weight:,.2f}€",
                            "Cashback Fans (€)": f"{cashback_arquetipo * participacion_merchants / 100 * user_weight:,.2f}€",
                            "Cashback total (€)": f"{cashback_arquetipo * participacion_merchants / 100:,.2f}€"
                        })

        # Helper functions
        def clean_currency(val): return float(val.replace("€", "").replace(",", "").strip())
        def clean_percentage(val): return float(val.replace("%", "").strip())

        # Load and clean
        df = pd.DataFrame(detalle_cashback)
        df = df.groupby(["Arquetipo", "Categoría"]).agg({
            "Gasto promedio": "first",
            "Comisión Total (%)": "first",
            "Comisión Club (%)": "first",
            "Comisión Proveedores (%)": "first",
            "Participación merchants (%)": "first",
            "Fans": "first"
        }).reset_index()

        # Clean values
        df["Gasto promedio"] = df["Gasto promedio"].apply(clean_currency)
        df["Comisión Total (%)"] = df["Comisión Total (%)"].apply(clean_percentage)
        df["Comisión Club (%)"] = df["Comisión Club (%)"].apply(clean_percentage)
        df["Comisión Proveedores (%)"] = df["Comisión Proveedores (%)"].apply(clean_percentage)
        df["Participación merchants (%)"] = df["Participación merchants (%)"].apply(clean_percentage)

        # Fans participation from arquetipos, as chosen in slider participacion_arquetipos
        df["Fans participation (%)"] = df["Arquetipo"].map(participacion_arquetipos)

        # Compose JSON
        structured = {}

        for _, row in df.iterrows():
            arquetipo = row["Arquetipo"]
            if arquetipo not in structured:
                structured[arquetipo] = {}

            fans_base = row["Fans"]
            gasto = row["Gasto promedio"]
            total_pct = row["Comisión Total (%)"]/ 100
            club_pct = row["Comisión Club (%)"] / 100
            prov_pct = row["Comisión Proveedores (%)"] / 100
            merch_pct = row["Participación merchants (%)"] / 100

            proyeccion = {}
            for año in range(1, 4):
                incremento = round(((1 + aumento_fans / 100) ** (año - 1) - 1) * 100, 2)
                fans_year = fans_base * (1 + aumento_fans / 100) ** (año - 1)

                cashback_total = fans_year * gasto * (total_pct) * (merch_pct)
                cashback_club = cashback_total * club_pct
                cashback_prov = cashback_total * prov_pct
                cashback_fan = cashback_total * (1 - club_pct - prov_pct)

                proyeccion[f"Año {año}"] = {
                    "Incremento (%)": incremento,
                    "Fans": int(fans_year), 
                    "Cashback": {
                        "Cashback mensual total (€)": cashback_total,
                        "Cashback mensual fan (€)": cashback_fan,
                        "Cashback mensual proveedores (€)": cashback_prov,
                        "Cashback mensual club (€)": cashback_club,
                    }
                }

            structured[arquetipo][len(structured[arquetipo])] = {
                "Categoría": row["Categoría"],
                "Gasto promedio": gasto,
                "Fans (total por arquetipo)": arquetipos_ciudad[arquetipo], 
                "Fans participation (%)": round(row["Fans participation (%)"], 2),
                "Fans (participación num)": int(fans_base),
                "Comisiones": {
                    "Club (%)": club_pct,
                    "Fans (%)": round(1 - club_pct - prov_pct, 2),
                    "Proveedores (%)": prov_pct,
                },
                "Merchans participation (%)": merch_pct,
                "Proyección": proyeccion
            }

        # Convert to pretty JSON
        pretty_json = json.dumps(structured, indent=4, ensure_ascii=False)
        #st.code(pretty_json, language="json")
        
        cashback_mensual_all_fan = 0    
        # Iterate over the structured data to calculate the total cashback (YEAR 1)
        for arquetipo, categorias in structured.items():
            for categoria, data in categorias.items():
                cashback_mensual_all_fan += data["Proyección"]["Año 1"]["Cashback"]["Cashback mensual fan (€)"]


        # KPI card for total ingresos generados (fans)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f5c542, #f5c542);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6);
            text-align: center;
            border: 1px solid #f5c542;
        ">
            <p style="margin: 5px 0 0; font-size: 32px; font-weight: bold; color: #31333f;">
                {cashback_mensual_all_fan:,.2f}€
            </p>
            <p style="margin: 0; font-size: 12px; font-weight: 600; color: #31333f; letter-spacing: 1px;">
                TOTAL INGRESOS GENERADOS POR LOS FANS AL MES
            </p>

        </div>
        """, unsafe_allow_html=True)


        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)

        # 🌟 Custom KPI Cards - Yearly Projections
        col1, col2, col3 = st.columns(3)

        # Calculate yearly totals: FAN
        year_1_total = 0
        year_2_total = 0
        year_3_total = 0

        for arquetipo, categorias in structured.items():
            for categoria, data in categorias.items():
                year_1_total += data["Proyección"]["Año 1"]["Cashback"]["Cashback mensual fan (€)"] * 12
                year_2_total += data["Proyección"]["Año 2"]["Cashback"]["Cashback mensual fan (€)"] * 12
                year_3_total += data["Proyección"]["Año 3"]["Cashback"]["Cashback mensual fan (€)"] * 12
        

        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2a2a40, #2a2a40);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6);
                text-align: center;
                #border: 1px solid #f5c542;
            ">
                <p style="margin: 5px 0 0; font-size: 26px; font-weight: bold; color: #f5c542;">
                    {year_1_total:,.2f}€
                </p>
                <p style="margin: 0; font-size: 12px; font-weight: 600; color: #f0f0f0; letter-spacing: 1px;">
                    PRIMER AÑO
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2a2a40, #2a2a40);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6);
                text-align: center;
                #border: 1px solid #f5c542;
            ">
                <p style="margin: 5px 0 0; font-size: 26px; font-weight: bold; color: #f5c542;">
                    {year_2_total:,.2f}€
                </p>
                <p style="margin: 0; font-size: 12px; font-weight: 600; color: #f0f0f0; letter-spacing: 1px;">
                    SEGUNDO AÑO
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2a2a40, #2a2a40);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6);
                text-align: center;
                #border: 1px solid #f5c542;
            ">
                <p style="margin: 5px 0 0; font-size: 26px; font-weight: bold; color: #f5c542;">
                    {year_3_total:,.2f}€
                </p>
                <p style="margin: 0; font-size: 12px; font-weight: 600; color: #f0f0f0; letter-spacing: 1px;">
                    TERCER AÑO
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)

        # Dotted line with more space between dots
        st.markdown("""
        <div style="
            width: 100%;
            height: 5px;
            background-image: radial-gradient(circle, #f5c542 1px, transparent 1px);
            background-size: 10px 5px;  /* dot spacing (horizontal x vertical) */
            background-repeat: repeat-x;
            margin: 30px 0;
        "></div>
        """, unsafe_allow_html=True)

        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)

        ## Distribución de cashback para club y proveedores
        # Iterate over the structured data to calculate the total cashback, every year and plot in bar chart (x axis, year; y axis, cashback; legend: club/proveedores)
        chart_data = []

        # Iterate over arquetipos and categories
        for arquetipo, categorias in structured.items():
            for _, cat_info in categorias.items():
                for año in ["Año 1", "Año 2", "Año 3"]:
                    club_cb = cat_info["Proyección"][año]["Cashback"]["Cashback mensual club (€)"]
                    prov_cb = cat_info["Proyección"][año]["Cashback"]["Cashback mensual proveedores (€)"]
                    
                    chart_data.append({
                        "Año": año,
                        "Tipo": "Club",
                        "Cashback (€)": club_cb * 12  # Convert to yearly
                    })
                    chart_data.append({
                        "Año": año,
                        "Tipo": "Proveedores",
                        "Cashback (€)": prov_cb * 12  # Convert to yearly
                    })

        # Convert to DataFrame and group totals per year/type
        df_cashback = pd.DataFrame(chart_data)
        df_cashback = df_cashback.groupby(["Año", "Tipo"], as_index=False).sum()

        # Title for chart 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center;"> 
            <p style="margin: 0; font-size: 12px; font-weight: 600; color: #f0f0f0; letter-spacing: 1px;">
                NEGOCIO GENERADO POR EL CLUB Y PROVEEDORES
            </p>
        </div>
        """, unsafe_allow_html=True)
            

        fig = px.bar(
            df_cashback,
            x="Año",
            y="Cashback (€)",
            color="Tipo",
            barmode="relative",
            title="NEGOCIO GENERADO POR EL CLUB Y PROVEEDORES",
            text_auto=".2s",
            color_discrete_map={
                "Club": "#f5c542",
                "Proveedores": "#2a2a40"
            }
        )

        fig.update_layout(title_text="", title_x=0.5)
        
        fig.update_layout(
            title_x=0.0,
            yaxis_title="Cashback (€)",
            xaxis_title="",
            font=dict(family="Arial", size=13, color="#2a2a40"),
            legend_title="Beneficiario",
            margin=dict(l=20, r=20, t=60, b=40),
            showlegend=True,
            dragmode=False,
        )

        # Prevent zoom/pan
        fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)

        # Clean bar appearance
        fig.update_traces(marker_line_color='white', marker_line_width=1, textposition='outside')
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.1)', zeroline=False)
        fig.update_traces(textfont_color='lightgrey', selector=dict(name="Proveedores"))

        # Legend upper centered
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=12),
            )
        )
        fig.update_layout(legend_title_text=None)

        # Show chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


        # Dotted line with more space between dots
        st.markdown("""
        <div style="
            width: 100%;
            height: 5px;
            background-image: radial-gradient(circle, #f5c542 1px, transparent 1px);
            background-size: 10px 5px;  /* dot spacing (horizontal x vertical) */
            background-repeat: repeat-x;
            margin: 30px 0;
        "></div>
        """, unsafe_allow_html=True)

        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)

        # Slicer for percentage of cashback used in the club
        cashback_used_slicer = st.slider(
            "¿Qué porcentaje de cashback de los fans se destina al club anualmente?",
            min_value=0,
            max_value=100,
            value=65,
            step=1
        )

        # Calculate cashback used
        cashback_used = cashback_mensual_all_fan * (cashback_used_slicer / 100) * 12

        # KPI card for total ingresos generados (fans)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f5c542, #f5c542);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6);
            text-align: center;
            border: 1px solid #f5c542;
        ">
            <p style="margin: 5px 0 0; font-size: 32px; font-weight: bold; color: #31333f;">
                {cashback_used:,.2f}€
            </p>
            <p style="margin: 0; font-size: 12px; font-weight: 600; color: #31333f; letter-spacing: 1px;">
                CASHBACK UTILIZADO POR LOS FANS EN EL CLUB ANUALMENTE
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)

        # 🌟 Custom KPI Cards - Yearly Projections
        col1, col2, col3 = st.columns(3)

        # Calculate yearly totals: FAN
        cashback_year_1 = 0
        cashback_year_2 = 0
        cashback_year_3 = 0


        for arquetipo, categorias in structured.items():
            for categoria, data in categorias.items():
                cashback_year_1 += data["Proyección"]["Año 1"]["Cashback"]["Cashback mensual fan (€)"] * 12 * (cashback_used_slicer / 100)
                cashback_year_2 += data["Proyección"]["Año 2"]["Cashback"]["Cashback mensual fan (€)"] * 12 * (cashback_used_slicer / 100)
                cashback_year_3 += data["Proyección"]["Año 3"]["Cashback"]["Cashback mensual fan (€)"] * 12 * (cashback_used_slicer / 100)


        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2a2a40, #2a2a40);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6);
                text-align: center;
                #border: 1px solid #f5c542;
            ">
                <p style="margin: 5px 0 0; font-size: 26px; font-weight: bold; color: #f5c542;">
                    {cashback_year_1:,.2f}€
                </p>
                <p style="margin: 0; font-size: 12px; font-weight: 600; color: #f0f0f0; letter-spacing: 1px;">
                    PRIMER AÑO
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2a2a40, #2a2a40);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6);
                text-align: center;
                #border: 1px solid #f5c542;
            ">
                <p style="margin: 5px 0 0; font-size: 26px; font-weight: bold; color: #f5c542;">
                    {cashback_year_2:,.2f}€
                </p>
                <p style="margin: 0; font-size: 12px; font-weight: 600; color: #f0f0f0; letter-spacing: 1px;">
                    SEGUNDO AÑO
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2a2a40, #2a2a40);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6);
                text-align: center;
                #border: 1px solid #f5c542;
            ">
                <p style="margin: 5px 0 0; font-size: 26px; font-weight: bold; color: #f5c542;">
                    {cashback_year_3:,.2f}€
                </p>
                <p style="margin: 0; font-size: 12px; font-weight: 600; color: #f0f0f0; letter-spacing: 1px;">
                    TERCER AÑO
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


        # Dotted line with more space between dots
        st.markdown("""
        <div style="
            width: 100%;
            height: 5px;
            background-image: radial-gradient(circle, #f5c542 1px, transparent 1px);
            background-size: 10px 5px;  /* dot spacing (horizontal x vertical) */
            background-repeat: repeat-x;
            margin: 30px 0;
        "></div>
        """, unsafe_allow_html=True)

        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)

        # Estimación de meses necesarios para comprar camiseta y entrada
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f5c542, #f5c542);
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
            text-align: center;
        ">
            <p style="margin: 0; font-size: 12px; font-weight: 600; color: #31333f; letter-spacing: 1px;">
                ESTIMACIÓN DE MESES NECESARIOS PARA COMPRAR CAMISETA Y ENTRADA
            </p>
            <p style="margin: 0; font-size: 12px; color: #31333f; letter-spacing: 1px;">
                <br>Para calcular el número de meses necesarios para comprar una camiseta o una entrada, 
                se ha utilizado el precio de la camiseta y la entrada, así como el cashback mensual estimado por fan.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
                    

        precio_camiseta = 80
        precio_entrada = 30  # Hasta 80-90 euros
        cashback_per_arquetipo = {}

        for arquetipo, categorias in structured.items():
            st.write(f"🎯 Arquetipo: {arquetipo}")

            # Sum cashback mensual per arquetipo
            if arquetipo not in cashback_per_arquetipo:
                cashback_per_arquetipo[arquetipo] = 0

            for categoria, data in categorias.items():
                cashback_mensual = data["Proyección"]["Año 1"]["Cashback"]["Cashback mensual fan (€)"]
                cashback_per_arquetipo[arquetipo] += cashback_mensual

            num_users = users_por_arquetipo.get(arquetipo, 0)
            cashback_arquetipo_avg = cashback_per_arquetipo[arquetipo] / num_users if num_users > 0 else 0

            meses_camiseta = precio_camiseta / cashback_arquetipo_avg if cashback_arquetipo_avg > 0 else float("inf")
            meses_entrada = precio_entrada / cashback_arquetipo_avg if cashback_arquetipo_avg > 0 else float("inf")

            st.markdown(f"""
            <div style="background-color:#2a2a40;padding:15px 20px;border-radius:8px;margin-bottom:10px;">
                <p style="margin:0;font-size:14px;">
                    🧾 Cashback mensual estimado por fan: <strong>{cashback_arquetipo_avg:.2f}€</strong>
                </p>
                <p style="margin:0;font-size:14px;">
                    🧢 Para comprar una camiseta de <strong>{precio_camiseta}€</strong>, 
                    un fan necesitaría <strong>{meses_camiseta:.1f} meses</strong> de cashback.
                </p>
                <p style="margin:0;font-size:14px;">
                    🎟️ Para comprar una entrada de <strong>{precio_entrada}€</strong>, 
                    un fan necesitaría <strong>{meses_entrada:.1f} meses</strong> de cashback.
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)


    # Inicializar el flag reset
    if "reset" not in st.session_state:
        st.session_state.reset = False

    # Botón de reinicio
    if buttons['Reiniciar']:
        st.session_state.reset = True
        st.rerun()

    # Si está activado el reinicio, resetear los sliders y otros valores
    if st.session_state.reset:
        st.session_state.slider_fan_casual = 15
        st.session_state.slider_profesional = 15
        st.session_state.slider_familia = 15
        st.session_state.slider_jubilados = 15

        st.session_state.participacion_arquetipos = {
            "Fan casual (joven adulto)": 15,
            "Adulto profesional soltero": 15,
            "Familia de clase media con dos hijos": 15,
            "Pareja de jubilados": 15
        }

        st.session_state.participacion_merchants = 90
        st.session_state.aumento_fans = 10

        st.session_state.reset = False
        st.rerun()  # rerun final para mostrar los valores reseteados


    #If button 'Exportar' is pressed
    if buttons['Exportar']:
        # Exportar el JSON a un archivo
        with open("cashback_proyeccion.json", "w", encoding="utf-8") as f:
            f.write(pretty_json)
        st.success("Archivo JSON exportado correctamente.")