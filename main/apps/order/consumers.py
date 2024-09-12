import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):

    def connect(self):
        self.group_name = 'upload'
        async_to_sync(self.channel_layer.group_add)(self.group_name,
                                                    self.channel_name)
        self.accept()

    # Function to disconnect the Socket
    def disconnect(self, close_code):
        self.close()

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    def notify(self, event):
        self.send(text_data=json.dumps(event["message"]))