import globals_file
from client_interactions import add_reaction
from wakeonlan import send_magic_packet

"""
Turn on PC
Attempts to send the magic packet to the MAC address specified in the config

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Sends magic packet to the mac address in the config
"""

async def apply(client, message):
  send_magic_packet(globals_file.turn_on_pc_config['mac_to_wake'])
  await add_reaction(client, message, '👍')
  await add_reaction(client, message, '🖥️')

def is_triggered(message):
  if(not message.guild.id in globals_file.turn_on_pc_config['allowed_servers']):
    return False
  if(not message.channel.id in globals_file.turn_on_pc_config['allowed_channels']):
    return False
  if(not message.author.id in globals_file.turn_on_pc_config['allowed_users']):
    return False
  if(not globals_file.turn_on_pc_config['mac_to_wake']):
    return False
  # determine if this rule will be triggered
  return message.content == 'turn on pc'
