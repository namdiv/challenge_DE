from typing import List, Tuple
import pandas as pd
from collections import Counter

def extract_mentioned_users(user_list: list):
    if user_list != None:
        return [e.get('username') for e in user_list]


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


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    mentionedUsers_username = []
    for chunk in pd.read_json(path_or_buf=file_path, lines=True, chunksize=1000):
        users = chunk['mentionedUsers'].apply(extract_mentioned_users)
        mentionedUsers_username.extend(users)

    mentionedUsers_list = []
    for each_list in mentionedUsers_username:
        if each_list is not None:
            mentionedUsers_list += each_list

    return get_most_common_elements(mentionedUsers_list)