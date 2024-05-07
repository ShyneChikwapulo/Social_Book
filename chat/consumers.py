import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

from chat.models import ChatMessage, Thread



User = get_user_model()

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room

        # Fetch the logged-in user's profile image URL
        logged_in_user_profile_img_url = await self.get_logged_in_user_profile_img_url(user)


        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept',
            'logged_in_user_profile_img_url': logged_in_user_profile_img_url  # Include profile image URL in the response
        })
    
    @database_sync_to_async
    def get_logged_in_user_profile_img_url(self, user):
        return user.profile.profileimg.url if hasattr(user, 'profile') and user.profile.profileimg else None

    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')

        if not msg:
            print('Error:: empty message')
            return False

        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)
        if not sent_by_user:
            print('Error:: sent by user is incorrect')
        if not send_to_user:
            print('Error:: send to user is incorrect')
        if not thread_obj:
            print('Error:: Thread id is incorrect')

        # Access the related profile object in a synchronous context
        sent_by_user_profile = await sync_to_async(lambda: sent_by_user.profile)()

        # Get the sender's profile image URL
        sender_profile_img_url = sent_by_user_profile.profileimg.url

        print("sender Profile Image URL:", sender_profile_img_url)


        # Access the related profile object in a synchronous context
        send_to_user_profile = await sync_to_async(lambda: send_to_user.profile)()

        # Get the recipient's profile image URL
        recipient_profile_img_url = send_to_user_profile.profileimg.url

        print("recipient Profile Image URL:", recipient_profile_img_url)
        

        await self.create_chat_message(thread_obj, sent_by_user, msg)

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']
        response = {
            'message': msg,
            'sent_by': self_user.id,
            'thread_id': thread_id,
            'sender_profile_img_url': sender_profile_img_url, # Include recipient's profile image URL in the response
            'recipient_profile_img_url': recipient_profile_img_url 
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )
        
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

    async def websocket_disconnect(self, event):
        print('disconnect', event)



    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        ChatMessage.objects.create(thread=thread, user=user, message=msg)
    