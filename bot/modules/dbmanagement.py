import openai
import json
import os
from dotenv import load_dotenv
try:
    import summarize
    import dbmanagement as dbm
except:
    import modules.summarize as summarize
    import modules.dbmanagement as dbm


load_dotenv(os.path.join("config", ".env"))
openai.api_key = os.environ.get('OPENAI_API_KEY')
folder = 'chats'


async def load_history(server_id, channel_id, mode):
    if mode == 0: ### Normal History with System Messages
        systemmsg = await dbm.get_config_by_id(server_id, channel_id)
        systemmsg = systemmsg[4]
        checkpoint = await dbm.get_latest_summary(server_id, channel_id)
        checkpoint = checkpoint[4]
        msgpoint = await dbm.get_last_chat(server_id, channel_id)
        print(str(msgpoint))
        msgpoint = msgpoint[8]

        results = await dbm.get_chat_range(server_id, channel_id, checkpoint, msgpoint)

        messages = [{'role': result[5], 'content': result[7]} for result in results]
        messages.insert(0, {'role': 'system', 'content': f'{systemmsg}'})

        summary = await dbm.get_latest_summary(server_id, channel_id)
        summary = summary[3]
        if summary != '':
            messages.insert(1, {'role': 'system', 'content': 'This is the Summary of previous conversations:\n\n' + summary})

        return messages

    if mode == 1: ### Summary Mode without System Messages and Formatted differently
        checkpoint = await dbm.get_latest_summary(server_id, channel_id)
        checkpoint = checkpoint[4]
        msgpoint = await dbm.get_last_chat(server_id, channel_id)
        msgpoint = msgpoint[8]

        results = await dbm.get_chat_range(server_id, channel_id, checkpoint, msgpoint-10)

        messages = ''
        for result in results:
            if result[5] == 'assistant':
                messages += f"Assistant: {result[7]}\n"
            elif result[5] == 'user':
                messages += f"{result[7]}\n"

        return messages


# add optional parameter for mode
async def get_answer(server_id=0, channel_id=0, mode=0, msg=''):
    if mode == 0: ### Normal Mode
        gptversion = await dbm.get_config_by_id(server_id, channel_id)
        gptversion = gptversion[3]
        if gptversion == 3:
            usemodel = "gpt-3.5-turbo"
        elif gptversion == 4:
            usemodel = "gpt-4"

        history = await load_history(server_id, channel_id, 0)

        try:
            answer = openai.ChatCompletion.create(
                model=usemodel,
                messages=history
            )
            answer = answer['choices'][0]['message']['content']

            return answer
        except Exception as e:
            return "Error while trying to use ChatAPI: " + str(e)

    elif mode == 1: ### Summarize Mode
        try:
            answer = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{'role': 'user',
                          'content': f'Please summarize the following conversation: {msg}'}])

            answer = answer['choices'][0]['message']['content']
            return answer
        except Exception as e:
            return "Error while trying to use ChatAPI: " + str(e)

