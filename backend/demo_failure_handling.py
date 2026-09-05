import router
from executor import execute_request

print("=== BEFORE: normal cheap tier routing ===")
print(router.TIER_MODELS["cheap"])


original_cheap_tier = router.TIER_MODELS["cheap"]
router.TIER_MODELS["cheap"] = [
    ("groq", "this-model-does-not-exist"),  
    original_cheap_tier[1],  
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