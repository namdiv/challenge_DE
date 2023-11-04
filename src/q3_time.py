from typing import List, Tuple
import pandas as pd
from collections import Counter
import jsonlines

def read_json_lines(file_path: str, cols: list):
    """Lee un archivo en el cual hay un objeto JSON por línea y devuelve los datos solicitados en un dataframe de pandas.

    Args:
        file_path (str): path del archivo a leer..
        cols (list): lista de "keys" de cada JSON que queremos devolver

    Returns:
        pd.DataFrame: dataframe de pandas con los datos solicitados.
    """
    data = []
    with jsonlines.open(file_path) as reader:
        for item in reader:
            item = {key: item[key] for key in cols if key in item}
            data.append(item)
    return pd.DataFrame(data)

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
    if type(user_list)==list:
        return [e.get('username') for e in user_list]


def q3_time(file_path: str) -> List[Tuple[str, int]]:

    # Lectura de datos.
    df = read_json_lines(file_path=file_path, cols=['mentionedUsers'])

    # Creamos una columna en la que cada registro es una lista con los usuarios mencionados en dicho registro.
    df['mentionedUsers_username'] = df['mentionedUsers'].apply(extract_mentioned_users)

    # Concatenamos todas las menciones en una sola lista, para luego realizar el conteo.
    mentionedUsers_list = []
    for each_list in df.mentionedUsers_username.dropna():
        mentionedUsers_list += each_list

    # Devolvemos la salida de la función get_most_common_elements con los 10 usuarios más mencionados.
    return get_most_common_elements(mentionedUsers_list)