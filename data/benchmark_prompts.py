BENCHMARK_PROMPTS = [
    # Simple / factual (should route cheap)
    "What is the capital of Japan?",
    "What year did World War 2 end?",
    "How many continents are there?",
    "What is the boiling point of water in Celsius?",
    "Who wrote Romeo and Juliet?",

    # Complex / reasoning (should route premium)
   "Analyze the trade-offs between microservices and monolithic architecture, and justify a recommendation for a mid-size startup.",
    "Explain step by step why the time complexity of binary search is O(log n), and compare it to linear search's trade-offs.",
    "Evaluate the pros and cons of remote work versus in-office work for a software engineering team, and justify a hybrid policy.",
    "Analyze the architecture trade-offs between SQL and NoSQL databases for a high-write social media application, and justify a recommendation.",
    "Justify whether a startup should build its own authentication system or use a third-party provider, analyzing the trade-offs.",
]

print(f"Total prompts: {len(BENCHMARK_PROMPTS)}") if __name__ == "__main__" else None