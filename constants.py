from typing import List, Dict, Any
from typing_extensions import TypedDict

class State(TypedDict):
    url: str
    descricao: str
    tendencias_mercado: str
    avaliacao: int
    resposta_final: str
    enough: bool
    interacoes: int
    pensamentos: List[str]