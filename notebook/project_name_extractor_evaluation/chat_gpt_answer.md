#  Question 1
I am planning to use Hugging Face library. Can you propose how can I extract project_name from the users' questions in order to use them as keywords? Should I have a list of all projects, etc? What should be my actions? Please note, that the questions will be in German, I cannot use models that were designed for English.

#  Answer 1
To extract the `project_name` from user questions in German using the Hugging Face library, there are several strategies you can follow. Since you plan to use Hugging Face, you'll have access to multilingual models that support German, as well as specialized German models.

Here’s how you can approach this:

### 1. **Maintain a List of Project Names**
Yes, maintaining a list of all project names is a crucial step. This list can serve as a reference for identifying project names within user queries. The project names can be stored in a database or a file, and you can update this list as new projects are introduced.

For example:
```json
[
  "Projekt A",
  "Projekt B",
  "Das Haus",
  "The Five"
]
```

You will need to use these project names as keywords to identify which project the user is asking about in their query. Here's the step-by-step plan:

### 2. **Using a German Model for Named Entity Recognition (NER)**

https://huggingface.co/models?language=de&other=named-entity-recognition&sort=modified

Hugging Face provides several pre-trained models that are specifically designed for the German language and include Named Entity Recognition (NER) functionality. You can use these models to extract project names from user questions. Although project names may not always fall under traditional entity categories (like `ORG`, `LOC`, etc.), you can use NER as a first step to extract potential entity candidates.

For example, use the `deepset/gbert-large` or `dbmdz/bert-large-cased-finetuned-conll03-english` models, which support German:

```python
from transformers import pipeline

# Load the German NER model from Hugging Face
ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-german")

# Example question
question = "Was ist der Zinssatz für das Projekt The Five?"

# Apply NER to extract named entities
entities = ner(question)

for entity in entities:
    print(entity)
```

The NER model may identify project names if they resemble named entities (such as organizations). However, NER might not always be perfect for this specific task, so you will likely need additional steps.

### 3. **Fuzzy Matching for Project Name Recognition**
Since project names may not always be recognized by NER, another effective method is **fuzzy string matching**. Once you have a list of project names, you can use libraries like `fuzzywuzzy` or Hugging Face's `datasets` library to perform fuzzy matching between the user’s question and your list of project names.

Here’s how you can implement fuzzy matching:

```python
from fuzzywuzzy import process

# List of project names
projects = ["Projekt A", "Projekt B", "Das Haus", "The Five"]

# User's question
question = "Was ist der Zinssatz für das Projekt The Five?"

# Extract the most likely project from the question using fuzzy matching
project_name, confidence = process.extractOne(question, projects)

print(f"Matched Project: {project_name} with confidence: {confidence}")
```

In this case, you’d extract the project name `"The Five"` from the question and then proceed to query your index based on that result.

### 4. **Keyword-Based Approach**
A simpler approach is to scan the user’s question for keywords that match project names from your list. This approach works well when you have well-defined project names.

Here’s an example:

```python
# List of project names
projects = ["Projekt A", "Projekt B", "Das Haus", "The Five"]

# User's question
question = "Was ist der Zinssatz für das Projekt The Five?"

# Look for exact matches of project names in the question
matched_projects = [project for project in projects if project.lower() in question.lower()]

if matched_projects:
    print(f"Project found: {matched_projects[0]}")
else:
    print("No project found.")
```

This method is faster and simpler but may miss typos or partial matches, which is why combining it with fuzzy matching can be very effective.

### 5. **Train a Custom Model for Project Name Extraction**
If you have sufficient data, you can fine-tune a German transformer model (e.g., BERT, XLM-R, or GPT) to extract project names specifically. You’ll need labeled training data that highlights project names in various sentences. Hugging Face makes it easy to fine-tune models for NER or other tasks using the `Trainer` API.

The workflow would look like this:
1. Label the training data (questions with highlighted project names).
2. Fine-tune a pre-trained German model like `bert-base-german-cased` or `xlm-roberta-large`.
3. Use the fine-tuned model to extract project names.

### 6. **Actionable Steps**

1. **Prepare a List of Project Names**: Create and maintain an up-to-date list of all project names (or project IDs).
2. **Use a Pre-Trained German NER Model**: Try out pre-trained German NER models from Hugging Face and see if they can identify project names from user questions.
3. **Incorporate Fuzzy Matching**: Use fuzzy matching techniques to capture project names, especially when there might be slight variations in spelling or wording in the user query.
4. **Combine Methods**: Combine NER and fuzzy matching approaches for optimal performance. NER will help with more structured entities, while fuzzy matching will catch variations.
5. **Use Hugging Face Pipelines**: Implement the retrieval logic using Hugging Face’s `pipeline` functions for NER and text search.
6. **Future Option – Train a Custom Model**: Fine-tune a custom model for project name extraction if your project grows and you want more precise control over entity recognition.

### 7. **Example Workflow with Fuzzy Matching + NER**
Here’s an example that combines NER and fuzzy matching:

```python
from transformers import pipeline
from fuzzywuzzy import process

# Load NER model
ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-german")

# List of project names
projects = ["Projekt A", "Projekt B", "Das Haus", "The Five"]

# User's question
question = "Was ist der Zinssatz für das Projekt The Five?"

# Step 1: Try to identify named entities
entities = ner(question)

# Step 2: Fuzzy matching for project names
project_name, confidence = process.extractOne(question, projects)

# Combine results
print(f"Entities found: {entities}")
print(f"Fuzzy Matched Project: {project_name} with confidence: {confidence}")
```

By applying both approaches, you increase the chances of accurately extracting the project name from the user's question.

### Conclusion
1. **Maintain a list of all project names** as a reference.
2. Use **NER models** from Hugging Face, preferably multilingual or German-specific models.
3. Employ **fuzzy matching** to enhance project name extraction from questions.
4. Consider fine-tuning a custom model for German question-answer data if you require greater accuracy.

This hybrid approach ensures your system is capable of accurately extracting project names and directing user queries to the correct information.

# Question 2
How to evaluate the function that extracts project names from customer emails? I have a ground truth CSV file that contains the expected project names and the customer email content. What metrics should I use, and what systematic approach should I follow to assess the accuracy and performance of the function?
# Answer 2
Evaluating a function that extracts project names from customer emails requires both **quantitative metrics** and a **systematic approach** to assess its accuracy and performance. Since there is a **ground truth CSV file** containing both the expected project names and the customer email content, we can measure how well the function performs by comparing its outputs with the expected results.

### Step-by-Step Approach

1. **Define the Evaluation Metrics**:
   The most appropriate metrics for this task are:

   - **Accuracy**: Measures how often the function correctly extracts the project name. It's the ratio of correctly identified project names to the total number of cases.
   - **Precision**: Measures the percentage of correctly extracted project names among all names extracted by the function.
   - **Recall**: Measures how many of the actual project names were correctly extracted by the function.
   - **F1 Score**: A harmonic mean of precision and recall, useful when you want a balance between precision and recall.

2. **Approach**:
   - **Extract**: Run the function over the email subjects or bodies to extract the project names.
   - **Compare**: Compare the extracted project names with the ground truth provided in the CSV file.
   - **Evaluate**: Calculate the evaluation metrics based on the comparison results.

### Example in Python Using Pandas

Here’s how you can implement the evaluation process using Python, with a focus on metrics such as accuracy, precision, recall, and F1 score. This example assumes that you have a function `extract_project_name` that extracts the project name from the subject or body of the email.

```python
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Sample CSV Data
data = {
    'source_system': ['evdi', 'evdi'],
    'expected_project_id': ['{54EE27F7-BFB3-49BD-9438-2BE412C8D8A0}', '{54EE27F7-BFB3-49BD-9438-2BE412C8D8A0}'],
    'expected_project_name': ['DFI Zukunftspark Oberfranken VI', 'DFI Zukunftspark Oberfranken VI'],
    'subject': [
        'Welche Sicherheiten bietet das Projekt DFI Zukunftspark Oberfranken VI?',
        'Wie ist die Verzinsung für Investoren im Projekt DFI Zukunftspark Oberfranken VI?'
    ],
    'body': [
        'Können Sie mir bitte mitteilen, welche Sicherheiten im angeboten werden? Es ist mir wichtig zu wissen, wie mein Investment abgesichert wird und ob es zusätzliche Garantien gibt.',
        'Ich interessiere mich für die Verzinsung beim Projekt DFI Zukunftspark Oberfranken VI. Wann beginnt diese und wie hoch ist sie? Gibt es Unterschiede zwischen verschiedenen Investitionssummen?'
    ]
}

# Load the data into a DataFrame
df = pd.DataFrame(data)

# Placeholder function for extracting project name (to be replaced with your actual function)
def extract_project_name(subject, body):
    # Here you will implement your actual logic
    # For simplicity, we assume it finds the project name in the subject.
    # In a real-world case, you would need a more complex pattern matching or NLP extraction method.
    if 'DFI Zukunftspark Oberfranken VI' in subject:
        return 'DFI Zukunftspark Oberfranken VI'
    return None

# Apply the function to extract project names from the emails
df['extracted_project_name'] = df.apply(lambda row: extract_project_name(row['subject'], row['body']), axis=1)

# Ground truth and predictions
y_true = df['expected_project_name']
y_pred = df['extracted_project_name']

# Compute metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='micro')  # Since it's a multiclass problem, we can use 'micro'
recall = recall_score(y_true, y_pred, average='micro')
f1 = f1_score(y_true, y_pred, average='micro')

# Print results
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")
```

### Explanation of Key Parts:

1. **`extract_project_name` Function**:
   This function is a placeholder in the example. You'll need to replace it with the actual logic that extracts project names from the email's subject or body. You might use pattern matching (like regex) or more advanced NLP techniques (such as named entity recognition).

2. **Evaluation Metrics**:
   - **Accuracy**: This tells you how often the function correctly extracts the project name.
   - **Precision**: This is the percentage of correct project names among the extracted names.
   - **Recall**: This measures how many of the ground truth names the function was able to find.
   - **F1 Score**: This gives a balance between precision and recall, important if you care about both false positives and false negatives.

### Next Steps:

- If your function returns **partial names** or names that are similar but not exact (e.g., `DFI Zukunftspark Oberfranken` instead of `DFI Zukunftspark Oberfranken VI`), you might need to consider using **string similarity metrics** like Levenshtein distance.
- If your model is dealing with multiple project names and variants, then you can implement a **ranking evaluation** (like Mean Reciprocal Rank or Mean Average Precision) to assess the quality of retrieval when multiple projects are mentioned.

This approach will give you a comprehensive evaluation of how well your project name extraction function is working!

# Which book or even books can I read to understand  metrics that you used in this example?
To gain a solid understanding of the evaluation metrics used in the example (accuracy, precision, recall, F1 score), you can refer to several key books that cover these concepts in-depth, particularly within the context of machine learning, information retrieval, and natural language processing (NLP). Here’s a curated list of books that explain these metrics in detail:

### 1. **"Pattern Recognition and Machine Learning" by Christopher M. Bishop**
   - **Why this book?**
     - This book is a foundational text in machine learning and covers all essential metrics used for evaluating classification and other predictive tasks, including **accuracy**, **precision**, **recall**, and **F1 score**. It explains both the theoretical underpinnings and practical applications of these metrics.
   - **Key Topics**:
     - Performance metrics for classification models
     - Model evaluation and error analysis
     - Confusion matrix and derivation of precision, recall, and F1 score
   - **Level**: Intermediate to advanced

### 2. **"Introduction to Information Retrieval" by Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze**
   - **Why this book?**
     - This book is specifically focused on information retrieval and text analysis. It provides detailed discussions on metrics like **precision**, **recall**, and **F1 score**, particularly in the context of evaluating retrieval-based systems like the **RAG** system you're working on.
   - **Key Topics**:
     - Precision and recall in the context of search engines and text retrieval
     - Trade-offs between precision and recall, including the F1 score
     - Metrics for ranked retrieval results and systems like yours, including Mean Average Precision (MAP) and Mean Reciprocal Rank (MRR)
   - **Level**: Beginner to intermediate

### 3. **"Speech and Language Processing" by Daniel Jurafsky and James H. Martin**
   - **Why this book?**
     - A comprehensive resource for NLP tasks, this book explains how metrics such as **accuracy**, **precision**, **recall**, and **F1 score** are applied in natural language processing and text-based applications (like extracting project names from emails). It's particularly useful for tasks involving text classification, information extraction, and named entity recognition (NER).
   - **Key Topics**:
     - Evaluation metrics for NLP tasks (precision, recall, F1 score)
     - Text classification, entity recognition, and related applications
     - Statistical methods for language modeling and extraction
   - **Level**: Beginner to intermediate

### 4. **"Evaluating Learning Algorithms: A Classification Perspective" by Nathalie Japkowicz and Mohak Shah**
   - **Why this book?**
     - This book provides a detailed and practical guide to evaluating machine learning algorithms, with a focus on classification problems. It gives a thorough treatment of performance metrics, including **precision**, **recall**, **F1 score**, and how they relate to the specific goals of a learning task.
   - **Key Topics**:
     - Theoretical foundation of evaluation metrics
     - Class imbalance, precision-recall trade-offs, and the relevance of metrics like the F1 score
     - Model validation techniques, including cross-validation
   - **Level**: Intermediate to advanced

### 5. **"The Elements of Statistical Learning" by Trevor Hastie, Robert Tibshirani, and Jerome Friedman**
   - **Why this book?**
     - This is a highly regarded text on machine learning and statistical methods. It covers various methods of evaluating models, including **accuracy**, **precision**, **recall**, and **F1 score**. While it's more technical, it provides the mathematical grounding behind these metrics and their importance in different machine learning tasks.
   - **Key Topics**:
     - Evaluation of classification algorithms and related metrics
     - Bias-variance trade-off and error decomposition
     - Cross-validation and model selection
   - **Level**: Advanced

### 6. **"Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow" by Aurélien Géron**
   - **Why this book?**
     - A more practical and hands-on guide, this book is ideal if you want to learn how to implement these metrics in Python using libraries like **scikit-learn**. It includes examples of how to calculate **accuracy**, **precision**, **recall**, and **F1 score** using real-world datasets and code.
   - **Key Topics**:
     - Practical implementations of evaluation metrics in Python
     - Model evaluation and validation techniques
     - Comprehensive Python code snippets and tutorials
   - **Level**: Beginner to intermediate

---

### **Summary of Recommendations**:
- **Beginner-friendly, practical applications**: 
   - *"Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow"* by Aurélien Géron
   - *"Introduction to Information Retrieval"* by Christopher Manning et al.

- **In-depth theoretical understanding**:
   - *"Pattern Recognition and Machine Learning"* by Christopher Bishop
   - *"The Elements of Statistical Learning"* by Hastie, Tibshirani, Friedman

- **NLP and text-based systems focus**:
   - *"Speech and Language Processing"* by Jurafsky and Martin

These books should give you both the **theoretical knowledge** and **practical skills** needed to understand and effectively use evaluation metrics like **accuracy**, **precision**, **recall**, and **F1 score**, particularly for your work with RAG systems.