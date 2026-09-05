import re

REASONING_KEYWORDS = [
    "analyze", "explain why", "compare", "step by step", "step-by-step",
    "evaluate", "justify", "reasoning", "pros and cons", "trade-off",
    "tradeoff", "architecture", "design", "optimize", "debug", "prove"
]

CODE_INDICATORS = ["```", "def ", "function ", "class ", "import ", "SELECT ", "<html"]

def score_complexity(prompt: str) -> dict:
    """
    Returns a complexity score (0-1) and tier ('cheap' or 'premium')
    along with the reasoning behind the score, for audit logging.
    """
    reasons = []
    score = 0.0

    # Signal 1: length
    length = len(prompt)
    if length > 400:
        score += 0.3
        reasons.append(f"long prompt ({length} chars) (+0.3)")
    elif length > 150:
        score += 0.15
        reasons.append(f"medium-length prompt ({length} chars) (+0.15)")
    else:
        reasons.append(f"short prompt ({length} chars) (+0)")

    # Signal 2: reasoning keywords
    prompt_lower = prompt.lower()
    matched_keywords = [kw for kw in REASONING_KEYWORDS if kw in prompt_lower]
    if matched_keywords:
        score += 0.35
        reasons.append(f"reasoning keywords found: {matched_keywords} (+0.35)")
    else:
        reasons.append("no reasoning keywords found (+0)")

    # Signal 3: code indicators
    matched_code = [c for c in CODE_INDICATORS if c.lower() in prompt_lower]
    if matched_code:
        score += 0.2
        reasons.append(f"code/technical indicators found: {matched_code} (+0.2)")
    else:
        reasons.append("no code indicators found (+0)")

    # Signal 4: multi-part questions
    question_count = prompt.count("?")
    if question_count >= 2:
        score += 0.15
        reasons.append(f"multi-part question ({question_count} '?' marks) (+0.15)")
    else:
        reasons.append(f"single/no question mark ({question_count}) (+0)")

    score = min(score, 1.0)
    tier = "premium" if score >= 0.3 else "cheap"

    return {
        "score": round(score, 2),
        "tier": tier,
        "reasoning": "; ".join(reasons)
    }