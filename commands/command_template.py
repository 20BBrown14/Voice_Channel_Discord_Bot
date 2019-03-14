"""
Command function template

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param other_args: Whatever other args that are passed into this template
@result: sends a message on...
@result: deletes a message on...
@result: adds a react on....
"""
async def command(client, message, other_args):
  # Do some stuff


# String that triggers this command
TRIGGER = '!some_trigger_mesasge'