import math

def result(query):
    # Simulating search results for different queries
    results = {
        "query1": ["doc1", "doc2", "doc3", "doc4", "doc5"],
        "query2": ["doc3", "doc1", "doc4", "doc2", "doc5"],
        "query3": ["doc2", "doc4", "doc1", "doc5", "doc3"],
        "query4": ["doc1", "doc2", "doc4"],
        "query5": ["doc2", "doc3", "doc1"],
    }
    return results.get(query, [])

def rank(result_list, document):
    try:
        return result_list.index(document) + 1
    except ValueError:
        return math.inf

def rrf_score(document, queries, k=60):
    score = 0.0
    for query in queries:
        result_list = result(query)
        if document in result_list:
            score += 1.0 / (k + rank(result_list, document))
    return score

# Example usage
# queries = ["query1", "query2", "query3"]
queries = ["query4", "query5"]
# documents = ["doc1", "doc2", "doc3", "doc4", "doc5", "doc6"]
documents = ["doc1", "doc2", "doc3", "doc4"]

# Calculate RRF scores for each document
scores = {doc: rrf_score(doc, queries) for doc in documents}

# Sort documents by their RRF scores
ranked_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print("Documents ranked by RRF score:")
for doc, score in ranked_documents:
    print(f"{doc}: {score}")