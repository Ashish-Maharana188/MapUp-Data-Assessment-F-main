import pandas as pd
import numpy as np


def generate_car_matrix(df) -> pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
        where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    result_df = df.pivot(index="id_1", columns="id_2", values="car")
    result_df = result_df.fillna(0)
    return result_df


def get_type_count(df) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    condition_values = [
        (df["car"] <= 15),
        (df["car"] > 15) & (df["car"] <= 25),
        (df["car"] > 25),
    ]
    choice_values = ["low", "medium", "high"]
    df["car_type"] = pd.Series(
        np.select(condition_values, choice_values, default="unknown"), dtype="category"
    )
    car_type_counts = df["car_type"].value_counts().to_dict()
    car_type_counts = dict(sorted(car_type_counts.items()))
    return car_type_counts


def get_bus_indexes(df) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean_bus = df["bus"].mean()
    index_bus = df[df["bus"] > 2 * mean_bus].index.tolist()
    index_bus.sort()
    return index_bus


def filter_routes(df) -> list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    average_trucks = df.groupby("route")["truck"].mean()
    average_route = average_trucks[average_trucks > 7].unique()
    average_route.sort()

    return average_route


def multiply_matrix(matrix) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
    pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = matrix.copy()
    mask_20 = modified_matrix > 20
    modified_matrix[mask_20] *= 0.75
    modified_matrix[~mask_20] *= 1.25

    modified_matrix = modified_matrix.round(1)

    return modified_matrix


def time_check(df) -> pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the
    timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days
    period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df["start_datetime"] = pd.to_datetime(
        df["startDay"] + " " + df["startTime"], format="%A %H:%M:%S"
    )
    df["end_datetime"] = pd.to_datetime(
        df["startDay"] + " " + df["endTime"], format="%A %H:%M:%S"
    )

    df["duration"] = (df["end_datetime"] - df["start_datetime"]).dt.total_seconds()
    df["day_of_week"] = df["start_datetime"].dt.dayofweek

    is_valid = (df["duration"] == 24 * 60 * 60) & (df["day_of_week"].nunique() == 7)

    final_result = is_valid.groupby([df["id"], df["id_2"]]).all()

    return final_result


# Read_CSV
df = pd.read_csv("datasets/dataset-1.csv")
df2 = pd.read_csv("datasets/dataset-2.csv")


# Fucntion_Calling
result_matrix = generate_car_matrix(df)
print(result_matrix)

car_type_counts = get_type_count(df)
print(car_type_counts)

index_bus = get_bus_indexes(df)
print(index_bus)

average_route = filter_routes(df)
print(average_route)

modified_matrix = multiply_matrix(result_matrix)
print(modified_matrix)

final_result = time_check(df2)
print(final_result)
