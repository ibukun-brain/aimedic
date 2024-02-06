# from django.core.cache import cache
# from django.db.models.signals import post_delete, post_save
# from django.dispatch import receiver

# from chats.models import PractitionerChannelChat, UserChannelChat


# @receiver(post_delete, sender=UserChannelChat, dispatch_uid='post_user_chat_deleted')
# def object_user_chat_post_delete_handler(sender, **kwargs):
#     cache.delete('user_practitioner_channel')


# @receiver(
#     post_delete,
#     sender=PractitionerChannelChat,
#     dispatch_uid='post_practitioner_chat_deleted'
# )
# def object_practitioner_post_delete_handler(sender, **kwargs):
#     cache.delete('user_practitioner_channel')


# @receiver(post_save, sender=UserChannelChat, dispatch_uid='post_user_chat_updated')
# def object_user_chat_post_save_handler(sender, **kwargs):
#     cache.delete('user_practitioner_channel')


# @receiver(
#     post_save,
#     sender=PractitionerChannelChat,
#     dispatch_uid='post_practitioner_chat_updated'
# )
# def object_practitioner_chat_post_save_handler(sender, **kwargs):
#     cache.delete('user_practitioner_channel')
