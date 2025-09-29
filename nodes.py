"""
Nós de processamento para o AI Agent - Avaliação de Negócios

Este arquivo contém todas as funções de processamento que representam
os nós do grafo LangGraph.
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any
from functools import lru_cache
from langchain_groq import ChatGroq
from constants import State
from dotenv import load_dotenv

load_dotenv()

# Inicializar o modelo de IA
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.7)


@lru_cache(maxsize=100)
def fetch_website_content(url: str) -> str:
    """
    Extrai o conteúdo textual de uma URL.
    
    Args:
        url: URL do site a ser analisado
        
    Returns:
        str: Conteúdo textual extraído do site
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            return text
        return f"Error: Unable to fetch website content (status {response.status_code})"
    except Exception as e:
        return f"Exception: {str(e)}"


def step_descriptor(state: State) -> dict:
    """
    Nó que gera uma descrição concisa do site analisado.
    
    Args:
        state: Estado atual do processamento
        
    Returns:
        dict: Estado atualizado com a descrição
    """
    content = fetch_website_content(state["url"])
    if content.startswith("Error") or content.startswith("Exception"):
        return {"descricao": content}
    
    snippet = content[:1000]
    prompt = (
        f"Forneça um descritor conciso de uma linha resumindo o conteúdo do site.\n\n"
        f"Trecho do conteúdo:\n{snippet}"
    )
    response_msg = llm.invoke(prompt)
    descriptor = response_msg.content
    return {**state, "descricao": descriptor.strip()}


def step_decision(state: State) -> dict:
    """
    Nó que decide se há informações suficientes para uma avaliação confiável.
    
    Args:
        state: Estado atual do processamento
        
    Returns:
        dict: Estado atualizado com a decisão
    """
    if state["interacoes"] >= 3:
        return {"enough": True}
    
    prompt = (
        f"Com base na seguinte descrição do site:\n'{state['descricao']}'\n"
        f"e os insights adicionais até agora: {', '.join(state['pensamentos']) if state['pensamentos'] else 'Nenhum'}\n"
        "Você tem informações suficientes para avaliar esta ideia de negócio de forma confiável? "
        "Responda com True ou False."
    )
    decision_msg = llm.invoke(prompt)
    decision_text = decision_msg.content
    enough = "True" in decision_text.lower()
    return {**state, "enough": enough}


def step_think_more(state: State) -> dict:
    """
    Nó que gera insights adicionais quando necessário.
    
    Args:
        state: Estado atual do processamento
        
    Returns:
        dict: Estado atualizado com novos insights
    """
    new_iter = state["interacoes"] + 1
    
    # Gerar novo insight
    prompt_insight = (
        f"Descrição do site: '{state['descricao']}'.\n"
        f"Insights existentes: {', '.join(state['pensamentos']) if state['pensamentos'] else 'Nenhum'}.\n"
        "Qual é um insight ou fator adicional que deve ser considerado para avaliar esta ideia de negócio? "
        "Responda em uma frase concisa."
    )
    insight_msg = llm.invoke(prompt_insight)
    new_thought = insight_msg.content.strip()
    updated_thoughts = state["pensamentos"] + [new_thought]
    
    # Gerar tendências de mercado atualizadas
    prompt_trends = (
        f"Com base na descrição do site '{state['descricao']}' e no novo insight '{new_thought}', "
        "forneça um resumo atualizado e breve das tendências de mercado relevantes em uma frase."
    )
    trends_msg = llm.invoke(prompt_trends)
    new_trends = trends_msg.content.strip()
    
    return {
        **state,
        "interacoes": new_iter,
        "pensamentos": updated_thoughts,
        "tendencias_mercado": new_trends
    }


def step_finalize(state: State) -> dict:
    """
    Nó final que gera a avaliação completa do negócio.
    
    Args:
        state: Estado atual do processamento
        
    Returns:
        dict: Estado atualizado com a avaliação final
    """
    prompt = (
        f"Usando a descrição do site:\n'{state['descricao']}'\n"
        f"e os seguintes insights adicionais: {', '.join(state['pensamentos']) if state['pensamentos'] else 'Nenhum'}\n"
        f"com resumo das tendências de mercado: '{state['tendencias_mercado']}'\n"
        "Forneça uma avaliação final do negócio em 3-5 linhas e classifique a ideia de negócio em uma escala de 1 (ruim) a 10 (excelente). "
        "IMPORTANTE: Formate sua resposta EXATAMENTE assim: 'Resumo Final: [sua análise aqui]; Avaliação: [número de 1 a 10]'"
    )

    final_msg = llm.invoke(prompt)
    final = final_msg.content.strip()
    
    # Procurar por diferentes formatos de avaliação
    patterns = [
        r'Avaliação:\s*(\d+)',
        r'Rating:\s*(\d+)',
        r'Nota:\s*(\d+)',
        r'Score:\s*(\d+)',
        r'(\d+)/10',
        r'(\d+)\s*de\s*10',
        r'(\d+)\s*out\s*of\s*10'
    ]
    
    rating = 0
    for pattern in patterns:
        match = re.search(pattern, final, re.IGNORECASE)
        if match:
            rating = int(match.group(1))
            break
    
    # Se não encontrou nenhum padrão, procurar por qualquer número entre 1-10
    if rating == 0:
        numbers = re.findall(r'\b([1-9]|10)\b', final)
        if numbers:
            rating = int(numbers[-1])  # Pega o último número encontrado
    
    return {**state,
        "resposta_final": final,
        "avaliacao": rating}
