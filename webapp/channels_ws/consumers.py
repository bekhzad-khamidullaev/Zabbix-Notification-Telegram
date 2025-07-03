from channels.generic.websocket import JsonWebsocketConsumer


class UpdateConsumer(JsonWebsocketConsumer):
    def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            self.close()
            return
        super().connect()

    def receive_json(self, content):
        action = content.get('action')
        channel = content.get('channel')
        if action == 'subscribe' and channel:
            self.channel_layer.group_add(channel, self.channel_name)
        elif action == 'unsubscribe' and channel:
            self.channel_layer.group_discard(channel, self.channel_name)

    def send_update(self, event):
        self.send_json({"type": event.get('type'), "payload": event.get('data')})
