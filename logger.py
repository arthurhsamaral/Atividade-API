import logging
import sys

def setup_logger(name: str = "api_logger") -> logging.Logger:
    """
    Configura e retorna um logger customizado com saída para arquivo (api.log) e console.
    """
    logger = logging.getLogger(name)
    
    # Previne que o logger adicione múltiplos handlers se for chamado várias vezes
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # File Handler (api.log)
        file_handler = logging.FileHandler("api.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        
        # Stream Handler (Console)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
    return logger

# Instância padrão para ser usada no projeto
logger = setup_logger()
