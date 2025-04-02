import logging


logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщений
    handlers=[
        logging.StreamHandler()  # Вывод в консоль
    ]
)

logger = logging.getLogger(__name__)