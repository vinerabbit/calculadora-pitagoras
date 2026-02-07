import streamlit as st
import math
import hmac
import hashlib
from datetime import datetime

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Calculadora de Engenharia | HF Spaces",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== ESTILOS CSS PERSONALIZADOS ==========
st.markdown("""
<style>
    /* Cores temáticas de engenharia */
    :root {
        --primary: #1E88E5;
        --secondary: #FF9800;
        --success: #4CAF50;
        --dark: #263238;
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--primary), #0D47A1);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--secondary);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    
    .result-box {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid var(--primary);
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), #1565C0);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(30, 136, 229, 0.3);
    }
    
    /* Animações */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ========== SISTEMA DE SENHA SEGURA ==========
def check_password():
    """Sistema de login seguro para Hugging Face."""
    
    # Na primeira execução, pede para configurar senha
    if "app_password" not in st.session_state:
        st.session_state.app_password = None
    
    if st.session_state.app_password is not None:
        # Verifica senha já configurada
        entered_password = st.text_input("🔐 Digite a senha:", type="password", key="login_pass")
        if st.button("Acessar"):
            entered_hash = hashlib.sha256(entered_password.encode()).hexdigest()
            if hmac.compare_digest(entered_hash, st.session_state.app_password):
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Senha incorreta!")
        return False
    
    # Tela de configuração inicial
    if "password_correct" not in st.session_state:
        st.markdown('<div class="main-header fade-in">', unsafe_allow_html=True)
        st.title("🔐 Configuração Inicial")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            <div class="card fade-in">
            <h3>Bem-vindo à Calculadora de Engenharia!</h3>
            <p>Configure uma senha de acesso para seu time:</p>
            </div>
            """, unsafe_allow_html=True)
            
            new_password = st.text_input("Crie uma senha segura:", type="password", key="new_pass")
            confirm_password = st.text_input("Confirme a senha:", type="password", key="confirm_pass")
            
            if st.button("✅ Configurar Senha", type="primary"):
                if new_password and new_password == confirm_password:
                    if len(new_password) >= 6:
                        st.session_state.app_password = hashlib.sha256(new_password.encode()).hexdigest()
                        st.session_state.password_correct = True
                        st.success("✅ Senha configurada com sucesso! Recarregando...")
                        st.rerun()
                    else:
                        st.warning("⚠️ A senha deve ter pelo menos 6 caracteres")
                else:
                    st.error("❌ As senhas não coincidem ou estão vazias")
        
        with col2:
            st.markdown("""
            <div class="card">
            <h4>💡 Dicas de segurança:</h4>
            <ul>
            <li>Use letras, números e símbolos</li>
            <li>Mínimo 6 caracteres</li>
            <li>Anote em local seguro</li>
            <li>Compartilhe apenas com a equipe</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        return False
    
    return st.session_state.get("password_correct", False)

# ========== VERIFICAÇÃO DE ACESSO ==========
if not check_password():
    st.stop()

# ========== APP PRINCIPAL ==========

# Cabeçalho visual
col_header1, col_header2, col_header3 = st.columns([3, 1, 1])
with col_header1:
    st.markdown('<div class="main-header fade-in">', unsafe_allow_html=True)
    st.title("📐 Calculadora Avançada de Engenharia")
    st.markdown(f"*Último acesso: {datetime.now().strftime('%d/%m/%Y %H:%M')}*")
    st.markdown("</div>", unsafe_allow_html=True)

with col_header2:
    st.metric("Status", "✅ Online", delta="Ativo")
with col_header3:
    if st.button("🚪 Sair"):
        for key in list(st.session_state.keys()):
            if key != "app_password":  # Mantém a senha configurada
                del st.session_state[key]
        st.rerun()

# Barra lateral com menu
with st.sidebar:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🧮 Menu de Cálculos")
    calculo_selecionado = st.radio(
        "Selecione o cálculo:",
        ["📏 Teorema de Pitágoras", 
         "📐 Trigonometria Básica",
         "⚖️ Conversão de Unidades",
         "📊 Estatísticas"],
        index=0
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="card">
    <h4>📈 Histórico Rápido</h4>
    <p>Últimos cálculos aparecem aqui</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Modo escuro/claro
    modo = st.toggle("🌙 Modo Escuro", value=False)
    if modo:
        st.markdown("""<style> .stApp { background-color: #0E1117; } </style>""", unsafe_allow_html=True)

# ========== CALCULADORA DE PITÁGORAS (MELHORADA) ==========
if calculo_selecionado == "📏 Teorema de Pitágoras":
    
    st.markdown("## 📐 Calculadora do Teorema de Pitágoras")
    
    # Layout em colunas
    col_config, col_calc = st.columns([1, 2])
    
    with col_config:
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.subheader("⚙️ Configurações")
        
        tipo_calculo = st.radio(
            "Calcular:",
            ["🔺 Hipotenusa (c)", "📐 Cateto (a/b)"],
            key="pit_tipo"
        )
        
        precisao = st.slider("Casas decimais:", 2, 8, 4)
        
        unidade = st.selectbox(
            "Unidade de medida:",
            ["metros", "centímetros", "milímetros", "polegadas", "pés"]
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Informação do triângulo
        with st.expander("📖 Sobre o Teorema"):
            st.latex(r"a^2 + b^2 = c^2")
            st.markdown("""
            **Onde:**
            - `a`, `b` = Catetos
            - `c` = Hipotenusa
            
            **Aplicações:**
            - Cálculo de escadas
            - Estruturas diagonais
            - Distâncias em planta baixa
            """)
    
    with col_calc:
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        
        if tipo_calculo == "🔺 Hipotenusa (c)":
            st.subheader("Calcular Hipotenusa")
            
            col_a, col_b = st.columns(2)
            with col_a:
                a = st.number_input(
                    f"Cateto a ({unidade})",
                    min_value=0.0,
                    value=3.0,
                    step=0.1,
                    format=f"%.{precisao}f",
                    help="Comprimento do primeiro cateto"
                )
            
            with col_b:
                b = st.number_input(
                    f"Cateto b ({unidade})",
                    min_value=0.0,
                    value=4.0,
                    step=0.1,
                    format=f"%.{precisao}f",
                    help="Comprimento do segundo cateto"
                )
            
            if st.button("🧮 Calcular Hipotenusa", type="primary", use_container_width=True):
                if a > 0 and b > 0:
                    c = math.sqrt(a**2 + b**2)
                    
                    # Resultado visual
                    st.markdown("---")
                    st.markdown(f'<div class="result-box fade-in">', unsafe_allow_html=True)
                    st.metric(
                        label=f"📐 Hipotenusa (c)",
                        value=f"{c:.{precisao}f} {unidade}",
                        delta=f"Triângulo {a:.1f}-{b:.1f}-{c:.1f}"
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Visualização do triângulo
                    st.subheader("📊 Visualização")
                    col_viz1, col_viz2 = st.columns(2)
                    
                    with col_viz1:
                        st.markdown(f"""
                        ```
                               |\\
                               | \\
                          {b:.{precisao}f} |  \\ {c:.{precisao}f}
                               |   \\
                               |____\\
                                 {a:.{precisao}f}
                        ```
                        """)
                    
                    with col_viz2:
                        # Gráfico simples
                        import matplotlib.pyplot as plt
                        fig, ax = plt.subplots(figsize=(3, 3))
                        triangle_x = [0, a, 0, 0]
                        triangle_y = [0, 0, b, 0]
                        ax.plot(triangle_x, triangle_y, 'b-', linewidth=2)
                        ax.fill(triangle_x, triangle_y, alpha=0.3)
                        ax.set_aspect('equal')
                        ax.grid(True, alpha=0.3)
                        st.pyplot(fig, use_container_width=True)
                    
                    # Detalhes matemáticos
                    with st.expander("📝 Ver cálculo passo a passo"):
                        st.latex(rf"c = \sqrt{{a^2 + b^2}}")
                        st.latex(rf"c = \sqrt{{{a}^{{2}} + {b}^{{2}}}}")
                        st.latex(rf"c = \sqrt{{{a**2:.{precisao}f} + {b**2:.{precisao}f}}}")
                        st.latex(rf"c = \sqrt{{{a**2 + b**2:.{precisao}f}}}")
                        st.latex(rf"c = {c:.{precisao}f}")
                        
                        # Informações adicionais
                        st.info(f"**Relação:** c/a = {c/a:.3f} | c/b = {c/b:.3f}")
                        
                else:
                    st.error("⚠️ Os catetos devem ser maiores que zero!")
        
        else:  # Calcular Cateto
            st.subheader("Calcular Cateto")
            
            col_c, col_b = st.columns(2)
            with col_c:
                c = st.number_input(
                    f"Hipotenusa c ({unidade})",
                    min_value=0.0,
                    value=5.0,
                    step=0.1,
                    format=f"%.{precisao}f"
                )
            
            with col_b:
                b = st.number_input(
                    f"Cateto conhecido ({unidade})",
                    min_value=0.0,
                    value=4.0,
                    step=0.1,
                    format=f"%.{precisao}f"
                )
            
            if st.button("🧮 Calcular Cateto", type="primary", use_container_width=True):
                if c > 0 and b > 0 and c > b:
                    a = math.sqrt(c**2 - b**2)
                    
                    st.markdown("---")
                    st.markdown(f'<div class="result-box fade-in">', unsafe_allow_html=True)
                    st.metric(
                        label=f"📐 Cateto desconhecido (a)",
                        value=f"{a:.{precisao}f} {unidade}",
                        delta=f"Faltante do triângulo"
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Validação
                    st.success(f"✅ Validação: √({a:.{precisao}f}² + {b:.{precisao}f}²) = {math.sqrt(a**2 + b**2):.{precisao}f} {unidade}")
                    
                elif c <= b:
                    st.error("❌ A hipotenusa deve ser MAIOR que o cateto!")
                else:
                    st.error("❌ Valores devem ser positivos!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ========== OUTROS MÓDULOS (ESQUELETO) ==========
elif calculo_selecionado == "📐 Trigonometria Básica":
    st.markdown("## 📐 Trigonometria Básica")
    st.info("Em desenvolvimento... Use o menu lateral para voltar a Pitágoras")
    # Aqui você pode adicionar seno, cosseno, tangente

elif calculo_selecionado == "⚖️ Conversão de Unidades":
    st.markdown("## ⚖️ Conversão de Unidades")
    st.info("Em desenvolvimento...")

elif calculo_selecionado == "📊 Estatísticas":
    st.markdown("## 📊 Estatísticas")
    st.info("Em desenvolvimento...")

# ========== RODAPÉ ==========
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)
with col_footer1:
    st.caption(f"🔄 Versão 1.0 | {datetime.now().year}")
with col_footer2:
    st.caption("🔒 Hospedado no Hugging Face Spaces")
with col_footer3:
    st.caption("📧 Suporte: seu-email@empresa.com")

# Botão de feedback
if st.button("💬 Enviar Feedback", key="feedback"):
    st.success("Obrigado! Em produção, isto enviaria um email ou abriria um formulário.")
