from router import route_request, PROVIDER_FUNCTIONS
from cost_calculator import calculate_cost

def execute_request(prompt: str) -> dict:
    """
    Full request lifecycle: route -> call LLM (with fallback on failure) ->
    calculate cost -> return everything needed for logging.
    """
    routing = route_request(prompt)
    tier = routing["tier"]

    attempts = [routing["primary"], routing["fallback"]]
    last_error = None
    fallback_triggered = False

    for i, (provider, model_name) in enumerate(attempts):
        try:
            call_fn = PROVIDER_FUNCTIONS[provider]
            response = call_fn(model_name, prompt)

            cost = calculate_cost(
                provider=provider,
                model_name=model_name,
                input_tokens=response["input_tokens"],
                output_tokens=response["output_tokens"]
            )

            return {
                "status": "success" if i == 0 else "fallback_success",
                "tier": tier,
                "complexity_score": routing["complexity_score"],
                "complexity_reasoning": routing["complexity_reasoning"],
                "provider": provider,
                "model": model_name,
                "input_tokens": response["input_tokens"],
                "output_tokens": response["output_tokens"],
                "cost": cost,
                "response_text": response["text"],
                "fallback_triggered": i > 0,
                "error_on_primary": str(last_error) if i > 0 else None,
            }

        except Exception as e:
            last_error = e
            fallback_triggered = True
            continue  # try next in attempts list

    # If we get here, every attempt failed
    return {
        "status": "blocked",
        "tier": tier,
        "complexity_score": routing["complexity_score"],
        "complexity_reasoning": routing["complexity_reasoning"],
        "provider": None,
        "model": None,
        "input_tokens": None,
        "output_tokens": None,
        "cost": None,
        "response_text": None,
        "fallback_triggered": fallback_triggered,
        "error_on_primary": str(last_error),
    }