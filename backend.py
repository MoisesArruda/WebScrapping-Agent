"""
Backend principal do AI Agent - Avaliação de Negócios

Este arquivo contém a lógica principal do grafo LangGraph e a função
de processamento de URLs.
"""

from pprint import pprint
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from constants import State
from nodes import step_descriptor, step_decision, step_think_more, step_finalize
from routes import decision_router

load_dotenv()


def build_graph():
    """
    Constrói o grafo de processamento para avaliação de negócios.
    
    O grafo implementa o seguinte fluxo:
    1. step_descriptor: Extrai e descreve o conteúdo do site
    2. step_decision: Decide se há informações suficientes
    3. step_think_more: Gera insights adicionais (se necessário)
    4. step_finalize: Produz a avaliação final
    
    Returns:
        CompiledGraph: Grafo compilado pronto para execução
    """
    graph_builder = StateGraph(State)
    
    # Adiciona os nós do grafo
    graph_builder.add_node("step_descriptor", step_descriptor)
    graph_builder.add_node("step_decision", step_decision)
    graph_builder.add_node("step_think_more", step_think_more)
    graph_builder.add_node("step_finalize", step_finalize)
    
    # Configura as transições entre nós
    graph_builder.add_edge(START, "step_descriptor")
    graph_builder.add_edge("step_descriptor", "step_decision")
    
    # Roteamento condicional baseado na decisão
    graph_builder.add_conditional_edges(
        "step_decision", 
        decision_router, 
        {
            "step_think_more": "step_think_more", 
            "step_finalize": "step_finalize"
        }
    )
    
    # Loop de volta para decisão após gerar mais insights
    graph_builder.add_edge("step_think_more", "step_decision")
    
    # Finalização do processamento
    graph_builder.add_edge("step_finalize", END)
    
    # Compila e retorna o grafo
    return graph_builder.compile()

def process_url(url: str) -> dict:
    """
    Processa uma URL e retorna o resultado da avaliação de negócio.
    
    Args:
        url: URL do site a ser analisado
        
    Returns:
        dict: Resultado da análise contendo:
            - descriptor: Descrição do negócio
            - thoughts: Lista de insights gerados
            - market_trends: Tendências de mercado identificadas
            - rating: Nota de 1-10
            - final_answer: Resumo final da avaliação
    """
    # Estado inicial do processamento
    initial_state: State = {
        "url": url,
        "descricao": "",
        "tendencias_mercado": "",
        "avaliacao": 0,
        "resposta_final": "",
        "enough": False,
        "interacoes": 0,
        "pensamentos": [],
    }

    # Executa o grafo de processamento
    graph = build_graph()
    final_result = None
    
    for result in graph.stream(initial_state):
        final_result = result
    
    # Formata e retorna o resultado final
    if final_result and 'step_finalize' in final_result:
        state = final_result['step_finalize']
        return {
            "descriptor": state.get("descricao", ""),
            "thoughts": state.get("pensamentos", []),
            "market_trends": state.get("tendencias_mercado", ""),
            "rating": state.get("avaliacao", 0),
            "final_answer": state.get("resposta_final", "")
        }
    else:
        return {
            "descriptor": "Erro no processamento",
            "thoughts": [],
            "market_trends": "",
            "rating": 0,
            "final_answer": "Não foi possível processar a URL fornecida."
        }

if __name__ == "__main__":
    """
    Exemplo de uso do backend.
    """
    # URL de teste
    test_url = "https://example.com"
    
    print("🤖 AI Agent - Teste do Backend")
    print("=" * 40)
    print(f"Testando URL: {test_url}")
    print("Processando...")
    
    # Processar a URL
    result = process_url(test_url)
    
    # Exibir resultado
    print("\n📊 Resultado:")
    pprint(result)
