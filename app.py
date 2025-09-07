from module.auth import auth
from module.get_data import get_data
from module.get_devices_list import get_devices_list
from module.validate_config import validate_config
import logging
from dotenv import dotenv_values
from pathlib import Path
from datetime import date, timedelta
import csv
import os


def main():
    try:

        log_dir = "log"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("log/info.log"),  # запись в файл
                logging.StreamHandler(),  # вывод в консоль
            ],
        )

        logger = logging.getLogger(__name__)

        validate_config(config)

        # получить id сессии
        # 3 раза попробовать
        session_id = None
        for attempt in range(3):
            session_id = auth(username, password, auth_url)
            if session_id:
                break
            logger.warning(f"Authentication attempt {attempt + 1} failed")

        if not session_id:
            raise Exception("Authentication failed after 3 attempts")

        # получить список устройств
        if session_id:
            devices = get_devices_list(session_id, device_url)

        if not devices:
            raise Exception("No devices available")

        if devices:
            params = [
                "id",
                "name",
                "imei",
                "latitude",
                "longitude",
                "lastDataReceivedDt",
            ]
            for i in range(len(devices)):
                print("Доступные устройства:")
                for param in params:
                    print(f"{param}: {devices[i].get(param)}")
        else:
            logger.error("No devices found")
            exit(1)

        # выбор по порядковому номеру
        # первый id устройства для теста
        n = 0
        device_id = devices[n]["id"]

        if device_id:
            data = get_data(
                session_id, device_id, data_url, startDate, endDate, measurements
            )

        if data:
            csv_dir = "csv"
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir)

            with open(
                f"csv/{startDate}_{endDate}.csv",
                "w",
                newline="",
                encoding="utf-8",
            ) as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                logger.info(f"Exported {len(data)} records directly to CSV {file}")

        logger.info("Application completed successfully")

    except Exception as e:
        logger.error(f"Application failed: {e}")
        exit(1)


if __name__ == "__main__":

    # путь к конфигурационному файлу
    env_path = Path("config/.env")
    config = dotenv_values(env_path)

    # получить все необходимые параметры
    username = config.get("USERNAME")
    password = config.get("PASSWORD")
    auth_url = config.get("auth_url")
    device_url = config.get("device_url")
    data_url = config.get("data_url")

    # список необходимых измерений с метеостанции для загрузки
    measurements = config.get("measurements")

    """
    ограничить даты выгрузки: start_day задается в .env
    будут загружаться данные со дня = (сегодня - start_day) до сегодня - 1 (то есть вчерашнего дня)
      
    """
    today = date.today()
    start_day = int(config.get("start_day"))

    startDate = (today - timedelta(days=start_day)).strftime("%d.%m.%Y")
    endDate = (today - timedelta(days=1)).strftime("%d.%m.%Y")

    main()
