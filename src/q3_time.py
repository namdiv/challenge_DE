from typing import List, Tuple
import pandas as pd
from collections import Counter

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

def extract_mentioned_users(user_list: list):
    """Extrae los usernames de la lista de diccionarios que trae la columna mentionedUsers.

    Args:
        user_list (list): lista de diccionarios de los usuarios mencionados.

    Returns:
        list: lista con los nombres (str) de los usuarios mencionados.
    """
    if user_list != None:
        return [e.get('username') for e in user_list]


def q3_time(file_path: str) -> List[Tuple[str, int]]:

    # Lectura de datos.
    df = pd.read_json(path_or_buf=file_path, lines=True)

    # Creamos una columna en la que cada registro es una lista con los usuarios mencionados en dicho registro.
    df['mentionedUsers_username'] = df['mentionedUsers'].apply(extract_mentioned_users)

    # Concatenamos todas las menciones en una sola lista, para luego realizar el conteo.
    mentionedUsers_list = []
    for each_list in df.mentionedUsers_username.dropna():
        mentionedUsers_list += each_list

    # Devolvemos la salida de la función get_most_common_elements con los 10 usuarios más mencionados.
    return get_most_common_elements(mentionedUsers_list)


if __name__=='__main__':
    print(q3_time('../farmers-protest-tweets-2021-2-4.json'))