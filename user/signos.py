from datetime import datetime

def obter_signo(data_nascimento):
    """
    Retorna o signo do zodíaco com base na data de nascimento.

    :param data_nascimento: String no formato 'DD-MM-YYYY'
    :return: Nome do signo do zodíaco
    """
    signos = [
        ("Capricorn", (1, 1), (1, 19)),
        ("Aquarius", (1, 20), (2, 18)),
        ("Pisces", (2, 19), (3, 20)),
        ("Aries", (3, 21), (4, 19)),
        ("Taurus", (4, 20), (5, 20)),
        ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)),
        ("Leo", (7, 23), (8, 22)),
        ("Virgo", (8, 23), (9, 22)),
        ("Libra", (9, 23), (10, 22)),
        ("Scorpio", (10, 23), (11, 21)),
        ("Sagittarius", (11, 22), (12, 21)),
        ("Capricorn", (12, 22), (12, 31)),
    ]

    # Converter a data de nascimento para um objeto datetime
    try:
        dia, mes, ano = map(int, data_nascimento.split("-"))
        data = datetime(ano, mes, dia)
    except ValueError:
        raise ValueError("Data de nascimento inválida. Use o formato 'DD-MM-YYYY'.")

    # Determinar o signo
    for signo, inicio, fim in signos:
        inicio_data = datetime(data.year, inicio[0], inicio[1])
        fim_data = datetime(data.year, fim[0], fim[1])
        if inicio_data <= data <= fim_data:
            return signo.lower()

    return "Signo não encontrado"