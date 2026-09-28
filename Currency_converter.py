from datetime import datetime
import requests


def get_combined_exchange_rates():
    frankfurter_url = "https://api.frankfurter.app/latest?to=USD"

    exchangerate_url = "https://open.er-api.com/v6/latest/USD"

    try:
        resp_frank = requests.get(frankfurter_url, timeout=10)
        resp_frank.raise_for_status()
        data_frank = resp_frank.json()

        eur_to_usd = data_frank.get("rates", {}).get("USD")

        if not eur_to_usd:
            print("Ошибка: Frankfurter API не вернул курс USD.")
            return

        resp_er = requests.get(exchangerate_url, timeout=10)
        resp_er.raise_for_status()
        data_er = resp_er.json()

        usd_to_rub = data_er.get("rates", {}).get("RUB")

        if not usd_to_rub:
            print("Ошибка: ExchangeRate-API не вернул курс RUB.")
            return

        eur_to_rub = eur_to_usd * usd_to_rub

        fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Актуальный курс валют на {fetch_time}")
        print(f"1 USD = {usd_to_rub:.2f} RUB (данные ExchangeRate-API)")
        print(f"1 EUR = {eur_to_rub:.2f} RUB (кросс-курс через Frankfurter)")

    except requests.exceptions.RequestException as error:
        print(f"Безопасная остановка. Ошибка сети: {error}")
    except ValueError:
        print("Безопасная остановка. Получены некорректные данные от сервера (не JSON).")


if __name__ == "__main__":
    get_combined_exchange_rates()