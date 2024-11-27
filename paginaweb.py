import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Dimex Gestor", page_icon=":office:", layout="centered")

# Estilo global con los colores personalizados
st.markdown(
    """
    <style>
    .titulo {
        color: #4B4F54;
        font-size: 28px;
        font-weight: bold;
    }
    .subtitulo {
        color: #63A532;
        font-size: 22px;
        font-weight: bold;
    }
    .texto-destacado {
        color: #4B4F54;
        font-size: 16px;
        font-weight: bold;
    }
    .texto-normal {
        color: #4B4F54;
        font-size: 14px;
    }
    .caption {
        color: #4B4F54;
        font-size: 12px;
        font-style: italic;
    }
    .boton-verde button {
        background-color: #63A532 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Función para la pantalla de login
def login_screen():
    st.markdown("<div class='titulo' style='text-align:center;'>Call Center</div>", unsafe_allow_html=True)  # Título "Call Center"
    st.markdown("<div class='titulo'>Bienvenido al Sistema de Gestión - Dimex</div>", unsafe_allow_html=True)
    st.markdown("<div class='texto-normal'>Por favor, inicia sesión para continuar.</div>", unsafe_allow_html=True)
    
    username = st.text_input("Usuario:", placeholder="Ingresa tu usuario")
    password = st.text_input("Contraseña:", type="password", placeholder="Ingresa tu contraseña")
    
    if st.button("Iniciar Sesión", use_container_width=True):
        if username == "gestor" and password == "dimex123":
            st.session_state["logged_in"] = True
            st.session_state["page"] = "search"
        else:
            st.error("Usuario o contraseña incorrectos.")

# Función para la pantalla de búsqueda de cliente
def search_screen():
    st.markdown("<div class='titulo'>Búsqueda de Cliente</div>", unsafe_allow_html=True)
    client_id = st.text_input("ID del Cliente:", placeholder="Ingresa el ID del cliente")
    
    if st.button("Buscar Cliente", use_container_width=True):
        dummy_data = {
            "12345": {
                "ID": "12345",
                "Nombre": "Juan Pérez",
                "Ingreso Bruto": 20000,
                "Edad": 45,
                "Deuda Acumulada": 5000,
                "Cuenta Contenida": "No",
                "Nivel de Atraso": "30_59",
                "Historial de Gestiones": ["Llamada en marzo", "Correo en abril", "Visita en mayo"],
                "PromesaPrevia": "Sí"
            },
            "67890": {
                "ID": "67890",
                "Nombre": "María López",
                "Ingreso Bruto": 15000,
                "Edad": 50,
                "Deuda Acumulada": 7000,
                "Cuenta Contenida": "Sí",
                "Nivel de Atraso": "90_119",
                "Historial de Gestiones": ["Llamada en enero", "Mensaje en febrero"],
                "PromesaPrevia": "No"
            }
        }
        client_data = dummy_data.get(client_id)
        if client_data:
            st.session_state["client_data"] = client_data
            st.session_state["page"] = "client_info"
        else:
            st.error("No se encontró un cliente con ese ID.")

    if st.button("Cerrar Sesión", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"

# Función para la pantalla de información del cliente
def client_info_screen():
    client_data = st.session_state.get("client_data", {})
    if not client_data:
        st.warning("No se encontró información del cliente.")
        return

    st.markdown(f"<div class='titulo'>{client_data['Nombre']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='caption'>ID: {client_data['ID']}</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("<div class='subtitulo'>Decisión del Gestor</div>", unsafe_allow_html=True)
    decision_options = ["Quita/Castigo", "Tus Pesos Valen Más", "Pago Sin Beneficio", "Reestructura del Crédito"]
    decision = st.selectbox("Selecciona una opción:", options=decision_options)

    incluir_promesa = st.checkbox("¿Registrar una promesa de pago?")
    if incluir_promesa:
        promise_date = st.date_input("Fecha de promesa de pago:")
        promise_amount = st.text_input("Monto prometido por el cliente:", placeholder="Ingresa el monto prometido")

    comentarios = st.text_area("Comentarios:", placeholder="Escribe aquí tus comentarios...")

    if st.button("Guardar Información", use_container_width=True):
        if incluir_promesa and not promise_amount:
            st.error("Por favor, ingresa el monto prometido por el cliente.")
        else:
            st.success("Información guardada correctamente:")
            st.json({
                "ID Cliente": client_data["ID"],
                "Decisión del Gestor": decision,
                "Fecha de Promesa de Pago": str(promise_date) if incluir_promesa else "N/A",
                "Monto de Promesa de Pago": promise_amount if incluir_promesa else "N/A",
                "Comentarios": comentarios,
            })

    if st.button("Regresar", use_container_width=True):
        st.session_state["page"] = "search"

# Control de flujo de la aplicación
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"

if st.session_state["page"] == "login":
    login_screen()
elif st.session_state["page"] == "search":
    search_screen()
elif st.session_state["page"] == "client_info":
    client_info_screen()