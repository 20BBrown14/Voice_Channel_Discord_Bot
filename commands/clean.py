from client_interactions import delete_message, purge_from

"""
Clean Command
Deletes messages from or intended for the bot from the channel the command was invoked in
ex: !clean 50

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Deletes triggering message
@result: Purges messages
"""
async def command(client, message):
  await delete_message(message)
  amount = message.content[7:]
  try:
    amount = int(amount)
  except:
    amount = 5

  def delete_message_check(message):
    client_id = client.user.id
    if (client_id == message.author.id or message.content.startswith('!')):
      return True
    else:
      return False
  await purge_from(client, message, amount, delete_message_check)


# String that triggers this command
TRIGGER = '!clean'

def is_triggered(message_content):
  return message_content.lower().startswith(TRIGGER)