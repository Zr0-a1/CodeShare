def calculate_popularity(snippet):
    
    # Popularity score based on views, downloads, and reports.
    # Reports have a reduced penalty for local demo use.
    

    VIEW_WEIGHT = 1
    DOWNLOAD_WEIGHT = 5
    REPORT_WEIGHT = -2  # penality for reports

    score = 0
    score += snippet.views * VIEW_WEIGHT
    score += snippet.downloads * DOWNLOAD_WEIGHT
    score += snippet.reports_count * REPORT_WEIGHT

    if score < 0:
        score = 0

    return score


def rank_snippets(snippets):
    scored = []
    for s in snippets:
        score = calculate_popularity(s)
        scored.append((score, s))

    # Manual sort (descending)
    for i in range(len(scored)):
        for j in range(i + 1, len(scored)):
            if scored[j][0] > scored[i][0]:
                scored[i], scored[j] = scored[j], scored[i]

    return [s for _, s in scored]
