import streamlit as st
import math

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Calculadora de Engenharia",
    page_icon="📐",
    layout="wide"
)

# ========== SENHA DIRETA (SEM HASH) ==========
SENHA_CORRETA = "Engenharia2024"  # Senha que você quer

# ========== VERIFICAÇÃO DE SENHA SIMPLES ==========
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.markdown("""
    <div style='
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    '>
        <h1>🔐 Calculadora de Engenharia</h1>
        <p>Acesso restrito à equipe</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        senha = st.text_input("Digite a senha:", type="password", key="input_senha")
        
        if st.button("✅ Entrar", use_container_width=True):
            if senha == SENHA_CORRETA:
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("❌ Senha incorreta! Tente: Engenharia2024")
    
    st.stop()

# ========== APP PRINCIPAL ==========
st.title("📐 Calculadora do Teorema de Pitágoras")
st.markdown("---")

# Menu lateral
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    tipo_calculo = st.radio(
        "Tipo de cálculo:",
        ["📏 Calcular Hipotenusa", "📐 Calcular Cateto"]
    )
    
    st.markdown("---")
    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.rerun()

# Cálculos
if tipo_calculo == "📏 Calcular Hipotenusa":
    col1, col2 = st.columns(2)
    
    with col1:
        a = st.number_input("Cateto a", value=3.0, step=0.1)
    
    with col2:
        b = st.number_input("Cateto b", value=4.0, step=0.1)
    
    if st.button("🧮 Calcular"):
        c = math.sqrt(a**2 + b**2)
        st.success(f"### Hipotenusa = {c:.4f}")
        st.latex(f"c = \sqrt{{{a}^2 + {b}^2}} = {c:.4f}")

else:
    col1, col2 = st.columns(2)
    
    with col1:
        c = st.number_input("Hipotenusa", value=5.0, step=0.1)
    
    with col2:
        b = st.number_input("Cateto conhecido", value=4.0, step=0.1)
    
    if st.button("🧮 Calcular"):
        if c > b:
            a = math.sqrt(c**2 - b**2)
            st.success(f"### Cateto = {a:.4f}")
            st.latex(f"a = \sqrt{{{c}^2 - {b}^2}} = {a:.4f}")
        else:
            st.error("Hipotenusa deve ser maior que o cateto!")

st.markdown("---")
st.caption("✅ Logado com sucesso | Senha: Engenharia2024")
