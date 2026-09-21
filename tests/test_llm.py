from src.llm import generate_answer


context = """
Python is a high-level programming language.
It is widely used for web development, data science,
machine learning, and automation.
"""

question = "What is Python commonly used for?"

answer = generate_answer(context, question)

print("\nAnswer:")
print(answer)