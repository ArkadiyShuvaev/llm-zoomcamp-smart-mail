from sentence_transformers import SentenceTransformer
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: DataFrame, *args, **kwargs) -> DataFrame:
    
    model_name = kwargs['embeddings_model_name']
    model = SentenceTransformer(model_name)
  
    
    batch_size = kwargs.get('batch_size', 100)
    embeddings = []

    for i in range(0, len(data), batch_size):
        batch = data.iloc[i:i + batch_size]
        question_answer_pairs = (batch["question"] + " " + batch["answer"]).tolist()
        batch_vectors = model.encode(question_answer_pairs)
        
        # Append embeddings to the list
        embeddings.extend(batch_vectors)

    data['vector_question_answer'] = embeddings
    return data
    


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'