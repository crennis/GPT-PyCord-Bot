import modules.summarize as summarize
import modules.gpt as gpt


history = gpt.load_history('112233445566')

#print(summarize.summarize('112233445566'))

new_string = ''
if history[1]['role'] == 'system':
    new_string += f"System:{history[1]['content']}\n"

for x in history[:-3]:
    if x['role'] == "assistant":
        new_string += f"Assistant: {x['content']}\n"
    elif x['role'] == "user":
        new_string += f"{x['content']}\n"

print(new_string)
print(history[1])

history[1] = {'test'}

print(history)