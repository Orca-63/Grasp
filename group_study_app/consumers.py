from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404, redirect
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import json


class ChatRoomConsumer(WebsocketConsumer):

    def connect(self):
        from .models import ChatGroup
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(
            ChatGroup, group_name=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()

    def receive(self, text_data):
        from .models import GroupMessage
        text_data_json = json.loads(text_data)

        text_body = text_data_json.get('text_body', '').strip()
        latex_body = text_data_json.get('latex_body', '').strip()

        # Prioritize latex if present
        body = latex_body if latex_body else text_body

        if body:
            message = GroupMessage.objects.create(
                body=body,
                author=self.user,
                group=self.chatroom,
                message_type='latex' if latex_body else 'text'  # Optional, if you track type
            )
            event = {
                'type': 'message_handler',
                'message_id': message.id,
            }
            async_to_sync(self.channel_layer.group_send)(
                self.chatroom_name, event
            )

    def message_handler(self, event):
        from .models import GroupMessage
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
            'chat_group': self.chatroom
        }
        html = render_to_string(
            "group_study_app/partials/chat_message_p.html", context=context)
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1

        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

    def online_count_handler(self, event):
        online_count = event['online_count']
        from .models import ChatGroup
        chat_messages = ChatGroup.objects.get(
            group_name=self.chatroom_name).chat_messages.all()[:30]
        author_ids = set([message.author.id for message in chat_messages])
        from .models import User
        users = User.objects.filter(id__in=author_ids)

        context = {
            'online_count': online_count,
            'chat_group': self.chatroom,
            'users': users
        }
        html = render_to_string(
            "group_study_app/partials/online_count.html", context)
        self.send(text_data=html)

    @login_required
    def get_or_create_chatroom(request, username):
        from .models import ChatGroup
        if request.user.username == username:
            return redirect('home')
        from .models import User
        other_user = User.objects.get(username=username)
        my_chatrooms = request.user.chat_groups.filter(is_private=True)

        if my_chatrooms.exists():
            for chatroom in my_chatrooms:
                if other_user in chatroom.members.all():
                    chatroom = chatroom
                    break
                else:
                    chatroom = ChatGroup.objects.create(is_private=True)
                    chatroom.members.add(other_user, request.user)
        else:
            chatroom = ChatGroup.objects.create(is_private=True)
            chatroom.members.add(other_user, request.user)

        return redirect('chatroom', chatroom.group_name)
