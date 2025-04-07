# Importación de librerías
import streamlit as st
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la aplicación
st.set_page_config(page_title='Simulación', layout='centered', initial_sidebar_state='collapsed')

# Título de la aplicación
st.title('')
st.markdown('')
st.write('')

tab1, tab2, tab3 = st.tabs(["Definición de arquetipos", "Cálculo de comisiones", "Análisis de beneficios"])#, "Simulación de escenarios"])

##### Definición de arquetipos

with tab1:
    st.sidebar.title('Arquetipos')
    st.sidebar.markdown('## Definición de arquetipos')
    # st.write('En esta sección detallamos y elegimos los gastos mensuales categorizados para cada arquetipo.')
    # Write a message in Spansh explaining that this tab is for defining the monthly expenses for each archetype for each expense category.
    #st.write('Selecciona los importes medios de cada categoría de gasto para cada arquetipo. Estos importes se utilizarán para calcular el cashback mensual estimado por fan y por arquetipo. Puedes modificar los valores por defecto para adaptarlos a tu caso específico.')
    st.markdown("""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
    <p style="margin:0;font-size:14px;">ℹ️ Selecciona los importes medios de cada categoría de gasto para cada arquetipo.
    Estos importes se utilizarán para calcular el cashback mensual estimado por fan y por arquetipo.
    Puedes modificar los valores por defecto para adaptarlos a cada caso específico.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Valores generales de las categorías
    CATEGORIAS_RANGO = {
        "Alimentación y bebidas no alcohólicas": (0, 1000),
        "Transporte (gasolina, coche)": (0, 500),
        "Suministros: electricidad, gas": (0, 2000),
        "Sanidad (Seguros médicos)": (0, 500),
        "Restaurantes, ocio y cultura": (0, 500),

        "Ropa y calzado": (0, 500),
        "Educación (colegios, actividades)": (0, 1000),
        "Deporte y bienestar (gimnasio, clubs)": (0, 300),
        "Tecnología y telecomunicaciones": (0, 300),
        "Otros bienes y servicios": (0, 300),
        "Abono (deportivo)": (0, 100),
        "Merchandising y compras esporádicas": (0, 100)
    }

    # Valores mínimos y máximos por arquetipo
    ARQUETIPOS_ORIGINALES = {
        "Fan casual (joven adulto)": {
            "Alimentación y bebidas no alcohólicas": (150, 250),
            "Transporte (gasolina, coche)": (20, 50),
            "Suministros: electricidad, gas": (0, 50),
            "Sanidad (Seguros médicos)": (0, 0),
            "Restaurantes, ocio y cultura": (100, 150),

            "Ropa y calzado": (10, 50),
            "Educación (colegios, actividades)": (0, 0),
            "Deporte y bienestar (gimnasio, clubs)": (25, 60),
            "Tecnología y telecomunicaciones": (10, 30),
            "Otros bienes y servicios": (20, 80),
            "Abono (deportivo)": (0, 0),
            "Merchandising y compras esporádicas": (0, 0)
        },
        "Adulto profesional soltero": {
            "Alimentación y bebidas no alcohólicas": (200, 300),
            "Transporte (gasolina, coche)": (50, 100),
            "Suministros: electricidad, gas": (0, 100),
            "Sanidad (Seguros médicos)": (0, 50),
            "Restaurantes, ocio y cultura": (150, 200),

            "Ropa y calzado": (50, 100),
            "Educación (colegios, actividades)": (0, 0),
            "Deporte y bienestar (gimnasio, clubs)": (30, 60),
            "Tecnología y telecomunicaciones": (20, 40),
            "Otros bienes y servicios": (50, 100),
            "Abono (deportivo)": (0, 80),
            "Merchandising y compras esporádicas": (0, 20)
        },
        "Familia de clase media con dos hijos": {
            "Alimentación y bebidas no alcohólicas": (500, 600),
            "Transporte (gasolina, coche)": (100, 200),
            "Suministros: electricidad, gas": (0, 200),
            "Sanidad (Seguros médicos)": (0, 80),
            "Restaurantes, ocio y cultura": (200, 300),

            "Ropa y calzado": (100, 200),
            "Educación (colegios, actividades)": (300, 400),
            "Deporte y bienestar (gimnasio, clubs)": (50, 100),
            "Tecnología y telecomunicaciones": (30, 60),
            "Otros bienes y servicios": (50, 150),
            "Abono (deportivo)": (0, 0),
            "Merchandising y compras esporádicas": (0, 20),
        },
        "Pareja de jubilados": {
            "Alimentación y bebidas no alcohólicas": (300, 400),
            "Transporte (gasolina, coche)": (0, 50),
            "Suministros: electricidad, gas": (0, 150),
            "Sanidad (Seguros médicos)": (50, 120),
            "Restaurantes, ocio y cultura": (50, 100),
            
            "Ropa y calzado": (20, 50),
            "Educación (colegios, actividades)": (0, 0),
            "Deporte y bienestar (gimnasio, clubs)": (25, 50),
            "Tecnología y telecomunicaciones": (20, 40),
            "Otros bienes y servicios": (50, 150),
            "Abono (deportivo)": (0, 0),
            "Merchandising y compras esporádicas": (0, 20)
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
        nuevos_valores = {}
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
                        
        st.session_state.valores_actuales = nuevos_valores

    # Botones de acción
    if st.button("Guardar cambios"):
        st.session_state.valores_modificados[arquetipo] = nuevos_valores
        st.info("Cambios guardados para este arquetipo!")

    if st.button("Restablecer original"):
        st.session_state.valores_actuales = ARQUETIPOS_ORIGINALES[arquetipo].copy()
        if arquetipo in st.session_state.valores_modificados:
            del st.session_state.valores_modificados[arquetipo]
        st.rerun()

#### Cálculo de porcentajes
with tab2:
    st.markdown("""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
    <p style="margin:0;font-size:14px;">ℹ️ En esta sección puedes editar los porcentajes de cashback por categoría y
    la distribución de los porcentajes entre el club, los proveedores y los fans. <br>Puedes modificar las comisiones base por categoría y la distribución de
    cashback entre el club, los proveedores y los fans. Estos porcentajes se utilizan para calcular el cashback
    mensual estimado por fan y por arquetipo.</p>
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
            st.session_state['club_weight'] = 0.1
        if 'user_weight' not in st.session_state:
            st.session_state['user_weight'] = 0.6
        if 'proveedores_weight' not in st.session_state:
            st.session_state['proveedores_weight'] = 0.3

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
            <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
            <p style="margin:0;font-size:14px;">La suma de los pesos es <strong>{total_weight:.2f}</strong>.
            Debe ser igual a 1.0 para que la distribución sea correcta.</p>
            <p style="margin:0;font-size:14px;">Puedes ajustar los pesos y hacer clic en "Recalcular" para
            normalizar automáticamente los pesos.</p>
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
            "Alimentación y bebidas no alcohólicas",
            "Transporte (gasolina, coche)",
            "Suministros: electricidad, gas",
            "Sanidad (Seguros médicos)",
            
            "Ropa y calzado",
            "Educación (colegios, actividades)",
            "Deporte y bienestar (gimnasio, clubs)",
            "Tecnología y telecomunicaciones",
            "Otros bienes y servicios",
            "Abono (deportivo)",
            "Merchandising y compras esporádicas"
        ]

        base_df = pd.DataFrame({
            "Categoría": categorias,
            "Porc. base (%)": [1.5] * len(categorias)
        })

        num_columns = 2
        columns = st.columns(num_columns)

        for index, row in base_df.iterrows():
            col = columns[index % num_columns]
            with col:
                base_df.at[index, "Porc. base (%)"] = st.number_input(
                    f"{row['Categoría']}",
                    min_value=0.0,
                    max_value=5.0,
                    value=row["Porc. base (%)"],
                    step=0.1,
                    format="%.2f",
                    key=f"input_{index}"
                )

        # Calcula el porcentaje avg
        base_df["Porc. avg (%)"] = base_df["Porc. base (%)"].mean()
        st.markdown(f"""
        <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
        <p style="margin:0;font-size:14px;">ℹ️ El porcentaje base por categoría es el promedio de los porcentajes
        de cada categoría: <strong>{base_df["Porc. base (%)"].mean():.2f}%</strong></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    
    
#### Análisis de beneficios
with tab3:
    st.subheader("Distribución de población por arquetipos")
    
    # Create columns
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
    porcentaje = total_poblacion / 250000 * 100
        
    st.markdown("<br>", unsafe_allow_html=True)

    st.progress(int(porcentaje)/100)
    
    st.markdown(f"""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
    <p style="margin:0;font-size:14px;">ℹ️ Estos arquetipos representan <strong>{total_poblacion:,} habitantes</strong> 
    ({porcentaje:.1f}%) de la población base de 250,000 habitantes.</p>
    </div>
    """, unsafe_allow_html=True)

    base_social = 40000
    porcentaje_bs = base_social / 250000 * 100
    porcentaje_sc = base_social / total_poblacion * 100
    st.markdown(f"""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
    <p style="margin:0;font-size:14px;">ℹ️ Base social inicial de 40,000 habitantes. </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)



    # Configuración de participación
    st.subheader("Configuración de participación por arquetipo")
    
    # Sliders individuales para cada arquetipo
    participacion_arquetipos = {
        "Fan casual (joven adulto)": st.slider("% Fan casuales activos: ", 1, 100, 15),
        "Adulto profesional soltero": st.slider("% Profesionales solteros activos", 1, 100, 15),
        "Familia de clase media con dos hijos": st.slider("% Familias activas", 1, 100, 15),
        "Pareja de jubilados": st.slider("% Jubilados activos", 1, 100, 15)
    }

    # Calculamos el número de fans por arquetipo.
    fans_casual = arquetipos_ciudad["Fan casual (joven adulto)"] * participacion_arquetipos["Fan casual (joven adulto)"] / 100
    adultos_profesionales = arquetipos_ciudad["Adulto profesional soltero"] * participacion_arquetipos["Adulto profesional soltero"] / 100
    familias = arquetipos_ciudad["Familia de clase media con dos hijos"] * participacion_arquetipos["Familia de clase media con dos hijos"] / 100
    jubilados = arquetipos_ciudad["Pareja de jubilados"] * participacion_arquetipos["Pareja de jubilados"] / 100
    total_participacion = fans_casual + adultos_profesionales + familias + jubilados
    

    st.progress(int(total_participacion)/total_poblacion)

    st.markdown(f"""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
    <p style="margin:0;font-size:14px;">ℹ️ La selección suma un total de <strong>{total_participacion:,.0f} fans</strong>
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

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


    
    # Slider para participación de merchans (agrupados, avg)
    participacion_merchants = st.slider("% Merchants activos", 1, 100, 5)

    # Cálculo de beneficios usando gastos de arquetipos
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Estimación")


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
                        "Gasto Promedio": f"{gasto_promedio:,.2f}€",
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

    #st.dataframe(pd.DataFrame(detalle_cashback), use_container_width=True)
    
    # Get cashback mensual por arquetipo
    df_cashback_arquetipo = pd.DataFrame(detalle_cashback)
    df_cashback_arquetipo = df_cashback_arquetipo.groupby("Arquetipo").agg({"Cashback Fans (€)": lambda x: sum(float(i.replace("€", "").replace(",", "")) for i in x)}).reset_index()
    df_cashback_arquetipo["Fans"] = df_cashback_arquetipo["Arquetipo"].map(users_por_arquetipo)
    df_cashback_arquetipo['Avg'] = df_cashback_arquetipo["Cashback Fans (€)"] / df_cashback_arquetipo["Fans"]
    
    # Calcular cashback total de fans, según participación de merchants
    # sum all rows for Cashback Fans (€)
    cashback_total_fans = df_cashback_arquetipo["Cashback Fans (€)"].sum()
    cashback_total = cashback_total * participacion_merchants / 100
    
    # Mostrar resultados
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total fans potenciales", f"{total_users:,.0f}")
        
    with col2:
        st.metric("Cashback mensual estimado", f"{cashback_total_fans:,.2f}€")
        
    with col3:
        st.metric("Cashback anual estimado", f"{cashback_total_fans * 12:,.2f}€")

    avg_user = cashback_total_fans / total_users if total_users > 0 else 0
    st.markdown(f"""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
    <p style="margin:0;font-size:14px;">ℹ️ El cashback mensual por fan es de <strong>{avg_user:,.2f}€</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)



    st.dataframe(df_cashback_arquetipo, use_container_width=True)

    # Para comprar una camiseta cuántos meses tardaríamos? Y una entrada? Cada uno de los arquetipos
    precio_camiseta = 80
    precio_entrada = 30 # Hasta 80-90 euros

    # Print cashback mensual estimado por arquetipo
    for index, row in df_cashback_arquetipo.iterrows():
        arquetipo = row["Arquetipo"]
        st.write(f"Arquetipo: {arquetipo}")
        cashback_arquetipo = row["Cashback Fans (€)"]



        cashback_arquetipo_avg = cashback_arquetipo / num_users if num_users > 0 else 0

        st.write(f"Cashback mensual estimado por fan: {cashback_arquetipo_avg:.2f}€")
        meses_camiseta = precio_camiseta / cashback_arquetipo_avg
        meses_entrada = precio_entrada / cashback_arquetipo_avg
        st.markdown(f"""
        <div style="background-color:#f0f2f6;padding:10px;border-radius:5px;">
        <p style="margin:0;font-size:14px;">Fan <strong>{arquetipo}</strong>:</p>
        <p style="margin:0;font-size:14px;">— Para comprar una camiseta de <strong>{precio_camiseta}€</strong>
        necesitarías <strong>{meses_camiseta:.1f} meses</strong> de cashback.</p>
        <p style="margin:0;font-size:14px;">— Para comprar una entrada de <strong>{precio_entrada}€</strong>
        necesitarías <strong>{meses_entrada:.1f} meses</strong> de cashback.</p>
        </div>
        """, unsafe_allow_html=True)
    



    
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Get the distribution of cashback per user type: club, user, providers
    # Create a DataFrame for the distribution
    df_distribution = pd.DataFrame({
        "Tipo": ["Club", "Proveedores", "Fans"],
        "Distribución (%)": [club_weight * 100, proveedores_weight * 100, user_weight * 100]
    })
    df_distribution["Distribución mensual (€)"] = df_distribution["Distribución (%)"] / 100 * cashback_total
    df_distribution["Distribución anual (€)"] = df_distribution["Distribución mensual (€)"] * 12
    st.dataframe(df_distribution, use_container_width=True)
    fig = px.pie(df_distribution, values='Distribución anual (€)', names='Tipo', title='',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside')
    fig.update_traces(textinfo='label')
    fig.update_traces(textfont_size=14)
    fig.update_layout(showlegend=True)
    fig.update_traces(marker=dict(colors=['#1f77b4', '#7f7f7f', '#d9d9d9']))
    st.plotly_chart(fig, use_container_width=True)

    # After calculating cashback_total, store it in session_state
    st.session_state.cashback_total = cashback_total
    st.session_state.detalle_cashback = detalle_cashback
