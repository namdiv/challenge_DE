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


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    # Este código es el mismo que q2_time.py con la diferencia que leemos los datos en particiones 
    # para ahorrar memoria.
    # Para realizar esto, utilizamos el parámetro chunksize.
    # Por lo tanto, es necesario hacer un bucle "for" y sacrificar procesamiento.
     
    emoji_lists = []
    for chunk in pd.read_json(path_or_buf=file_path, lines=True, chunksize=50):
        emojis = chunk['content'].apply(extract_emojis)
        emoji_lists.extend(emojis) #extend nos permite concatenar listas y almacenar los resultados de cada partición

    # La lista "emojis_list" tiene listas como elementos (es una lista de listas).
    # Con este bucle concatenamos todas las listas en una sola.
    all_emojis = []
    for i in emoji_lists:
        all_emojis += i

    # Retornamos la salida de get_most_common_elements.
    return get_most_common_elements(all_emojis)