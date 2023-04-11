import json
import os
try:
    import dbmanagement as dbm
    import gpt
except:
    import modules.dbmanagement as dbm
    import modules.gpt as gpt

folder = 'chats'
async def summarize(id):
    filename = f'{id}.json'
    history = gpt.load_history(id)
    new_string = ''
    if history[1]['role'] == 'system':
        new_string += f"System: {history[1]['content']}\n"

    for x in history[:-15]:
        if x['role'] == "assistant":
            new_string += f"Assistant: {x['content']}\n"
        elif x['role'] == "user":
            new_string += f"{x['content']}\n"

    message = f'Please Summarize following Conversation:\n\n{new_string}'

    summarised = await gpt.get_answer('199', '', message)

    new_systemmsg = {'role': 'system', 'content': f'You got the following Summary of previous conversations:\n\n {summarised}'}
    history[1] = new_systemmsg

    history = history[:2] + history[-15:]

    with open(os.path.join(folder, filename), 'w') as f:
        json.dump(history, f)

    os.remove(os.path.join(folder, '199.json'))

    return summarised

async def new_summarize(server_id, channel_id):
    ### Get
    print(f'new_summarize called with {server_id} and {channel_id}')
    history = await gpt.load_history(server_id, channel_id, 1)
    summary = await gpt.get_answer(mode=1, msg=history)
    msgpoint = await dbm.get_last_chat(server_id, channel_id)
    msgpoint = msgpoint[8]
    await dbm.add_summary(server_id, channel_id, summary, msgpoint-10)
