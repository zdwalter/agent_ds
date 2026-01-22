import sys

sys.path.insert(0, ".")

from server import ai_suggest_code, analyze_dependencies

# Test analyze_dependencies
print("Testing analyze_dependencies...")
result = analyze_dependencies(".")
print(result)

# Test ai_suggest_code (requires OpenAI API key)
print("\nTesting ai_suggest_code...")
try:
    result = ai_suggest_code("Write a function that adds two numbers in Python")
    print(result)
except Exception as e:
    print(f"Error: {e}")

# Test code_snippet_generate
print("\nTesting code_snippet_generate...")
try:
    from server import code_snippet_generate

    result = code_snippet_generate("for_loop", "python", "iterate over a list")
    print(result)
except Exception as e:
    print(f"Error: {e}")

# Test search_and_replace with parallel option (dry run)
print("\nTesting search_and_replace with parallel...")
try:
    import os
    import tempfile

    from server import search_and_replace

    with tempfile.TemporaryDirectory() as tmpdir:
        # create a test file
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("hello world\nhello there\n")
        result = search_and_replace(tmpdir, "hello", "hi", dry_run=True, parallel=False)
        print(result)
except Exception as e:
    print(f"Error: {e}")
