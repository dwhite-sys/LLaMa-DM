import ollama
MODEL = 'llama3.2:3B'

output = ollama.generate(MODEL, 'write a short story', stream = True)
print("This can happen")
current = ''
for latest_data in output:
    text_from_data = latest_data['response']
    current += text_from_data
    try:
        context = latest_data['context']  # Only the last chunk has a context. If you this happens, if means it's over.
    except:
        ""
print("This executes when the stream doesn't have any data to give the loop. This is another way to know if it's over")