import os
import pandas as pd
from pandas import DataFrame


def get_evaluation_results(results_file_path: str) -> DataFrame:
    """
    Read the evaluation results from a CSV file.

    Parameters:
    - results_file_path (str): The path to the CSV file containing the evaluation results.

    Returns:
    - DataFrame: The evaluation results.
    """

    df: DataFrame

    if os.path.exists(results_file_path):
        df = pd.read_csv(results_file_path, delimiter=";")
    else:
        columns = ["method", "metric", "value", "description", "dataset_version", "created_at"]

        df = pd.DataFrame(columns=columns)

    return df


def add_evaluation_results(results: DataFrame, results_file_path: str) -> None:
    """
    Save the evaluation results to a CSV file.

    Parameters:
    - results (DataFrame): The evaluation results to be saved.

    Examples:
    >>> import pandas as pd
    >>> from datetime import datetime
    >>> results = pd.DataFrame({
    ...     "method": ["reranking_answer_question", "reranking_answer_question", "reranking_question"],
    ...     "metric": ["mrr", "HR@K5", "HR@K3"],
    ...     "value" : ["0.623", "0.812", "0.798"],
    ...     "description": ["reranking using Reciprocal Rank Fusion", "reranking using Reciprocal Rank Fusion", "reranking using Reciprocal Rank Fusion"],
    ...     "dataset_version": ["v1.0", "v1.0", "v1.0"],
    ...     "created_at": [datetime.now(), datetime.now(), datetime.now()]
    ... })
    >>> add_evaluation_results(results, 'evaluation_results.csv')

    Returns:
    - None
    """

    results["created_at"] = results["created_at"].dt.strftime("%Y-%m-%d")

    existing_results = get_evaluation_results(results_file_path)

    # Merge the new results with the existing results, updating existing rows
    updated_results = pd.concat([existing_results, results]).drop_duplicates(
        subset=["method", "metric", "dataset_version", "created_at"], keep='last'
    ).reset_index(drop=True)

    updated_results.to_csv(results_file_path, sep=";", index=False)
