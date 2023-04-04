# from TTS.api import TTS
# import uuid
# import os
# import asyncio
#
# # Use Model tts_models/de/thorsten/tacotron2-DCA
# # coqui-ai
#
# async def generate_audio(text):
#     loop = asyncio.get_event_loop()
#     folder = "audio"
#     filename = f"{uuid.uuid4().hex}.wav"
#     path = os.path.join(folder, filename)
#
#     try:
#         def tts_to_file_blocking():
#             tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=True, gpu=False)
#             tts.tts_to_file(text=text, file_path=path)
#
#         await loop.run_in_executor(None, tts_to_file_blocking)
#         return path
#     except Exception as e:
#         print(e)
#         return str(e)
