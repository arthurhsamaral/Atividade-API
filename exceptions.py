# pyrefly: ignore [missing-import]
from fastapi import HTTPException
from logger import logger

def tratar_erro_gemini(status_code: int, response_text: str):
    """
    Trata erros de status retornados pela API do Gemini, convertendo-os em
    HTTPExceptions apropriadas com mensagens amigáveis em português.
    """
    logger.error(f"Erro recebido da API externa do Gemini: Status {status_code}, Resposta: {response_text}")

    if status_code == 400:
        raise HTTPException(
            status_code=400,
            detail="Requisição inválida enviada para a API do Gemini. Verifique os parâmetros."
        )
    elif status_code == 401:
        raise HTTPException(
            status_code=401, 
            detail="Não autorizado: A chave de API do Gemini é inválida ou expirou. Verifique o arquivo .env."
        )
    elif status_code == 403:
        raise HTTPException(
            status_code=403, 
            detail="Proibido: Acesso negado. A chave de API do Gemini não tem permissão para acessar este recurso."
        )
    elif status_code == 404:
        raise HTTPException(
            status_code=404, 
            detail="Não encontrado: O recurso da API do Gemini (ou o modelo) não foi encontrado."
        )
    elif status_code == 429:
        raise HTTPException(
            status_code=429, 
            detail="Muitas requisições: O limite de cota da API do Gemini foi atingido. Tente novamente mais tarde."
        )
    
    # Qualquer outro erro não esperado da API externa
    raise HTTPException(
        status_code=500, 
        detail=f"Erro na API do Gemini: {response_text}"
    )
