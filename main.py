import os
from JethroNatividad_fbchat import log, Client, MessageReaction, TypingStatus
import google.generativeai as genai

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
        self.setTypingStatus(TypingStatus.TYPING,
                             thread_id=thread_id,
                             thread_type=thread_type)

        # Initial Prompts
        prompt_parts = [
            "System: You are \"Abyss\" an ai messenger chatbot, your chat starts with \"Abyss: \".",
            "System: Your creator is Jethro Natividad.",
        ]

        messages = client.fetchThreadMessages(thread_id=thread_id, limit=12)
        messages.reverse()

        # Find messages that are "Let's switch to another topic, shall we?", then remove all messages before that.

        for message in messages:
          if message.text.startswith("Let's switch to another topic, shall we?"
                                     ) and message.author == self.uid:
            messages = messages[messages.index(message):]
            break

        # Construct Message History
        for message in messages:
          if message.author == self.uid:
            prompt_parts.append(f"Abyss: {message.text}")
          else:
            prompt_parts.append(f"User({author.name}): {message.text}")

        prompt_parts.append(f"User({author.name}): {message_object.text}")

        response = model.generate_content(prompt_parts)

        message_object.text = response.text[
            len("abyss: "):] if response.text.casefold().startswith(
                "abyss: ") else response.text

        self.send(message_object, thread_id=thread_id, thread_type=thread_type)

        self.setTypingStatus(TypingStatus.STOPPED,
                             thread_id=thread_id,
                             thread_type=thread_type)

      except ValueError:
        message_object.text = "Let's switch to another topic, shall we?"
        self.send(message_object, thread_id=thread_id, thread_type=thread_type)
        self.reactToMessage(message_object.uid, MessageReaction.NO)

        self.setTypingStatus(TypingStatus.STOPPED,
                             thread_id=thread_id,
                             thread_type=thread_type)

      except Exception as e:
        print(e)
        message_object.text = "Oops! An error occurred. Please resend your message or try again later."
        self.reactToMessage(message_object.uid, MessageReaction.SAD)
        self.send(message_object, thread_id=thread_id, thread_type=thread_type)

        self.setTypingStatus(TypingStatus.STOPPED,
                             thread_id=thread_id,
                             thread_type=thread_type)


client = AbyssBot(os.environ["FB_EMAIL"], os.environ["FB_PASS"])
client.listen()
