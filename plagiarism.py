from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similarity_score(text1, text2):
    tfidf = TfidfVectorizer().fit_transform([text1, text2])
    return cosine_similarity(tfidf)[0][1]

def plagiarism_check(generated, references, threshold=0.25):
    for ref in references:
        score = similarity_score(generated, ref)
        if score > threshold:
            return True, score
    return False, 0.0
