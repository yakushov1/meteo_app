from requests import post
from typing import List, Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


def get_devices_list(session_id: str, url: str) -> Optional[List[Dict[str, Any]]]:
    """
    Получить список устройств, доступных для пользователя.

    Args:
        session_id: id сессии, полученный при успешной аутентификации в auth
        url: url из документации api для получения списка устройств

    Returns:
        список доступных устройств и их параметры при успешном выполнении
        none и сообщение об ошибке в иной ситуации
        все статусы записываются в log

    """

    url = url
    headers = {"Cookie": f"JSESSIONID={session_id}", "Content-Type": "application/json"}

    try:
        logger.debug(
            f"Requesting devices list with session: {session_id[:5]}..."
        )  # сохранит первые 5 символов id сессии
        response = post(url, headers=headers, json={}, timeout=30)
        response.raise_for_status()
        data = response.json()
        devices_count = len(data.get("data", []))
        logger.info(f"Successfully retrieved {devices_count} devices")
        return data["data"]

    except Exception as e:
        logger.error(f"Failed to get devices list: {e}")
        logger.debug(f"Request failed")
        return None
