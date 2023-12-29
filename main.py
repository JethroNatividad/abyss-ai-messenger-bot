import os
from fbchat import log, Client, MessageReaction, TypingStatus
import google.generativeai as genai
from keep_alive import keep_alive

keep_alive()

genai.configure(api_key=os.environ["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-pro')


class AbyssBot(Client):

  def onMessage(self, author_id, message_object, thread_id, thread_type,
                **kwargs):
    self.markAsDelivered(thread_id, message_object.uid)
    self.markAsRead(thread_id)

    if author_id != self.uid:
      try:
        author = client.fetchUserInfo(author_id)[author_id]
        self.reactToMessage(message_object.uid, MessageReaction.HEART)
        client.setTypingStatus(TypingStatus.TYPING,
                               thread_id=thread_id,
                               thread_type=thread_type)

        prompt_parts = [
            "System: You are \"Abyss\" an ai messenger chatbot, your chat starts with \"Abyss: \".",
            "System: Your creator is Jethro Natividad.",
            f"User({author.name}): {message_object.text}"
        ]

        response = model.generate_content(prompt_parts)

        message_object.text = response.text[
            len("abyss: "):] if response.text.casefold().startswith(
                "abyss: ") else response.text

        client.setTypingStatus(TypingStatus.STOPPED,
                               thread_id=thread_id,
                               thread_type=thread_type)
        self.send(message_object, thread_id=thread_id, thread_type=thread_type)
      except ValueError:
        client.setTypingStatus(TypingStatus.STOPPED,
                               thread_id=thread_id,
                               thread_type=thread_type)
        message_object.text = "Prompt blocked, try another one."
        self.reactToMessage(message_object.uid, MessageReaction.NO)
        self.send(message_object, thread_id=thread_id, thread_type=thread_type)


client = AbyssBot(os.environ["FB_EMAIL"], os.environ["FB_PASS"])
client.listen()
