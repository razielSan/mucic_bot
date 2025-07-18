def cheak_data_is_number(data: str, year=None, quantity=None):
    """Проверяет являются ли данные числом."""
    try:
        result = "Год" if year else "Количество песен в альбоме"
        data = int(data)
        if data > 0:
            if quantity:
                if data > 50:
                    print(quantity)
                    return (None, {"error": f"{result} должно быть меньше или равно 50"})
            return (int(data), {"error": None})
        else:
            return (None, {"error": f"{result} должен быть положительным числом"})
    except Exception:
        return (None, {"error": f"{result} должен быть целым числом"})


