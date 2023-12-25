
import os
from fbchat import log, Client, MessageReaction

import pathlib
import textwrap
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-pro')

class AbyssBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        if author_id != self.uid:
            if prompt:
                try:
                    self.reactToMessage(message_object.uid, MessageReaction.YES)
                    response = model.generate_content(prompt)
                    message_object.text = response.text
                    self.send(message_object, thread_id=thread_id, thread_type=thread_type)
                except ValueError:
                    message_object.text = "Prompt blocked, try another one."
                    self.reactToMessage(message_object.uid, MessageReaction.NO)
                    self.send(message_object, thread_id=thread_id, thread_type=thread_type)

client = AbyssBot(os.environ["FB_EMAIL"], os.environ["FB_PASS"])
client.listen()
