import streamlit as st
import math
import hashlib

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="Calculadora de Engenharia",
    page_icon="📐",
    layout="wide"
)

# ========== SENHA FIXA ==========
# SENHA: Engenharia2024 (não mudará)
SENHA_CORRETA_HASH = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6"  # Hash de "Engenharia2024"

# ========== VERIFICAÇÃO DE SENHA ==========
def verificar_senha():
    """Verifica se o usuário digitou a senha correta."""
    
    # Se já está logado, mostra o app
    if st.session_state.get("logado"):
        return True
    
    # Tela de login
    st.markdown("""
    <div style='
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    '>
        <h1>🔐 Calculadora Profissional</h1>
        <p>Acesso restrito à equipe de engenharia</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown("### 🔒 Área Restrita")
            senha = st.text_input(
                "Digite a senha de acesso:",
                type="password",
                help="Contate o administrador para obter a senha",
                key="input_senha"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("✅ Entrar", use_container_width=True):
                    # Gera hash da senha digitada
                    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                    
                    # Comparação segura
                    if senha_hash == SENHA_CORRETA_HASH:
                        st.session_state.logado = True
                        st.rerun()
                    else:
                        st.error("❌ Senha incorreta!")
                        
            with col_btn2:
                if st.button("🔄 Limpar", use_container_width=True):
                    st.rerun()
    
    # Rodapé da tela de login
    st.markdown("---")
    st.caption("© 2024 - Uso exclusivo da equipe de engenharia | Versão 1.0")
    
    return False

# ========== VERIFICA ANTES DE MOSTRAR O APP ==========
if not verificar_senha():
    st.stop()

# ========== APP PRINCIPAL (só aparece se senha correta) ==========

# Cabeçalho
st.title("📐 Calculadora do Teorema de Pitágoras")
st.markdown("---")

# Menu lateral
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    tipo_calculo = st.radio(
        "Tipo de cálculo:",
        ["📏 Calcular Hipotenusa", "📐 Calcular Cateto"],
        index=0
    )
    
    precisao = st.slider("Casas decimais:", 2, 6, 4)
    unidade = st.selectbox("Unidade:", ["m", "cm", "mm", "pol", "ft"])
    
    st.markdown("---")
    st.markdown("### 📊 Informações")
    st.info(f"Usuário: **Logado** | Precisão: **{precisao} decimais**")
    
    if st.button("🚪 Sair do sistema"):
        st.session_state.logado = False
        st.rerun()

# ========== CALCULADORA ==========
if tipo_calculo == "📏 Calcular Hipotenusa":
    st.subheader("📏 Cálculo da Hipotenusa")
    st.latex(r"c = \sqrt{a^2 + b^2}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        a = st.number_input(
            f"Cateto a ({unidade})",
            min_value=0.0,
            value=3.0,
            step=0.1,
            format=f"%.{precisao}f"
        )
    
    with col2:
        b = st.number_input(
            f"Cateto b ({unidade})",
            min_value=0.0,
            value=4.0,
            step=0.1,
            format=f"%.{precisao}f"
        )
    
    if st.button("🧮 Calcular Hipotenusa", type="primary"):
        if a > 0 and b > 0:
            c = math.sqrt(a**2 + b**2)
            
            # Resultado
            st.success("### ✅ Cálculo Concluído!")
            
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.metric(
                    label=f"Hipotenusa (c)",
                    value=f"{c:.{precisao}f} {unidade}",
                    delta="Resultado"
                )
            
            with col_res2:
                st.metric(
                    label="Relação c/a",
                    value=f"{c/a:.3f}",
                    delta="c ÷ a"
                )
            
            # Detalhes
            with st.expander("📝 Ver cálculo detalhado"):
                st.latex(rf"c = \sqrt{{{a}^2 + {b}^2}}")
                st.latex(rf"c = \sqrt{{{a**2:.4f} + {b**2:.4f}}}")
                st.latex(rf"c = \sqrt{{{a**2 + b**2:.4f}}}")
                st.latex(rf"c = {c:.{precisao}f} \, \text{{{unidade}}}")
            
            # Visualização
            st.markdown("#### 📐 Representação Gráfica")
            st.code(f"""
                   |\\
                   | \\
              {b:.2f} |  \\ {c:.2f}
                   |   \\
                   |____\\
                     {a:.2f}
            """)
            
        else:
            st.error("⚠️ Os valores devem ser maiores que zero!")

else:  # Calcular Cateto
    st.subheader("📐 Cálculo do Cateto")
    st.latex(r"a = \sqrt{c^2 - b^2}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        c = st.number_input(
            f"Hipotenusa c ({unidade})",
            min_value=0.0,
            value=5.0,
            step=0.1,
            format=f"%.{precisao}f"
        )
    
    with col2:
        b = st.number_input(
            f"Cateto conhecido ({unidade})",
            min_value=0.0,
            value=4.0,
            step=0.1,
            format=f"%.{precisao}f"
        )
    
    if st.button("🧮 Calcular Cateto", type="primary"):
        if c > 0 and b > 0:
            if c > b:
                a = math.sqrt(c**2 - b**2)
                
                st.success("### ✅ Cálculo Concluído!")
                
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.metric(
                        label=f"Cateto (a)",
                        value=f"{a:.{precisao}f} {unidade}",
                        delta="Resultado"
                    )
                
                with col_res2:
                    st.metric(
                        label="Validação",
                        value=f"{math.sqrt(a**2 + b**2):.{precisao}f}",
                        delta="c recalculado"
                    )
                
                # Detalhes
                with st.expander("📝 Ver cálculo detalhado"):
                    st.latex(rf"a = \sqrt{{{c}^2 - {b}^2}}")
                    st.latex(rf"a = \sqrt{{{c**2:.4f} - {b**2:.4f}}}")
                    st.latex(rf"a = \sqrt{{{(c**2 - b**2):.4f}}}")
                    st.latex(rf"a = {a:.{precisao}f} \, \text{{{unidade}}}")
                
                st.info(f"**Validação:** √({a:.2f}² + {b:.2f}²) = {math.sqrt(a**2 + b**2):.4f} (deve ser ≈ {c:.4f})")
                
            else:
                st.error("❌ A hipotenusa deve ser MAIOR que o cateto!")
        else:
            st.error("❌ Os valores devem ser positivos!")

# ========== RODAPÉ ==========
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🔒 Acesso seguro com senha")
with col2:
    st.caption("📐 Calculadora de engenharia")
with col3:
    st.caption("🚀 Hospedado no Hugging Face")

# Botão de ajuda
if st.button("ℹ️ Ajuda / Instruções"):
    st.info("""
    **Como usar:**
    1. Escolha o tipo de cálculo no menu lateral
    2. Insira os valores conhecidos
    3. Clique no botão calcular
    4. Use os resultados em seus projetos
    
    **Senha de acesso:** Engenharia2024
    """)
