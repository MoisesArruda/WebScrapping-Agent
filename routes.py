"""
Funções de roteamento para o AI Agent - Avaliação de Negócios

Este arquivo contém as funções que determinam o fluxo de controle
entre os nós do grafo LangGraph.
"""

from constants import State


def decision_router(state: State) -> str:
    """
    Função de roteamento após o nó de decisão.
    
    Determina se deve continuar gerando insights ou finalizar a avaliação
    baseado no estado atual do processamento.
    
    Args:
        state: Estado atual do processamento
        
    Returns:
        str: Nome do próximo nó a ser executado
            - "step_think_more": Se precisa de mais insights
            - "step_finalize": Se tem informações suficientes
    """
    if state.get("enough", False):
        return "step_finalize"
    return "step_think_more"


def error_router(state: State) -> str:
    """
    Função de roteamento para tratamento de erros.
    
    Determina o próximo passo quando ocorre um erro no processamento.
    
    Args:
        state: Estado atual do processamento
        
    Returns:
        str: Nome do próximo nó a ser executado
    """
    # Se há erro na descrição, finalizar com erro
    if state.get("descricao", "").startswith(("Error", "Exception")):
        return "step_finalize"
    
    # Caso contrário, continuar com decisão
    return "step_decision"


def validate_state(state: State) -> bool:
    """
    Valida se o estado atual é válido para continuar o processamento.
    
    Args:
        state: Estado atual do processamento
        
    Returns:
        bool: True se o estado é válido, False caso contrário
    """
    required_fields = ["url", "descricao"]
    
    for field in required_fields:
        if field not in state or not state[field]:
            return False
    
    return True


def get_next_node(current_node: str, state: State) -> str:
    """
    Função genérica para determinar o próximo nó baseado no nó atual e estado.
    
    Args:
        current_node: Nome do nó atual
        state: Estado atual do processamento
        
    Returns:
        str: Nome do próximo nó a ser executado
    """
    # Mapeamento de nós para próximos nós
    node_mapping = {
        "step_descriptor": "step_decision",
        "step_decision": decision_router(state),
        "step_think_more": "step_decision",
        "step_finalize": "END"
    }
    
    return node_mapping.get(current_node, "step_finalize")
