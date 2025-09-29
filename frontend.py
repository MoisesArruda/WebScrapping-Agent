import streamlit as st
import time
from backend import process_url 
from streamlit_extras.switch_page_button import switch_page
import streamlit.components.v1 as components

# Configuração da página Streamlit
st.set_page_config(
    page_title="AI Agent Avaliação de Negócios",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Variável para imagem da sidebar (pode ser personalizada)
sidebar_image = "data/ArrudaConsulting.jpeg"

def page_config(layout: str = "wide", initial_sidebar_state: str = "auto"):
    """
    Configura a página Streamlit com parâmetros personalizáveis.
    
    Args:
        layout: Layout da página ("wide" ou "centered")
        initial_sidebar_state: Estado inicial da sidebar ("auto", "expanded", "collapsed")
    """
    st.set_page_config(
        page_title="AI Agent Avaliação de Negócios",
        page_icon=sidebar_image,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,        
    )

# Função para configurar a barra lateral
def side_navbar():
    """
    Configura a barra lateral da aplicação Streamlit.
    Esta função adiciona:
    - Título da barra lateral
    - Informações sobre a AInvest
    - Diretrizes de uso
    - Avisos importantes sobre o monitoramento

    Returns:
    None
    """
    # Adicionar imagem se disponível
    if sidebar_image != "Sua imagem aqui":
        st.sidebar.image(image=sidebar_image, width=250, use_container_width=False)
        st.sidebar.markdown("---")
    
    
    st.sidebar.info(
        """Olá, seja bem-vindo! \n\nEu sou um Agente especializado em avaliação de negócios desenvolvido pela Arruda Consulting."""
    )
    
    st.sidebar.markdown("### 📋 Como usar:")
    st.sidebar.markdown("""
    1. Cole a URL do site da startup
    2. Clique em "Processar"
    3. Aguarde a análise completa
    4. Veja a avaliação detalhada
    """)
    
    st.sidebar.markdown("### ⚠️ Avisos:")
    st.sidebar.warning("""
    - Certifique-se de que a URL é válida
    - O processamento pode levar alguns minutos
    - Todos os dados são processados localmente
    """)
    
    st.sidebar.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    
    if st.sidebar.button("🗑️ Limpar histórico", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Configurar a barra lateral
side_navbar()

# Título principal
st.title("🔗 AI Agent - Avaliação de Negócios")
st.markdown("### Analise startups e ideias de negócio com inteligência artificial")
st.markdown("---")

# Seção principal do formulário
with st.form(key='url_form'):
    st.subheader("📝 Insira uma URL para análise")
    
    # Campo de entrada de URL
    url_input = st.text_input(
        "URL da página",
        placeholder="https://exemplo.com",
        help="Cole a URL da página web da startup que você deseja analisar.",
        label_visibility="collapsed"
    )
    
    # Botão de submissão do formulário
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_button = st.form_submit_button(
            label='🚀 Processar Análise', 
            use_container_width=True,
            type="primary"
        )

# Lógica de processamento do formulário
if submit_button:
    if not url_input:
        st.warning("⚠️ Por favor, insira uma URL válida.")
    else:
        # Validação básica de URL
        if not url_input.startswith(('http://', 'https://')):
            url_input = 'https://' + url_input
        
        st.info(f"🔍 Analisando a URL: {url_input}")
        
        # Container para mostrar o progresso
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simular progresso
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 20:
                    status_text.text("📡 Conectando com o site...")
                elif i < 40:
                    status_text.text("📄 Extraindo conteúdo...")
                elif i < 60:
                    status_text.text("🤖 Analisando com IA...")
                elif i < 80:
                    status_text.text("💭 Gerando insights...")
                else:
                    status_text.text("📊 Finalizando avaliação...")
                time.sleep(0.05)
            
            status_text.text("✅ Análise concluída!")
        
        # Processar com o backend real
        try:
            with st.spinner("🔄 Processando análise completa..."):
                result = process_url(url_input)
            
            # Limpar o container de progresso
            progress_container.empty()
            
            st.success("🎉 Análise concluída com sucesso!")
            st.markdown("---")
            
            # Exibição dos resultados
            st.header("📊 Resultado da Análise")
            
            # Layout em duas colunas
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Descrição
                with st.container(border=True):
                    st.subheader("📝 Descrição do Negócio")
                    st.write(result["descriptor"])
                
                # Insights
                if result["thoughts"]:
                    with st.container(border=True):
                        st.subheader("💡 Insights Detalhados")
                        for i, thought in enumerate(result["thoughts"], 1):
                            st.write(f"**{i}.** {thought}")
                
                # Tendências de mercado
                if result["market_trends"]:
                    with st.container(border=True):
                        st.subheader("📈 Tendências de Mercado")
                        st.write(result["market_trends"])
            
            with col2:
                # Avaliação final
                with st.container(border=True):
                    st.subheader("⭐ Avaliação Final")
                    
                    # Métrica da nota
                    rating = result["rating"]
                    if rating >= 8:
                        st.metric("Nota", f"{rating}/10", delta="Excelente", delta_color="normal")
                    elif rating >= 6:
                        st.metric("Nota", f"{rating}/10", delta="Bom", delta_color="normal")
                    elif rating >= 4:
                        st.metric("Nota", f"{rating}/10", delta="Regular", delta_color="off")
                    else:
                        st.metric("Nota", f"{rating}/10", delta="Ruim", delta_color="inverse")
                    
                    # Resposta final
                    if result["final_answer"]:
                        st.markdown("**Resumo:**")
                        st.write(result["final_answer"])
            
            # Seção de ações
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(" ")
            
            with col2:
                if st.button("🔄 Nova Análise", use_container_width=True):
                    st.rerun()
            
            with col3:
                st.markdown(" ")
        
        except Exception as e:
            st.error("❌ Erro ao processar a análise.")
            st.exception(e)
            
            # Botão para tentar novamente
            if st.button("🔄 Tentar Novamente"):
                st.rerun()

# Rodapé
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Desenvolvido por <strong>Arruda Consulting</strong> | Powered by LangGraph & Streamlit</p>
    </div>
    """, 
    unsafe_allow_html=True
)
