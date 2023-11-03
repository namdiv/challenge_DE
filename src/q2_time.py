from typing import List, Tuple
import pandas as pd
from collections import Counter
import emoji

def get_most_common_elements(elements: list, n:int =10):
    """Extrae los n elementos más comunes de una lista junto con su respectivo conteo.

    Args:
        elements (list): lista de elementos que deseamos contar.
        n (int, optional): cantidad de elementos que deseamos obtener. Devuelve los 10 más comunes por defecto.

    Returns:
        list: lista de tuplas con los elementos más comunes y su conteo. Ejemplo [(elem1, 15), (elem2, 12), (elem3, 7),...]
    """
    _counter = Counter(elements)
    most_common_elements = _counter.most_common(n)
    return most_common_elements

def extract_emojis(text: str):
    """Extrae los emojis contenido en un string. Los emojis son identificados por la librería emoji.

    Args:
        text (str): texto que contiene los emojis que queremos extraer.

    Returns:
        list: lista con los emojis extraídos. Cada elemento corresponde a un emoji.
    """
    return [e.get('emoji') for e in emoji.emoji_list(text)]


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    # Lectura de los datos. La estructura de los datos son un objeto JSON por cada fila.
    df = pd.read_json(path_or_buf=file_path, lines=True)

    # Aplicamos la función extract_emojis en cada registro de la columna content.
    # La columna content representa el contenido (texto) del tweet. Por lo tanto, 
    # es la que nos interesa y en donde estarán los emojis.
    emojis = df['content'].apply(extract_emojis)

    # La lista "emojis" tiene listas como elementos (es una lista de listas).
    # Con este bucle concatenamos todas las listas en una sola.
    emojis_list = []
    for i in emojis:
        emojis_list += i

    # Retornamos la salida de get_most_common_elements.
    return get_most_common_elements(emojis_list)