from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
import bert_score
from transformers import BertTokenizer, BertModel
import torch

# Cosine Similarity using TF-IDF
def compute_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    cos_sim = cosine_similarity(vectors)
    return cos_sim[0][1]

# Jaccard Similarity
def compute_jaccard_similarity(text1, text2):
    set1 = set(text1.split())
    set2 = set(text2.split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

# BLEU Score with Smoothing
def compute_bleu_score(reference, candidate):
    reference = [reference.split()]
    candidate = candidate.split()
    smoothie = SmoothingFunction().method4
    return sentence_bleu(reference, candidate, smoothing_function=smoothie)

# ROUGE Score
def compute_rouge_score(reference, candidate):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, candidate)
    return scores  # Return all scores for analysis

# BERTScore
def compute_bertscore(reference, candidate):
    P, R, F1 = bert_score.score([candidate], [reference], lang='en', verbose=False)
    return F1.mean().item()

# Cosine Similarity using BERT embeddings
def compute_bert_cosine_similarity(text1, text2):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    inputs1 = tokenizer(text1, return_tensors='pt', truncation=True, max_length=512)
    inputs2 = tokenizer(text2, return_tensors='pt', truncation=True, max_length=512)

    with torch.no_grad():
        outputs1 = model(**inputs1)
        outputs2 = model(**inputs2)

    embedding1 = outputs1.last_hidden_state.mean(dim=1)
    embedding2 = outputs2.last_hidden_state.mean(dim=1)

    cos_sim = cosine_similarity(embedding1.numpy(), embedding2.numpy())[0][0]
    return cos_sim

# Evaluation Function
def evaluate_responses(expected_answer, generated_answer):
    results = {
        'Cosine Similarity (TF-IDF)': compute_cosine_similarity(expected_answer, generated_answer),
        'Jaccard Similarity': compute_jaccard_similarity(expected_answer, generated_answer),
        'BLEU Score': compute_bleu_score(expected_answer, generated_answer),
        'ROUGE Score (ROUGE-L F1)': compute_rouge_score(expected_answer, generated_answer)['rougeL'].fmeasure,
        'BERTScore': compute_bertscore(expected_answer, generated_answer),
        'BERT Cosine Similarity': compute_bert_cosine_similarity(expected_answer, generated_answer)
    }
    
    return results

# Example usage
if __name__ == "__main__":
    expected_answer = "The cat sits on the mat."
    generated_answer = "The cat is sitting on the mat."

    results = evaluate_responses(expected_answer, generated_answer)
    for metric, score in results.items():
        print(f"{metric}: {score:.4f}")
