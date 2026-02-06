import re


def split_clauses(text):
    # split on numbers like 1., 1.1, Clause 2, Article 3
    pattern = r'(?:\n\s*(?:Clause|Article)?\s*\d+(?:\.\d+)*)'

    parts = re.split(pattern, text)

    clauses = []
    for i, part in enumerate(parts):
        clean = part.strip()

        if len(clean) > 40:  # ignore tiny pieces
            clauses.append({
                "id": i + 1,
                "text": clean
            })

    return clauses
