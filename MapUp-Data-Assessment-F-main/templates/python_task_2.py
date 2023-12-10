import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist


def calculate_distance_matrix(df) -> pd.DataFrame():  # type: ignore
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distances = cdist(df[["distance"]], df[["distance"]])

    distances = (distances + distances.T) / 2

    np.fill_diagonal(distances, 0)

    distance_matrix = pd.DataFrame(
        distances, index=df["id_start"], columns=df["id_end"]
    )

    return distance_matrix


def unroll_distance_matrix(df) -> pd.DataFrame():  # type: ignore
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end',
        and 'distance'.
    """
    # Write your logic here
    stacked_df = distance_matrix.stack()

    # Reset the index to turn index labels into columns
    unrolled_df = stacked_df.reset_index()

    # Rename the columns for clarity
    unrolled_df.columns = ["id_start", "id_end", "distance"]

    # Exclude rows where id_start is the same as id_end
    unrolled_df = unrolled_df[unrolled_df["id_start"] != unrolled_df["id_end"]]

    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id) -> pd.DataFrame():  # type: ignore
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                        of the reference ID's average distance.
    """  # noqa: E501
    # Write your logic here

    return df


def calculate_toll_rate(df) -> pd.DataFrame():  # type: ignore
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

    return df


def calculate_time_based_toll_rates(df) -> pd.DataFrame():  # type: ignore
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df


df2 = pd.read_csv("datasets/dataset-3.csv")


distance_matrix = calculate_distance_matrix(df2)
print(distance_matrix)

unroll_matrix = unroll_distance_matrix(distance_matrix)
print(unroll_matrix)
