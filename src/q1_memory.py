from typing import List, Tuple
from datetime import datetime
import pandas as pd
from memory_profiler import profile

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

@profile
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """Devuelve las top 10 fechas donde hay más tweet junto con el usuario que más tweets realizó en cada día.

    Args:
        file_path (str): path del archivo que contiene los datos.

    Returns:
        List[Tuple[datetime.date, str]]: lista de tuplas con la fecha y el username del usuario. 
    """
    
    # Lectura de los datos. La estructura de los datos son un objeto JSON por cada fila.
    df = pd.read_json(path_or_buf=file_path, lines=True)

    # Este paso no lo hacemos en q1_time pero acá si para liberar memoria
    # Nos quedamos solo con las columnas necesarias
    cols = ['date', 'id', 'user']

    for col in df.columns:
        if col not in cols:
            df = df.drop(columns=col)

    # El dataframe posee una columna llamada "user". 
    # En esa columna cada registro es un diccionario con información del usuario.
    # Extraemos de el user_id y el username de cada usuario ya que los necesitaremos.
    df['user_id'] = df['user'].apply(extract_user_id)
    df['username'] = df['user'].apply(extract_username)


    # Utilizamos el método columnar de pandas para convertir las fechas de datetime a date.
    # Esto es necesario para luego agrupar por date.
    df['date'] = df['date'].dt.date


    # Obtenemos las top 10 fechas con más tweets y filtramos nuestro df por esas fechas
    top_10_dates = list(df.groupby('date').count().sort_values('id', ascending=False).index[0:10])
    df = df.loc[df.date.isin(top_10_dates)]

    # Creamos una columna llamada "rnk" (rank) para saber cuántos tweets realizó cada usuario en cada día.
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

    # El método to_records() nos permite obtener un array de tuplas de las columnas del dataframe.
    q1_records = df2.to_records(index=False)
    
    # Retornamos solo las columnas solicitadas en el ejercicio.
    return [(row.date, row.username) for row in q1_records]