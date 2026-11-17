from rag import load_documents, retrieve, build_context

def test_load_documents():
    assert len(load_documents()) == 6

def test_cancellation_policy_retrieved():
    hits = retrieve("How many hours before an appointment must I cancel?", k=2)
    assert "cancellations.txt" in [name for name, _, _ in hits]

def test_context_includes_source():
    assert "[Source: cancellations.txt]" in build_context([("cancellations.txt", "18 hours", 0.9)])

def test_empty_corpus():
    assert retrieve("question", documents=[]) == []


def test_load_documents_sorts_text_files(tmp_path):
    # Create files out of order, including one that should be ignored.
    (tmp_path / "z.txt").write_text("last", encoding="utf-8")
    (tmp_path / "a.txt").write_text("first", encoding="utf-8")
    (tmp_path / "ignore.md").write_text("ignored", encoding="utf-8")
    # Check both the filename order and the loaded contents.
    assert load_documents(tmp_path) == [("a.txt", "first"), ("z.txt", "last")]


def test_retrieve_sorts_ties_and_limits_results():
    # Identical texts have identical scores, so filenames break the tie.
    documents = [("z.txt", "appointment"), ("a.txt", "appointment")]
    hits = retrieve("appointment", k=1, documents=documents)
    assert [name for name, _, _ in hits] == ["a.txt"]


def test_retrieve_excludes_unrelated_documents():
    # Only the first document shares a word with the question.
    documents = [("match.txt", "cancellation"), ("other.txt", "laboratory")]
    hits = retrieve("cancellation", documents=documents)
    assert [name for name, _, _ in hits] == ["match.txt"]
    assert hits[0][2] > 0  # A returned match must have a positive score.


def test_retrieve_returns_no_matches_for_unknown_words():
    # A question with no shared words should not return zero-score documents.
    assert retrieve("transportation", documents=[("policy.txt", "appointment")]) == []


def test_context_formats_multiple_sources():
    # Each document should have its own source header and text.
    results = [("a.txt", "First policy", 0.9), ("b.txt", "Second policy", 0.5)]
    assert build_context(results) == "[Source: a.txt]\nFirst policy\n\n[Source: b.txt]\nSecond policy"
