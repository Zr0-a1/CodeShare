# Hardcoded Code Similarity Algorithm

def extract_code(snippet):
    if snippet.code:
        return snippet.code.strip()

    if snippet.file:
        try:
            content = snippet.file.read().decode("utf-8")
            snippet.file.seek(0)
            return content.strip()
        except:
            return ""
    return ""

def normalize_code(code):
    cleaned = []
    multi = False

    for line in code.split("\n"):
        line = line.strip()

        # Detect start of multiline comment
        if "/*" in line:
            multi = True
        if multi:
            if "*/" in line:
                multi = False
            continue

        # Remove single-line comments
        if line.startswith("#") or line.startswith("//"):
            continue
        
        if line:
            cleaned.append(line)

    return " ".join(cleaned)


def simple_similarity(code1, code2):
    set1 = set(code1.split())
    set2 = set(code2.split())

    if not set1 or not set2:
        return 0

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return (intersection / union) * 100


def is_duplicate(snippet, all_snippets, threshold=70):
    """
    Returns True if duplicate found.
    Checks against all snippets except itself.
    """

    new_code = extract_code(snippet)
    new_code = normalize_code(new_code)

    for other in all_snippets:
        if other.id == snippet.id:
            continue
        
        old_code = extract_code(other)
        old_code = normalize_code(old_code)

        score = simple_similarity(new_code, old_code)

        if score >= threshold:
            return True, score, other

    return False, 0, None
