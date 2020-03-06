# GOOGLE COMMAND NOT IN USE

"""
Google command
Description

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param other_args: Whatever other args that are passed into this template
@result: sends a message on...
@result: deletes a message on...
@result: adds a react on....
"""
async def command(client, message, other_args):
  search = message.content[7:]
  modifiedSearchString = ''
  lmgtfyPrefix = 'https://lmgtfy.com/?q='
  for c in search:
    if c == ' ':
      modifiedSearchString += '+'
    else:
      modifiedSearchString += c
  try:
    shortener = Shortener('Tinyurl')
    await client.send_message(message.channel if message.channel.name else message.author, '<%s>' % shortener.short(lmgtfyPrefix + modifiedSearchString))
  except:
    await client.send_message(message.author, 'Something went wrong shortening the URL. Here is the raw link: ' + lmgtfyPrefix + modifiedSearchString)
  await client.delete_message(message)



# String that triggers this command
TRIGGER = '!google'

def is_triggered(message_content):
  # determine if this command will be triggered