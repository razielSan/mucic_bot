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
                    return (None, {"error": f"{result} должно быть меньше или равно {quantity}"})
            return (int(data), {"error": None})
        else:
            return (None, {"error": f"{result} должен быть положительным числом"})
    except Exception:
        return (None, {"error": f"{result} должен быть целым числом"})


