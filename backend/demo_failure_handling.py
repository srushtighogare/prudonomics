import router
from executor import execute_request

print("=== BEFORE: normal cheap tier routing ===")
print(router.TIER_MODELS["cheap"])

# Deliberately break the primary model for the cheap tier
original_cheap_tier = router.TIER_MODELS["cheap"]
router.TIER_MODELS["cheap"] = [
    ("groq", "this-model-does-not-exist"),  # will genuinely fail
    original_cheap_tier[1],  # keep the real fallback (Gemini flash-lite)
]

print("\n=== Forcing a failure on the primary model ===")
print(router.TIER_MODELS["cheap"])

result = execute_request("What is the capital of Germany?")

print("\n=== RESULT ===")
for k, v in result.items():
    print(f"  {k}: {v}")

# Restore normal routing
router.TIER_MODELS["cheap"] = original_cheap_tier
print("\n=== AFTER: routing restored to normal ===")
print(router.TIER_MODELS["cheap"])