from requests import post
import logging


logger = logging.getLogger(__name__)


def auth(username: str, password: str, url: str) -> str | None:
    """
    Аутентификация пользователя в системе.

    Args:
        username: email пользователя
        password: пароль
        url: адрес для аутентификации

    Returns:
        session Id при успешном выполнении
        none и сообщение об ошибке в иной ситуации
        все статусы записываются в log

    """

    url = url
    data = {"loginType": "email", "login": username, "password": password}
    headers = {"Content-Type": "application/json"}

    try:
        logger.info(f"Attempting authentication for user: {username}")
        response = post(url, json=data, headers=headers, timeout=120)
        response.raise_for_status()  # выбросит исключение для 4xx/5xx статусов
        session_id = response.cookies["JSESSIONID"]
        logger.info("Authentication successful")
        return session_id

    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        logger.debug(f"Request details: URL={url}, username={username}")  # Без пароля!
        return None
