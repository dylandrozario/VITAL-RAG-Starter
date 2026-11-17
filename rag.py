"""Student exercise: implement retrieval over the fictional clinic policies."""
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer  # Turn text into TF-IDF vectors.
from sklearn.metrics.pairwise import cosine_similarity  # Compare vectors by their direction.

DOCS = Path(__file__).parent / "knowledge_base"

def load_documents(directory=DOCS):
    """Return list of (filename, text) for *.txt files."""
    # Read each text file in filename order, keeping its name and contents.
    return [(path.name, path.read_text(encoding="utf-8")) for path in sorted(Path(directory).glob("*.txt"))]

def retrieve(question: str, k: int = 2, documents=None):
    """Return top-k (filename, text, score) matches using TF-IDF."""
    documents = load_documents() if documents is None else documents  # Load defaults only when none were supplied.
    if not documents or k <= 0:  # There is nothing to rank or return.
        return []  # Return no matches.
    try:  # Documents without usable words cannot form a vocabulary.
        vectors = TfidfVectorizer().fit_transform([text for _, text in documents] + [question])  # Vectorize the texts and question together.
    except ValueError as exc:  # Handle an empty vocabulary from the vectorizer.
        if "empty vocabulary" not in str(exc):  # Keep unrelated errors visible.
            raise  # Re-raise unexpected errors.
        return []  # No words means no matches.
    scores = cosine_similarity(vectors[-1], vectors[:-1])[0]  # Compare the question with every document.
    results = [(name, text, float(score)) for (name, text), score in zip(documents, scores) if score > 0]  # Keep positive matches.
    results.sort(key=lambda result: (-result[2], result[0]))  # Rank by score, then filename.
    return results[:k]  # Return at most k matches.

def build_context(results):
    """Format hits with [Source: filename] headers."""
    # Put a source header before each document and separate documents with a blank line.
    return "\n\n".join(f"[Source: {name}]\n{text}" for name, text, _ in results)
