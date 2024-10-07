from typing import Dict, List, Tuple, Union
from pandas import DataFrame

import numpy as np
from elasticsearch import Elasticsearch

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def elasticsearch(data: DataFrame, *args, **kwargs):
    """
    Exports document data to an Elasticsearch database.
    """

    connection_string = kwargs.get("connection_string", "http://elasticsearch:9200")
    index_name = kwargs.get("index_name", "documents")
    number_of_shards = kwargs.get("number_of_shards", 1)
    number_of_replicas = kwargs.get("number_of_replicas", 0)
    vector_column_name = kwargs.get("vector_column_name", "vector_question_answer")

    dimensions = kwargs.get("dimensions") or None
    if dimensions is None and len(data) > 0:
        first_document = data.iloc[0]
        vector_value = first_document.get(vector_column_name)
        dimensions = len(vector_value) if vector_value is not None else 0

    print(f"Connecting to Elasticsearch at {connection_string}")
    es_client = Elasticsearch(connection_string, timeout=60)  # Increase timeout to 60 seconds
    print(es_client.info())

    index_settings = dict(
        settings=dict(
            number_of_shards=number_of_shards,
            number_of_replicas=number_of_replicas,
        ),
        mappings=dict(
            properties=dict(
                answer=dict(type="text", analyzer="german"),
                question=dict(type="text", analyzer="german"),
                category=dict(type="text", analyzer="german"),
                project_name=dict(type="text", analyzer="german"),
                document_id=dict(type="text"),
                answer_instructions=dict(type="text"),
                source_system=dict(type="keyword"),
                project_id=dict(type="keyword"),
                vector_question_answer=dict(
                    type="dense_vector",
                    dims=dimensions,
                    index=True,
                    similarity="cosine",
                ),
            ),
        ),
    )

    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)

    es_client.indices.create(index=index_name, body=index_settings)
    print("Index created with properties:", index_settings)

    print(f"Indexing {len(data)} data to Elasticsearch index '{index_name}'")
    for idx, row in data.iterrows():
        document_to_index = row.to_dict()
        es_client.index(index=index_name, document=document_to_index)
