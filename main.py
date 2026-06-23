import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from dotenv import load_dotenv

from schemas import (
    FeatureRequest, 
    FeatureBreakdownResponse, 
    TasksRequest, 
    ComplexityEstimationResponse
)

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "COLOQUE_SUA_CHAVE_AQUI":
    print("AVISO: GEMINI_API_KEY não configurada no arquivo .env!")

app = FastAPI(
    title="Tradutor de Técniques",
    description="API que traduz pedidos de leigos em especificações técnicas para times de desenvolvimento usando IA.",
    version="1.0.0",
    docs_url=None  # Desativa o padrão para usarmos um CDN alternativo
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/swagger-ui.css",
    )

MODEL_NAME = 'gemini-2.5-flash' 
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

async def chamar_gemini(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_URL, headers=headers, json=payload, timeout=60.0)
        
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Erro na API do Gemini: {response.text}")
        
    data = response.json()
    try:
        texto_resposta = data['candidates'][0]['content']['parts'][0]['text']
        # Limpa possível formatação markdown
        texto_resposta = texto_resposta.strip()
        if texto_resposta.startswith("```json"):
            texto_resposta = texto_resposta[7:]
        elif texto_resposta.startswith("```"):
            texto_resposta = texto_resposta[3:]
        if texto_resposta.endswith("```"):
            texto_resposta = texto_resposta[:-3]
        return texto_resposta.strip()
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Formato de resposta inesperado do Gemini.")

@app.post("/projeto/QuebrarTarefas", response_model=FeatureBreakdownResponse)
async def quebrar_tarefas(request: FeatureRequest):
    """
    Recebe uma descrição de uma funcionalidade em linguagem natural e retorna um JSON
    detalhando o passo a passo técnico necessário para Front-end, Back-end e Banco de Dados.
    """
    if not API_KEY or API_KEY == "COLOQUE_SUA_CHAVE_AQUI":
         raise HTTPException(status_code=500, detail="Chave da API do Gemini não configurada no servidor.")

    prompt = f"""
    Você é um arquiteto de software sênior. O cliente pediu a seguinte funcionalidade:
    "{request.descricao}"
    
    Quebre essa funcionalidade em subtarefas técnicas para a equipe de desenvolvimento.
    Seja EXTREMAMENTE OBJETIVO E RESUMIDO. Os detalhes técnicos devem ter, no máximo, 1 ou 2 frases curtas e diretas.
    Classifique cada tarefa na área apropriada (Frontend, Backend, Database).
    
    Retorne APENAS um JSON no seguinte formato (sem markdown):
    {{
        "funcionalidade": "Nome resumido da funcionalidade",
        "tarefas": [
            {{
                "area": "Frontend", 
                "titulo": "Nome da tarefa",
                "detalhes": "O que fazer detalhadamente"
            }}
        ]
    }}
    """
    
    try:
        texto_resposta = await chamar_gemini(prompt)
        result_json = json.loads(texto_resposta)
        return result_json
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="O modelo não retornou um JSON válido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tarefa/EstimarComplexidade", response_model=ComplexityEstimationResponse)
async def estimar_complexidade(request: TasksRequest):
    """
    Recebe uma lista de tarefas técnicas e retorna uma estimativa de complexidade,
    tempo em horas, possíveis riscos e sugestões para reduzir a dificuldade.
    """
    if not API_KEY or API_KEY == "COLOQUE_SUA_CHAVE_AQUI":
         raise HTTPException(status_code=500, detail="Chave da API do Gemini não configurada no servidor.")

    tarefas_json = request.model_dump_json()
    
    prompt = f"""
    Você é um gerente de projetos muito didático, especialista em traduzir jargões técnicos para pessoas leigas. 
    Avalie a seguinte lista de tarefas técnicas (que foi gerada para os desenvolvedores trabalharem):
    {tarefas_json}
    
    Seu objetivo agora é explicar essa estimativa para o cliente leigo (o dono do projeto).
    Avalie a complexidade geral, o tempo, os riscos, pré-requisitos e dê sugestões. 
    ESCREVA TUDO EM UMA LINGUAGEM SIMPLES E DIDÁTICA, sem jargões complexos, usando analogias do dia a dia se necessário, para que qualquer pessoa entenda os desafios envolvidos e como poderia facilitar o trabalho da equipe.
    
    Retorne APENAS um JSON no seguinte formato (sem blocos de markdown):
    {{
        "complexidade": "Baixa, Média ou Alta",
        "tempo_estimado_horas": 20,
        "riscos_e_prerequisitos": ["Explicação simples do risco 1", "Explicação simples do pré-requisito 1"],
        "sugestoes_reducao_complexidade": ["Sugestão didática 1", "Sugestão didática 2"]
    }}
    """
    
    try:
        texto_resposta = await chamar_gemini(prompt)
        result_json = json.loads(texto_resposta)
        return result_json
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="O modelo não retornou um JSON válido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
