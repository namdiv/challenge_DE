from typing import List, Tuple
from datetime import datetime
import pandas as pd
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

def extract_user_id(dicc: dict):
    """ Función específicamente creada para usar junto al método apply, aplicado a una columna de un
    dataframe de pandas.
    Extrae el id del usuario que viene dentro de la columna user en los datos recibidos.

    Args:
        dicc (dict): diccionario de los datos del usuario.

    Returns:
        int: retorna el id del usuario. 
    """
    return dicc.get('id')

def extract_username(dicc: dict):
    """Función específicamente creada para usar junto al método apply, aplicado a una columna de un
    dataframe de pandas.
    Extrae el username del usuario que viene dentro de la columna user en los datos recibidos.

    Args:
        dicc (dict): diccionario de los datos del usuario.

    Returns:
        str: retorna el username del usuario.
    """
    return dicc.get('username')



def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """Devuelve las top 10 fechas donde hay más tweet junto con el usuario que más tweets realizó en cada día.

    Args:
        file_path (str): path del archivo que contiene los datos.

    Returns:
        List[Tuple[datetime.date, str]]: lista de tuplas con la fecha y el username del usuario. 
    """

    # Lectura de los datos. La estructura de los datos son un objeto JSON por cada fila.
    df = read_json_lines(file_path, cols=['date', 'user', 'id'])

    # Extraemos de el user_id y el username de cada usuario, de la columna "user" ya que los necesitaremos.
    df['user_id'] = df['user'].apply(extract_user_id)
    df['username'] = df['user'].apply(extract_username)

    # Convertimos la columna date de tipo datetime a date.
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date

    # Obtenemos las top 10 fechas con más tweets y filtramos nuestro df por esas fechas
    top_10_dates = df['date'].value_counts().nlargest(10).index
    df = df.loc[df.date.isin(top_10_dates)]

    #Creamos una columna llamada "rnk" (rank) para saber cuántos tweets realizó cada usuario en cada día.
    df['rnk'] = df.groupby(['date', 'user_id']).cumcount()

    #Creamos un nuevo dataframe "df2" en el cual realizamos los siguientes pasos:
    # 1.    Agrupamos por date y user_id y nos quedamos con el máximo valor de rnk. 
    #       De esta forma obtenemos el usuario que mas veces twiteo por día.
    #       ACLARACIÓN IMPORTANTE: podría haber usado el username y no el user_id para ahorrarme un paso,
    #       pero no sería una buena práctica ya que el username no es un identificador único y twitter permite cambiarlo.
    # 
    # 2.    Ordenamos el dataframe de mayor a menor y aplicamos un first() por date. 
    #       Esto nos permite quedarnos con solo un registro por fecha.
    # 
    # 3.    En este paso hacemos un merge con la columna username para obtener el username
    #       del usuario que realizó más tweets.
    #       Además, por las dudas de que algún usuario haya cambiado su username entre esas fechas y obtengamos
    #       registros duplicados, eliminamos el registro duplicado y nos quedamos con el username más reciente.
    #       (esto lo hacemos con el keep='first')

    df2 = df[['date', 'user_id', 'rnk']].\
                        groupby(['date', 'user_id'], as_index=False).max().\
                        sort_values('rnk', ascending=False).\
                        groupby(['date'], as_index=False).first().\
                        sort_values('rnk', ascending=False).\
                        merge(df[['user_id', 'username']].drop_duplicates(keep='first'), how='left', on='user_id')

    q1_records = df2.to_records(index=False)
    
    return [(row.date, row.username) for row in q1_records]

