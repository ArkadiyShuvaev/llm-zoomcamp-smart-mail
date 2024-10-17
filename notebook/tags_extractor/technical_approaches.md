# Question 1
1. How can I include tags from the CSV file to the Elasticsearch index?
2. How can I leverage tags to search relevant information using text search?
3. How can I leverage tags to search relevant information using vector search?

# Answer 1
### 1. How can I include tags from the CSV file to the Elasticsearch index?

To include tags from the CSV file in your Elasticsearch index, you need to modify your index mapping to include a field for `tags`. Since the tags are categorical and often used for filtering or searching, you can index them as a `keyword` field. Here's how to adjust your index mapping:

#### Updated Elasticsearch Mapping:

```python
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
            tags=dict(type="keyword"),  # Add this line to include tags
            vector_question_answer=dict(
                type="dense_vector",
                dims=dimensions,
                index=True,
                similarity="cosine",
            ),
        ),
    ),
)
```

When you index a document, ensure the `tags` field from your CSV is included, for example:

```python
doc = {
    "answer": "Antworttext",
    "question": "Fragetext",
    "category": "Zahlungsverzug",
    "project_name": "The Five",
    "document_id": "0113C948-C9CE-4A3D-AF99-D66BDEDE7D33",
    "answer_instructions": "Hinweise",
    "source_system": "evdi",
    "project_id": "0113C948-C9CE-4A3D-AF99-D66BDEDE7D33",
    "tags": ["Zahlungsverzug", "Verzugszinsen"],  # Include the tags here
}
es.index(index="your_index", body=doc)
```

### 2. How can I leverage tags to search relevant information using text search?

To leverage tags for filtering or boosting relevance in text searches, you can modify your `multi_match` query and introduce a filter for `tags`. For instance, you might want to search through text fields but ensure the results are filtered by relevant tags.

#### Updated Text Search Query with Tags:

```python
text_query: Dict[str, Any] = {
    "bool": {
        "must": {
            "multi_match": {
                "query": user_question,
                "fields": ["question^2", "answer^2", "category", "project_name"],
                "type": "best_fields",
            }
        },
        "filter": [
            {"term": {"source_system": self.settings.source_system}},
            *([{"term": {"project_id": str(customer_project_id)}}] if customer_project_id else []),
            *([{"terms": {"tags": user_tags}}] if user_tags else [])  # Adding tag filter here
        ]
    }
}
```

In this case, `user_tags` is the list of tags you want to match, like `["Zahlungsverzug", "Verzugszinsen"]`. This ensures that only documents containing those tags are returned.

Alternatively, you can boost documents based on specific tags using `should` and `boost`:

```python
text_query: Dict[str, Any] = {
    "bool": {
        "must": {
            "multi_match": {
                "query": user_question,
                "fields": ["question^2", "answer^2", "category", "project_name"],
                "type": "best_fields",
            }
        },
        "should": [
            {"terms": {"tags": user_tags, "boost": 2.0}}  # Boost documents with relevant tags
        ],
        "filter": [
            {"term": {"source_system": self.settings.source_system}},
            *([{"term": {"project_id": str(customer_project_id)}}] if customer_project_id else []),
        ]
    }
}
```

### 3. How can I leverage tags to search relevant information using vector search?

When using vector search, you can filter the results based on tags by adding a `terms` filter for the `tags` field in the `filter` section of your `knn_query`.

#### Updated Vector Search Query with Tags:

```python
knn_query: Dict[str, Any] = {
    "field": vector_field_name,
    "query_vector": query_vector,
    "k": number_of_results,
    "num_candidates": 10000,
    "filter": [
        {"term": {"source_system": self.settings.source_system}},
        *([{"term": {"project_id": str(customer_project_id)}}] if customer_project_id else []),
        *([{"terms": {"tags": user_tags}}] if user_tags else [])  # Adding tag filter here
    ],
}
```

Here, `user_tags` is the list of tags you are filtering for. This approach allows you to use both vector similarity for ranking and tags for narrowing down the relevant results.

### Summary of Changes:
1. **Indexing tags**: Add a `tags` field in the index as a `keyword`.
2. **Text search**: Use `terms` to filter or boost by tags in the `text_query`.
3. **Vector search**: Filter vector search results using `terms` with the `tags` field.


# Question 2
follow-up question regarding points 2 and 3.
I do not have "user_tags" to search data. I have a question from the customer that is sent via email.

I thought to use these tags if some words exist in a question from the customer. Or is it a bad idea and I should extract somehow tags from the customer's email? What do you recommend me?

# Answer 2
Great follow-up! You're aiming to automatically leverage tags when customers send questions via email, which means that instead of explicitly getting tags from the user, you'd want to infer them from the content of the customer's email. There are two primary approaches you could take:

### 1. **Extracting Tags from Customer's Email Automatically (Recommended)**
This approach involves using natural language processing (NLP) techniques to automatically extract relevant tags from the email. The idea is to scan the customer's question for keywords or phrases that match or relate to the predefined tags in your system. 

**Steps:**

- **Predefined Tags**: Maintain a set of predefined tags relevant to your domain (e.g., "Zahlungsverzug", "Verzugszinsen", etc.).
- **Keyword Matching**: Use basic keyword matching or phrase detection to assign tags if they appear in the customer’s email.
- **Advanced NLP**: Use more sophisticated NLP techniques such as named entity recognition (NER) or topic modeling to detect relevant concepts in the text. You could also use pre-trained models to categorize the content of the email and assign tags.
  
#### Example of an Approach:
- If the customer's email contains words like *"Verzug"*, *"Zins"*, or *"Zahlung"*, your system could automatically assign the tags like `['Zahlungsverzug', 'Verzugszinsen']`.
  
#### Code Example (Keyword Matching):
Here’s an example of how you could assign tags based on keyword matching from a customer's question.

```python
predefined_tags = {
    "Zahlungsverzug": ["Verzug", "Zahlung", "verspätet", "ausstehend"],
    "Verzugszinsen": ["Zinsen", "Verzugszinsen", "Zinssatz"],
    # Add more tag categories and associated keywords here
}

def extract_tags_from_question(question: str) -> List[str]:
    extracted_tags = []
    for tag, keywords in predefined_tags.items():
        if any(keyword.lower() in question.lower() for keyword in keywords):
            extracted_tags.append(tag)
    return extracted_tags

# Example customer question
customer_question = "Warum habe ich noch keine Zinsen für das Projekt erhalten?"
tags = extract_tags_from_question(customer_question)
print(tags)  # Output: ['Verzugszinsen']
```

#### Why This Works:
- **Automatic Tagging**: You don't rely on customers to provide explicit tags; instead, the system infers tags based on the content of their email.
- **Flexible**: It can evolve as you add more tags or refine your keyword lists.

### 2. **Using Vector Representation for Automatic Tag Inference (Advanced)**
Another approach is to infer tags based on the semantic similarity of the customer's email content to existing question-answer pairs or known tag-related content using **vector search**. You can create vectors for your predefined tags and compute their similarity to the customer's email content.

#### Steps:
- **Pre-trained Language Models**: Use a pre-trained language model (like BERT or Sentence-BERT) to convert the customer's question into a vector.
- **Tag Representation**: Precompute vector representations of your tags or tag-associated questions/answers.
- **Vector Similarity**: Compare the customer question vector with tag vectors using cosine similarity or another similarity metric.
  
#### Example of an Approach (Vector Search with Tags):
- Convert both the email question and the predefined tags into vectors.
- Compute the similarity between the question vector and tag vectors.
- Assign tags with the highest similarity scores.

You could use the `knn_query` you already have in your vector search setup to handle this type of search.

```python
# Assuming you have vector representations for tags:
tags_vectors = {
    "Zahlungsverzug": vector_for_zahlungsverzug,
    "Verzugszinsen": vector_for_verzugszinsen,
    # Add other tag vectors
}

# Query vector for the customer's question
query_vector = get_vector_from_model(customer_question)

# Compute cosine similarity between the question vector and tag vectors
def find_most_similar_tags(query_vector, tags_vectors):
    similarities = {tag: cosine_similarity(query_vector, tag_vector) for tag, tag_vector in tags_vectors.items()}
    # Sort by highest similarity
    return sorted(similarities.items(), key=lambda item: item[1], reverse=True)

# Find top matching tags
similar_tags = find_most_similar_tags(query_vector, tags_vectors)
print(similar_tags)
```

#### Why This Works:
- **Context-Aware**: Vector representations capture the meaning of the text, allowing more accurate matching even if the customer's email doesn’t contain the exact keywords.
- **Scalable**: As you add more content to your system, vector-based search can adapt without the need for extensive keyword lists.

### Comparison of Approaches

| Approach                        | Pros                                               | Cons                                                 |
|----------------------------------|----------------------------------------------------|------------------------------------------------------|
| **Keyword Matching**             | Easy to implement, lightweight, transparent logic  | May miss out on matches if exact keywords aren't used |
| **NLP-based Tag Extraction**     | More sophisticated, captures meaning/context       | More complex to implement, requires NLP expertise     |
| **Vector Search for Tag Inference** | Captures semantic meaning, handles variability in text | Requires vector embeddings and a more advanced setup  |

### Recommendation

Given your setup, I recommend starting with **keyword-based tag extraction**, as it's easy to implement and maintain. Over time, as your system grows, you can layer on **vector-based tag inference** using your existing vector search infrastructure to improve the precision of tag assignment, especially when questions become more diverse in language or structure.