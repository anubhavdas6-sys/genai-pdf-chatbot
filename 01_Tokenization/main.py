import tiktoken
enc=tiktoken.encoding_for_model("gpt-4o")

text="My name is Anubhav"
tokens=enc.encode(text)

print("Tokens",tokens)

detokens=enc.decode(tokens)
print("Detokens:",detokens)