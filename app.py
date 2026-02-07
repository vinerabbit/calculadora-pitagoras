import streamlit as st
import math
import hmac
import hashlib

# ========== CONFIGURAÇÃO DA PÁGINA ==========
st.set_page_config(
    page_title="Calculadora Pitágoras | Engenharia",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== SISTEMA DE SENHA ==========
def check_password():
    """Retorna True se a senha estiver correta."""
    
    # Senha configurada (em produção, use variáveis de ambiente!)
    SENHA_CORRETA = hashlib.sha256("Engenharia123".encode()).hexdigest()
    
    def password_entered():
        """Verifica se a senha está correta."""
        entered_hash = hashlib.sha256(st.session_state["password"].encode()).hexdigest()
        if hmac.compare_digest(entered_hash, SENHA_CORRETA):
            st.session_state["password_correct"] = True
            # Não armazena a senha
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    
    # Retorna True se já passou pela senha
    if st.session_state.get("password_correct", False):
        return True
    
    # Tela de login
    st.title("🔐 Calculadora Profissional")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=150)
        st.text_input(
            "Digite a senha de acesso:",
            type="password",
            key="password",
            help="Contato o administrador para obter a senha"
        )
        
        # Botões lado a lado
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Entrar", use_container_width=True):
                password_entered()
                st.rerun()
        with col_btn2:
            if st.button("🔄 Limpar", use_container_width=True):
                st.session_state["password"] = ""
                st.rerun()
        
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("❌ Senha incorreta. Tente novamente.")
    
    st.markdown("---")
    st.caption("© 2024 - Calculadora para uso interno da equipe de engenharia")
    
    return False

# ========== VERIFICA SENHA ANTES DE MOSTRAR O APP ==========
if not check_password():
    st.stop()

# ========== APP PRINCIPAL (só aparece se senha correta) ==========

# Título com emoji
st.title("📐 Calculadora do Teorema de Pitágoras")
st.markdown("---")

# Explicação
with st.expander("📖 Sobre esta calculadora", expanded=False):
    st.markdown("""
    **Teorema de Pitágoras:**  
    `a² + b² = c²`
    
    Onde:
    - `a` e `b` são os catetos
    - `c` é a hipotenusa
    
    **Fórmulas:**
    - Hipotenusa: `c = √(a² + b²)`
    - Cateto: `a = √(c² - b²)`
    
    *Use esta calculadora para projetos de engenharia, arquitetura e construção.*
    """)

# Seleção do tipo de cálculo
st.subheader("🔧 Tipo de Cálculo")
opcao = st.radio(
    "O que você deseja calcular?",
    ["📏 Calcular Hipotenusa (c)", "📐 Calcular Cateto (a ou b)"],
    horizontal=True
)

st.markdown("---")

# Container principal
with st.container():
    if opcao == "📏 Calcular Hipotenusa (c)":
        st.subheader("Hipotenusa a partir dos Catetos")
        
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input(
                "Cateto a",
                min_value=0.0,
                value=3.0,
                step=0.1,
                format="%.3f",
                help="Comprimento do primeiro cateto"
            )
        with col2:
            b = st.number_input(
                "Cateto b", 
                min_value=0.0,
                value=4.0,
                step=0.1,
                format="%.3f",
                help="Comprimento do segundo cateto"
            )
        
        # Cálculo
        if st.button("🧮 Calcular Hipotenusa", type="primary", use_container_width=True):
            if a > 0 and b > 0:
                c = math.sqrt(a**2 + b**2)
                
                # Resultado com destaque
                st.markdown("---")
                st.success(f"### Resultado: `c = {c:.6f}`")
                
                # Detalhes do cálculo
                with st.expander("📝 Ver detalhes do cálculo"):
                    st.latex(rf"c = \sqrt{{{a}^2 + {b}^2}}")
                    st.latex(rf"c = \sqrt{{{a**2:.4f} + {b**2:.4f}}}")
                    st.latex(rf"c = \sqrt{{{a**2 + b**2:.4f}}}")
                    st.latex(rf"c = {c:.6f}")
                
                # Triângulo visual
                st.markdown("#### 📐 Representação do Triângulo")
                st.code(f"""
                       |\\
                       | \\
                    {b:.2f} |  \\ {c:.2f}
                       |   \\
                       |____\\
                         {a:.2f}
                """)
            else:
                st.error("⚠️ Os catetos devem ser maiores que zero!")
    
    else:  # Calcular Cateto
        st.subheader("Cateto a partir da Hipotenusa e outro Cateto")
        
        col1, col2 = st.columns(2)
        with col1:
            c = st.number_input(
                "Hipotenusa (c)",
                min_value=0.0,
                value=5.0,
                step=0.1,
                format="%.3f",
                help="Comprimento da hipotenusa"
            )
        with col2:
            b = st.number_input(
                "Cateto conhecido (b)", 
                min_value=0.0,
                value=4.0,
                step=0.1,
                format="%.3f",
                help="Comprimento do cateto conhecido"
            )
        
        # Cálculo
        if st.button("🧮 Calcular Cateto", type="primary", use_container_width=True):
            if c > 0 and b > 0 and c > b:
                a = math.sqrt(c**2 - b**2)
                
                # Resultado
                st.markdown("---")
                st.success(f"### Resultado: `a = {a:.6f}`")
                
                # Detalhes
                with st.expander("📝 Ver detalhes do cálculo"):
                    st.latex(rf"a = \sqrt{{{c}^2 - {b}^2}}")
                    st.latex(rf"a = \sqrt{{{c**2:.4f} - {b**2:.4f}}}")
                    st.latex(rf"a = \sqrt{{{(c**2 - b**2):.4f}}}")
                    st.latex(rf"a = {a:.6f}")
                
                # Validação
                st.info(f"**Validação:** `√({a:.4f}² + {b:.4f}²) = {math.sqrt(a**2 + b**2):.4f}` (deve ser ≈ {c:.4f})")
            elif c <= b:
                st.error("⚠️ A hipotenusa deve ser MAIOR que o cateto!")
            else:
                st.error("⚠️ Valores devem ser positivos!")

# Informações adicionais
st.markdown("---")
with st.expander("⚙️ Configurações e Informações"):
    st.write("**Como usar:**")
    st.write("1. Selecione o tipo de cálculo")
    st.write("2. Insira os valores conhecidos")
    st.write("3. Clique no botão calcular")
    st.write("4. Use os resultados em seus projetos")
    
    st.write("**Precisão:** 6 casas decimais")
    
    # Botão para limpar tudo
    if st.button("🗑️ Limpar todos os dados e sair"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Rodapé
st.markdown("---")
st.caption("🔒 Acesso seguro | 📐 Ferramenta para engenheiros | v1.0")
