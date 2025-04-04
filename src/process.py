
from dictor import dictor
import pandas as pd


def unnest_fields (episode: dict) -> dict:
    """
    Unnests relevant fields from a single episode record (TVMaze API response).

    Args:
        episode (dict): Raw nested episode data.

    Returns:
        dict: Flat dictionary with selected episode and show information.
    """

    episode_proc = dict()

    # Extracting Show data related

    episode_proc['show_id'] = dictor(episode, '_embedded.show.id')
    episode_proc['show_name'] = dictor(episode, '_embedded.show.name')
    episode_proc['show_avg_runtime'] = dictor(episode, '_embedded.show.averageRuntime')
    episode_proc['show_official_site'] = dictor(episode, '_embedded.show.officialSite')
    episode_proc['show_genres'] = dictor(episode, '_embedded.show.genres')

    # Extracting episode data related

    episode_proc['episode_id'] = dictor(episode, 'id')
    episode_proc['episode_runtime'] = dictor(episode, 'runtime')
    episode_proc['episode_number'] = dictor(episode, 'number')
    episode_proc['episode_season'] = dictor(episode,'season')
    episode_proc['episode_air_date'] = dictor(episode, 'airdate')

    return episode_proc


def split_dataframe(df: pd.DataFrame):
    """
    Divide the unnested DataFrame into fact and dimension tables.

    Args:
        df (pd.DataFrame): Flat dataframe from unnest_fields.

    Returns:
        Tuple of DataFrames: (fact_episodes, dim_shows, dim_genres, show_genres)
    """

    # Fact Table: This will contain Episodes
    fact_episodes = df[[
        'episode_id', 'episode_runtime', 'episode_number',
        'episode_season', 'episode_air_date', 'show_id'
    ]].drop_duplicates()

    # Dimension Table: Will contain the Shows
    dim_shows = df[[
        'show_id', 'show_name', 'show_avg_runtime',
        'show_official_site'
    ]].drop_duplicates()

    # Dimension Table: Genres (normalized)
    # Explode genres for 1 row per genre-show pair
    exploded = df[['show_id', 'show_genres']].explode('show_genres').dropna()
    exploded = exploded.rename(columns={'show_genres': 'genre_name'})

    # Genre dimension
    dim_genres = exploded[['genre_name']].drop_duplicates().reset_index(drop=True)
    dim_genres['genre_id'] = dim_genres.index + 1  # simple surrogate key

    # Join back to get genre_id: This table will represent a bridge table
    show_genres = exploded.merge(dim_genres, on='genre_name')[['show_id', 'genre_id']].drop_duplicates()

    return fact_episodes, dim_shows, dim_genres, show_genres


def clean_fact_episodes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Args:
        df: DataFrame corresponding to the fact table in this project:  fact episodes

    Returns: DataFrame with cleaned fields
    """
    df = df.dropna(subset=['episode_id', 'show_id']) # Foreign Keys
    df['episode_air_date'] = pd.to_datetime(df['episode_air_date'], errors='coerce')
    df = df.drop_duplicates()

    return df

def clean_dim_shows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Args: DataFrame corresponding to the shows dimension table in this project
        df:

    Returns: DataFrame with cleaned fields
    """

    df = df.dropna(subset=['show_id'])  # Primary Key
    df = df.drop_duplicates()
    df['show_avg_runtime'] = df['show_avg_runtime'].fillna(0)

    return df

def clean_dim_genres(df: pd.DataFrame) -> pd.DataFrame:
    """
    Args:
        df:  DataFrame corresponding to the genres dimension table in this project

    Returns: DataFrame with cleaned fields
    """

    df['genre_name'] = df['genre_name'].str.strip()
    df = df.drop_duplicates()

    return df

def clean_show_genres(df: pd.DataFrame) -> pd.DataFrame:
    """
    Args:
        df: DataFrame corresponding to the show genres table in this project

    Returns: DataFrame with cleaned fields

    """
    df = df.dropna(subset=['show_id', 'genre_id'])
    df = df.drop_duplicates()

    return df


