# AI Agent - Avaliação de Negócios

Uma aplicação completa para análise de startups e ideias de negócio usando inteligência artificial, desenvolvida com Streamlit e LangGraph.

## 🚀 Funcionalidades

- **Análise Automática**: Processa URLs de sites de startups automaticamente
- **Avaliação Inteligente**: Usa IA para gerar insights detalhados sobre o negócio
- **Interface Intuitiva**: Interface moderna e responsiva em Streamlit
- **Processamento em Tempo Real**: Feedback visual durante o processamento
- **Resultados Detalhados**: Descrição, insights, tendências de mercado e avaliação final

## 📋 Pré-requisitos

- Python 3.8+
- Chave API do Groq (para o modelo de IA)

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd WebScrapAgent
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
# Crie um arquivo .env na raiz do projeto
echo "GROQ_API_KEY=sua_chave_api_aqui" > .env
```

## 🎯 Como Usar

1. Execute a aplicação:
```bash
streamlit run frontend.py
```

2. Acesse a aplicação no navegador (geralmente em `http://localhost:8501`)

3. Cole a URL do site da startup que deseja analisar

4. Clique em "Processar Análise" e aguarde os resultados

## 📁 Estrutura do Projeto

```
WebScrapAgent/
├── backend.py          # Grafo principal e função de processamento
├── nodes.py            # Nós de processamento do LangGraph
├── routes.py           # Funções de roteamento do grafo
├── constants.py        # Definições de tipos e constantes
├── frontend.py         # Interface principal em Streamlit
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## 🔧 Componentes Principais

### Backend (backend.py)
- **Grafo Principal**: Construção e execução do grafo LangGraph
- **Função de Processamento**: Interface principal para análise de URLs
- **Integração**: Coordenação entre nós e rotas

### Nós (nodes.py)
- **step_descriptor**: Extração e descrição do conteúdo do site
- **step_decision**: Decisão sobre suficiência de informações
- **step_think_more**: Geração de insights adicionais
- **step_finalize**: Avaliação final com nota de 1-10

### Rotas (routes.py)
- **decision_router**: Roteamento condicional entre nós
- **Validação**: Verificação de estado e tratamento de erros
- **Controle de Fluxo**: Gerenciamento do fluxo de processamento

### Frontend (frontend.py)
- **Streamlit**: Interface web moderna e responsiva
- **Formulários**: Entrada de URL com validação
- **Progresso Visual**: Feedback em tempo real do processamento
- **Resultados**: Exibição organizada dos resultados da análise

## 📊 Fluxo de Processamento

1. **Extração**: Obtém conteúdo do site da URL fornecida
2. **Descrição**: Gera descrição concisa do negócio
3. **Decisão**: Determina se há informações suficientes
4. **Insights**: Gera insights adicionais se necessário
5. **Finalização**: Produz avaliação final com nota de 1-10

## 🎨 Personalização

### Imagem da Sidebar
Para adicionar uma imagem personalizada na sidebar, substitua a variável `sidebar_image` no arquivo `frontend.py`:

```python
sidebar_image = "caminho/para/sua/imagem.png"
```

### Configuração da Página
Use a função `page_config()` para personalizar o layout:

```python
page_config(layout="centered", initial_sidebar_state="collapsed")
```

## 🔒 Segurança

- Todas as URLs são validadas antes do processamento
- Dados processados localmente (não enviados para servidores externos)
- Timeout configurado para requisições web

## 🐛 Solução de Problemas

### Erro de API Key
Certifique-se de que a variável `GROQ_API_KEY` está configurada no arquivo `.env`.

### Erro de Conexão
Verifique sua conexão com a internet e se a URL fornecida é válida.

### Timeout
Para sites grandes, o processamento pode demorar. Aguarde ou tente com uma URL mais simples.

## 📝 Licença

Desenvolvido por **Arruda Consulting** | Powered by LangGraph & Streamlit

## 📞 Suporte

Para suporte técnico, entre em contato com a equipe de desenvolvimento.
