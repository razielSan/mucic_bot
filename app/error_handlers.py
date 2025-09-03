from typing import List


def cheak_data_is_number(data: str, year=None, quantity=None, collection=None):
    """Проверяет являются ли количество песен в альбоме или год целым числом."""
    try:
        result = "Год" if year else "Количество песен в альбоме"
        if collection:
            result = "Количество песен в cборнике"
        data = int(data)
        if data > 0:
            if quantity:
                if data > quantity:
                    return (
                        None,
                        {"error": f"{result} должно быть меньше или равно {quantity}"},
                    )
            return (int(data), {"error": None})
        else:
            return (None, {"error": f"{result} должен быть положительным числом"})
    except Exception:
        return (None, {"error": f"{result} должен быть целым числом"})


def chek_data_is_interval(data: str, interval: List):
    """Проверяет является ли число принадлежащим интервалу.
    Возвращает кортеж вида
    (data, {'err': None}) - если число принадлежит интервалу
    (False, {'err': <сообщение об ошибке>}) - если число не принадлежит интервалу

    Args:
        data (str): Данные для проверки вхождения
        interval (List): Интервал представляет из себя список вида
        [0, 30] где число 0 нижний порог вхождения, 30 верхний порог вхождения
    """

    try:
        data = int(data)
        if data >= interval[0] and data <= interval[1]:
            return data, {"err": None}
        else:
            return False, {
                "err": f"Номер песни должен быть в диапазоне от {interval[0]} до {interval[1]}",
            }

    except Exception as err:
        print(err)
        return (False, {"err": "Номер песни должен быть числом"})
