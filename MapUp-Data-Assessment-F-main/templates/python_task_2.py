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

    unrolled_df = stacked_df.reset_index()

    unrolled_df.columns = ["id_start", "id_end", "distance"]

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

    average_distance = unrolled_df.loc[
        unrolled_df["id_start"] == reference_value, "distance"
    ].mean()

    within_threshold = unrolled_df.loc[
        (unrolled_df["id_start"] != reference_value)
        & (
            unrolled_df["distance"].between(
                0.9 * average_distance, 1.1 * average_distance
            )
        ),
        "id_start",
    ].unique()

    result_list = sorted(within_threshold.tolist())

    return result_list


def calculate_toll_rate(df) -> pd.DataFrame():  # type: ignore
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {"moto": 0.8, "car": 1.2, "rv": 1.5, "bus": 2.2, "truck": 3.6}

    result_df = unrolled_df[["id_start", "id_end"]].copy()

    for vehicle_type, rate_coefficient in rate_coefficients.items():
        result_df[vehicle_type] = unrolled_df["distance"] * rate_coefficient

    return result_df


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

unrolled_df = unroll_distance_matrix(distance_matrix)
print(unrolled_df)

reference_value = unrolled_df["id_start"].iloc[0]
result_list = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)
print(result_list)

toll_rate = calculate_toll_rate(unrolled_df)
print(toll_rate)
