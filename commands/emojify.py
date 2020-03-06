from client_interactions import delete_message, send_message

"""
Emojify Command
Converts a message to an emojify letter'd message

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Sends a message always
@result: Deletes a triggering message always
"""
async def command(client, message):
  await delete_message(client, message)
  content = emojify(message.content[9:].lower())
  await send_message(client, message, content)

num2words = {1: ':one:', 2: ':two:', 3: ':three:', 4: ':four:', 5: ':five:', \
             6: ':six:', 7: ':seven:', 8: ':eight:', 9: ':nine:', 0: ':zero:'}

def emojify(string):
  emojiMessage = ''
  for c in string:
    if c.isalpha():
      emojiMessage += ':regional_indicator_' + c + ':'
    elif c.isnumeric():
      emojiMessage += num2words[int(c)]
    else:
      emojiMessage += c
      continue
    
  return emojiMessage

# String that triggers this command
TRIGGER = '!emojify '

def is_triggered(message_content):
  return message_content.lower().startswith(TRIGGER)