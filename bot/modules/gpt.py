import openai
import json
import os
from dotenv import load_dotenv
import modules.summarize as summarize
import asyncio

load_dotenv(os.path.join("configs", ".env"))
openai.api_key = os.environ.get('OPENAI_API_KEY')
folder = 'chats'


def load_history(id):
    filename = f'{id}.json'
    try:
        with open(os.path.join(folder, filename), 'r') as f:
            json.load(f)

    except FileNotFoundError as error:
        print(f'File not Found, creating... {error}')
        if id == "199":
            data = 'summarize:'
            setup_history(id, data)
        else:
            data = 'default:'
            setup_history(id, data)

    except json.JSONDecodeError as error:
        os.remove(os.path.join(folder, filename))
        print(f'File is empty, creating... {error}')
        load_history(id)

    with open(os.path.join(folder, filename), 'r') as f:
        f = json.load(f)

    return f

def update_history(id, data):
    filename = f'{id}.json'
    try:
        with open(os.path.join(folder, filename), "r") as f:
            loaded = json.load(f)
        loaded.append(data)

        with open(os.path.join(folder, filename), "w") as f:
            json.dump(loaded, f)

    except Exception as error:
        print(error)

def delete_history(id):
    filename = f'{id}.json'
    try:
        os.remove(os.path.join(folder, filename))
        return "Successfully deleted"
    except Exception as error:
        return error

async def get_answer(id, user, message):
    try:
        history = load_history(id)
        add_history = {"role": "user", "content": f'{user}: {message}'}
        update_history(id, add_history)
        history.append(add_history)
        answer = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history
        )
        answer = answer['choices'][0]['message']['content']
        update_history(id, {"role": "assistant", "content": f"{answer}"})
        if len(history) >= 26:
            await summarize.summarize(id)

        return answer
    except Exception as error:
        return "Error while trying to use ChatAPI: " + str(error)

# def get_answergpt4(id, user, message):
#     try:
#         update_history(id, {"role": "user", "content": f'{user}: {message}'})
#         history = load_history(id)
#         answer = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=history
#         )
#         answer = answer['choices'][0]['message']['content']
#         update_history(id, {"role": "assistant", "content": f"{answer}"})
#         print(len(history))
#         if len(history) >= 23:
#             summarize.summarize(id)
#
#         return answer
#     except Exception as error:
#         return "Error while trying to use ChatAPI " + str(error)

def setup_history(id, message):
    filename = f'{id}.json'

    if message == "summarize":
        message = [{"role": "system", "content": "You summarize conversation. You keep the most important things. Everything else can be removed."}]
    elif message == "default":
        message = [{"role": "system", "content": "You are an helpful assistant. Every Message the user writes starts with their username, the numbers and # must be ignored"}]
    else:
        message = [{"role": "system", "content": f"The Username consists of a name#numbers. The numbers can be ignored. {message}"}]

    # If file exists, delete it
    if os.path.exists(os.path.join(folder, filename)):
        os.remove(os.path.join(folder, filename))
    # Create new file
    with open(os.path.join(folder, filename), "w") as f:
        json.dump(message, f)
