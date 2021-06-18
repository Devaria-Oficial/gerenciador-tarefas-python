from datetime import datetime

def validar_data(data, formato_data='%Y-%m-%d'):
    try:
        data = datetime.strptime(data, formato_data)

        return data
    except Exception:
        return None
