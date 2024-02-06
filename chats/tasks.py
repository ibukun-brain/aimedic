from aimedic.utils.autogonai_api import AutoGonAI
from chats.models import Channel

autogonai_api = AutoGonAI()


def summarize_channel_title_task(channel_id, channel_title):
    channel = Channel.objects.get(id=channel_id)
    response = autogonai_api.gpt_4(
        message=f"extract a brief title from the following text: {channel_title}"
    )
    channel.title = response
    channel.save()


def chat_ai_task(text, ai_chat_id):
    pass
