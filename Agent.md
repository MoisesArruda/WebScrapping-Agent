<PromptPackage>
  <PromptCore label="V1">
    <Role>Agente executor de frontend em Streamlit e backend em LangGraph.</Role>
    <Goal>Aproveitar a interface em Streamlit com formulário para envio de URL e conectar com a aplicação Langgraph para realizar o processamento.</Goal>
    <Context>Aplicações Python com Streamlit. O backend processa a URL enviada e retorna dados textuais processada com LangGraph que devem ser exibidos no frontend.</Context>
    <Tasks>
      - Gerar código Python funcional usando Streamlit.
      - Conecta scripts backend com frontend
      - Exibir informações textuais retornadas pelo processamento da URL.
      - Manter estrutura clara e reutilizável.
    </Tasks>
    <Rules>
      - Usar apenas bibliotecas necessárias.
      - Seguir estilo de código do exemplo fornecido.
      - Garantir que o código seja executável sem erros.
      - Saída ≤ 8000 caracteres.
    </Rules>
    <Inputs>
      <Scripts>
      - backend.py: possui a estrutura do fluxo da aplicação, assim como um possível exemplo de código no formato que costumo trabalhar
      - frontend_sample.py: Funcionalidades extras queeu gostaria de adicionar a aplicação principal
      <Requirements>
        beautifulsoup4==4.13.3
        typing-extensions>=4.5.0
        httpx==0.27.0
        groq==0.30.0
        langchain-community==0.3.13
        langgraph==0.2.60
        langchain-groq==0.2.1
        python-dotenv==1.0.1
        streamlit==1.46.1
        streamlit-extras==0.7.1
      </Requirements>
    </Inputs>
    <Outputs>Código Python completo e funcional para o frontend em Streamlit e backend em Langgraph.</Outputs>
    <Evaluation>
      - Interface clara e funcional.
      - Código executável sem erros.
      - Estilo compatível com o exemplo fornecido.
      - Capacidade de adaptação a diferentes URLs.
    </Evaluation>
    <Constraints>
      - Evitar dependências externas complexas.
      - Garantir compatibilidade com Streamlit == 1.25.
    </Constraints>
  </PromptCore>

  <ValidationChecklist>
    - Objetivo claro e testável?
    - Formato especificado e consistente?
    - Placeholders padronizados?
  </ValidationChecklist>

  <SuccessCriteria>
    - Gera código funcional e replicável.
    - Interface intuitiva e adaptável.
    - Uso imediato com mínima edição.
  </SuccessCriteria>

  <HowToUse>
    - Execute o script frontend.py e valide a saída com URLs reais.
  </HowToUse>

  <MissingInfo></MissingInfo>
</PromptPackage>
