from src.rag import ask


question = "What is this document about?"

result = ask(question)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(result["answer"])

print("\nSources:")

for source in result["sources"]:
    print(source)