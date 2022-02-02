import requests
import json
from config import CODES, URL, BASE_PARAM, QUOTE_PARAM


class ConversionException(Exception):
    pass


class Converter:

    @staticmethod
    def get_price(base, quote, amount):
        try:
            rate = requests.get(f"{URL}?{BASE_PARAM}={base}&{QUOTE_PARAM}={quote}").content
        except requests.exceptions.RequestException:
            raise ConversionException("Не удалось получить данные о валютах")
        return round(json.loads(rate)[quote] * amount, 2)


class InputParser:

    @staticmethod
    def parse_conversion(input_string):
        input_data = input_string.strip().lower().split()

        if len(input_data) > 3 or len(input_data) < 2:
            raise ConversionException("Неверное количество параметров")

        base = input_data[0]
        quote = input_data[1]

        try:
            base_code = CODES[base]
        except KeyError:
            raise ConversionException(f"Недоступная валюта {base}")

        try:
            quote_code = CODES[quote]
        except KeyError:
            raise ConversionException(f"Недоступная валюта {quote}")

        if base_code == quote_code:
            raise ConversionException("Невозможно перевести валюту саму в себя")

        # Я решил сделать количество необязательным параметром
        if len(input_data) == 3:
            # Что бы отсеять инпут вида NaN или inf решил просто использовть множество
            accepted_characters = {str(x) for x in range(10)}
            accepted_characters.add(".")
            if set(input_data[2]).difference(accepted_characters):
                raise ConversionException("Введено некорректное значение количества")
            try:
                amount = float(input_data[2])
            except ValueError:
                raise ConversionException("Введено некорректное значение количества")
        else:
            amount = 1
        return base, quote, base_code, quote_code, amount
