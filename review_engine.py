import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")

# Define some legal clauses and risky terms
clauses = ['termination', 'indemnity', 'governing law', 'arbitration']
risky_terms = ['irrevocable', 'non-cancellable', 'binding']

def analyze_contract(text):
    doc = nlp(text.lower())
    
    found_clauses = []
    flagged_terms = []

    # Check for legal clauses
    for clause in clauses:
        if clause in text.lower():
            found_clauses.append(clause)

    # Search for risky language
    for token in doc:
        if token.text in risky_terms:
            flagged_terms.append(token.text)

    suggestions = []
    for clause in clauses:
        if clause not in found_clauses:
            suggestions.append(f"Missing clause: {clause.capitalize()}")

    return {
        'found_clauses': found_clauses,
        'flagged_terms': flagged_terms,
        'suggestions': suggestions
    }
