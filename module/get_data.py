# получить данные с устройства
from requests import post
from typing import List, Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


def get_data(
    session_id: str,
    device_id: str,
    url: str,
    startDate: str,
    endDate: str,
    measurements: str,
) -> Optional[List[Dict[str, Any]]]:
    """
    Получить данные с устройства в указанный промежуток времени.

    Args:
        session_id: id сессии, полученный при успешной аутентификации в auth
        device_id: id устройства (список доступных устройств получен из функции get_devices_list)
        url: url адрес для получения данных
        startDate: начальная дата в формате dd.mm.yy
        endDate: конечная дата в формате dd.mm.yy
        measurements: список измерений с метеостанции (задается в конфиге)

    Returns:
        список доступных устройств и их параметры при успешном выполнении
        none и сообщение об ошибке в иной ситуации
        все статусы записываются в log

    """
    url = url
    headers = {"Cookie": f"JSESSIONID={session_id}", "Content-Type": "application/json"}
    parameters = {
        "deviceId": device_id,
        "startDate": startDate,
        "endDate": endDate,
        "parameters": measurements,
    }

    try:
        logger.debug(
            f"Trying to get data in the session {session_id[:5]}... for the device {device_id}"
        )
        response = post(url, headers=headers, json={}, params=parameters, timeout=180)
        response.raise_for_status()  # для обработки исключения
        data = response.json()
        logger.info(
            f"Data from device {device_id} from {startDate} to {endDate} was successfully received"
        )
        return data

    except Exception as e:
        logger.error(f"Failed to get data: {e}")
        logger.debug(f"Request failed")
        return None
