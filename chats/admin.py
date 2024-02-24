from django.contrib import admin

from chats.models import (  # UserChannelChat,
    Channel,
    UserAIChat,
    UserPractitionerChannel,
    UserPractitionerChannelChat,
)


class UserAIchatInline(admin.TabularInline):
    readonly_fields = ["pk"]
    raw_id_fields = ["user"]
    extra = 1
    model = UserAIChat


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_select_related = ["user"]
    raw_id_fields = ["user"]
    list_display = ["user", "trunc_title", "created_at", "updated_at"]
    date_hierarchy = "created_at"
    inlines = [UserAIchatInline]


@admin.register(UserAIChat)
class UserAIChatAdmin(admin.ModelAdmin):
    readonly_fields = ["pk"]
    raw_id_fields = ["channel", "user"]
    list_display = ["trunc_text", "user", "created_at"]
    list_select_related = ["user"]
    search_fields = ["user__email", "user__first_name", "title"]


# class UserChannelChatInlineAdmin(admin.TabularInline):
#     extra = 1
#     model = UserChannelChat
#     list_select_related = ["user", "channel"]
#     raw_id_fields = ["user", "channel"]


# class PractitionerChannelChatInlineAdmin(admin.TabularInline):
#     extra = 1
#     model = PractitionerChannelChat
#     list_select_related = ["practitioner", "channel"]
#     raw_id_fields = ["practitioner", "channel"]


class UserPractitionerChannelChatInlineAdmin(admin.TabularInline):
    extra = 1
    model = UserPractitionerChannelChat
    list_select_related = ["practitioner", "patient", "channel"]
    raw_id_fields = ["practitioner", "patient", "channel"]


@admin.register(UserPractitionerChannel)
class UserPractitionerChannelAdmin(admin.ModelAdmin):
    list_display = ["chat", "id", "created_at"]
    raw_id_fields = ["chat"]
    date_hierarchy = "created_at"
    list_filter = ["created_at"]
    inlines = [UserPractitionerChannelChatInlineAdmin]
    # inlines = [UserChannelChatInlineAdmin, PractitionerChannelChatInlineAdmin]


# @admin.register(UserChannelChat)
# class UserChannelChatAdmin(admin.ModelAdmin):
#     list_display = ["user", "created_at"]
#     date_hierarchy = "created_at"
#     search_fields = ["user__email", "user__first_name", "user__last_name"]
#     list_select_related = ["user", "channel"]
#     raw_id_fields = ["user", "channel"]


# @admin.register(PractitionerChannelChat)
# class PractitionerChannelChatAdmin(admin.ModelAdmin):
#     list_display = ["practitioner", "created_at"]
#     date_hierarchy = "created_at"
#     search_fields = [
#         "practitioner__user__email",
#         "practitioner__user__first_name", "practitioner__user__last_name"
#     ]
#     list_select_related = ["practitioner", "channel"]
#     raw_id_fields = ["practitioner", "channel"]


@admin.register(UserPractitionerChannelChat)
class UserPractitionerChannelChatAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "practitioner",
        "patient",
        "created_at",
    ]
    date_hierarchy = "created_at"
    search_fields = [
        "patient__email",
        "patient__first_name",
        "patient__last_name",
        "practitioner__user__email",
        "practitioner__user__first_name",
        "practitioner__user__last_name",
    ]
    list_select_related = ["practitioner", "patient", "channel"]
    raw_id_fields = ["practitioner", "patient", "channel"]
