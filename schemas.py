from pydantic import BaseModel, Field
from typing import List

# --- Endpoint 1 Schemas ---

class FeatureRequest(BaseModel):
    descricao: str = Field(..., description="Descrição em linguagem natural da funcionalidade que deseja criar", example="Criar uma tela de login com autenticação Google")

class SubTask(BaseModel):
    area: str = Field(..., description="Área da tarefa (Frontend, Backend, Database)", example="Frontend")
    titulo: str = Field(..., description="Título resumido da tarefa", example="Criar botão de login com Google")
    detalhes: str = Field(..., description="Descrição detalhada do que precisa ser feito tecnicamente")

class FeatureBreakdownResponse(BaseModel):
    funcionalidade: str
    tarefas: List[SubTask]

# --- Endpoint 2 Schemas ---

class TasksRequest(BaseModel):
    tarefas: List[SubTask] = Field(..., description="Lista de tarefas gerada pelo endpoint de quebra de tarefas")

class ComplexityEstimationResponse(BaseModel):
    complexidade: str = Field(..., description="Complexidade estimada (Baixa, Média, Alta)", example="Média")
    tempo_estimado_horas: int = Field(..., description="Tempo sugerido em horas", example=12)
    riscos_e_prerequisitos: List[str] = Field(..., description="Possíveis riscos ou pré-requisitos técnicos")
    sugestoes_reducao_complexidade: List[str] = Field(..., description="Sugestões de modificações no pedido para reduzir a dificuldade de implementação")
