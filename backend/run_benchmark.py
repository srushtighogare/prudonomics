import sys
import os
import time
import json

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "data"))

from benchmark_prompts import BENCHMARK_PROMPTS
from providers.groq_provider import call_groq
from cost_calculator import calculate_cost
from executor import execute_request

BASELINE_PROVIDER = "groq"
BASELINE_MODEL = "openai/gpt-oss-120b"

def call_with_retry(prompt, max_retries=3, base_wait=20):
    
    for attempt in range(max_retries):
        try:
            return call_groq(BASELINE_MODEL, prompt), None
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                wait = base_wait * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s before retry {attempt+1}/{max_retries}...")
                time.sleep(wait)
                continue
            else:
                return None, err_str
    return None, "Exceeded max retries due to persistent rate limiting"

def run_baseline(prompts):
    results = []
    for i, prompt in enumerate(prompts):
        print(f"[Baseline {i+1}/{len(prompts)}] {prompt[:50]}...")
        response, error = call_with_retry(prompt)
        if response:
            cost = calculate_cost(BASELINE_PROVIDER, BASELINE_MODEL, response["input_tokens"], response["output_tokens"])
            results.append({"prompt": prompt, "cost": cost, "status": "success"})
        else:
            print(f"  FAILED permanently: {error[:100]}")
            results.append({"prompt": prompt, "cost": None, "status": "failed", "error": error[:200]})
        time.sleep(2)  
    return results

def run_routed(prompts):
    results = []
    for i, prompt in enumerate(prompts):
        print(f"[Routed {i+1}/{len(prompts)}] {prompt[:50]}...")
        result = execute_request(prompt)
        results.append({
            "prompt": prompt,
            "cost": result["cost"],
            "status": result["status"],
            "tier": result["tier"],
            "provider": result["provider"],
        })
        time.sleep(2)
    return results

def main():
    print(f"Running benchmark on {len(BENCHMARK_PROMPTS)} prompts...\n")

    print("=== PHASE A: Baseline (always premium model) ===")
    baseline_results = run_baseline(BENCHMARK_PROMPTS)

    print("\n=== PHASE B: Prudonomics Routed ===")
    routed_results = run_routed(BENCHMARK_PROMPTS)

    # Build a paired comparison: only prompts that succeeded in BOTH runs
    paired = []
    for b, r in zip(baseline_results, routed_results):
        if b["status"] == "success" and b["cost"] is not None and r["cost"] is not None:
            paired.append((b["cost"], r["cost"]))

    baseline_paired_total = sum(p[0] for p in paired)
    routed_paired_total = sum(p[1] for p in paired)
    reduction_pct = ((baseline_paired_total - routed_paired_total) / baseline_paired_total * 100) if baseline_paired_total > 0 else 0

    baseline_failures = sum(1 for r in baseline_results if r["status"] == "failed")
    routed_failures = sum(1 for r in routed_results if r["status"] not in ("success", "fallback_success"))

    summary = {
        "total_prompts_attempted": len(BENCHMARK_PROMPTS),
        "prompts_used_in_paired_comparison": len(paired),
        "baseline_paired_total_cost": round(baseline_paired_total, 8),
        "routed_paired_total_cost": round(routed_paired_total, 8),
        "cost_reduction_pct": round(reduction_pct, 2),
        "baseline_failures_excluded": baseline_failures,
        "routed_failures": routed_failures,
    }

    print("\n" + "=" * 50)
    print("BENCHMARK RESULTS (paired, apples-to-apples comparison)")
    print("=" * 50)
    for k, v in summary.items():
        print(f"{k}: {v}")

    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "benchmark_results.json")
    with open(output_path, "w") as f:
        json.dump({
            "summary": summary,
            "baseline_results": baseline_results,
            "routed_results": routed_results,
        }, f, indent=2)
    print(f"\nFull results saved to {output_path}")

if __name__ == "__main__":
    main()