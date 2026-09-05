from complexity_scorer import score_complexity
from providers.groq_provider import call_groq
from providers.gemini_provider import call_gemini

# Each tier lists (provider, model_name) in priority order.
# First entry = primary choice. Second entry = fallback if primary fails.
TIER_MODELS = {
    "cheap": [
        ("groq", "openai/gpt-oss-20b"),
        ("google", "gemini-3.1-flash-lite"),
    ],
    "premium": [
    ("google", "gemini-3.5-flash"),
    ("groq", "openai/gpt-oss-120b"),
    ],
}

PROVIDER_FUNCTIONS = {
    "groq": call_groq,
    "google": call_gemini,
}

def route_request(prompt: str) -> dict:
    """
    Scores the prompt's complexity, selects a tier, and returns the
    primary and fallback (provider, model) choices along with the
    scoring reasoning -- but does NOT call the LLM yet.
    """
    complexity = score_complexity(prompt)
    tier = complexity["tier"]
    candidates = TIER_MODELS[tier]

    return {
        "tier": tier,
        "complexity_score": complexity["score"],
        "complexity_reasoning": complexity["reasoning"],
        "primary": candidates[0],
        "fallback": candidates[1],
    }