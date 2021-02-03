import finnhub
from client_interactions import delete_message, send_message
import discord
import random

import globals_file

def creat_embeded(title, quote_data):
  open_price = quote_data['o']
  current_price = quote_data['c']
  previous_close = quote_data['pc']
  high_price = quote_data['h']
  low_price = quote_data['l']

  potential_logos = [
    "https://www.designfreelogoonline.com/wp-content/uploads/2017/09/000878-diamond-logo-design-logo-Free-Logo-creator-02.png",
    "https://styles.redditmedia.com/t5_2th52/styles/communityIcon_b37n2zfs8k861.png?width=256&s=a9cb63319055ded916e5b12ff03f1e8c63ae6911",
    "https://wprock.fr/wp-content/themes/wprock-theme/img/emoji/joypixels/512/1f680.png",
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/emojidex/112/chart-with-upwards-trend_1f4c8.png",
    "https://hongkongseohk.com/wp-content/uploads/2015/10/Money-lost-800x706.png",
    "https://miro.medium.com/max/3200/1*O9LVa-Zec0gGIBdqQtpykA.png",
  ]

  color = 0x00ff00 if current_price > open_price else 0xff0000
  embeded = discord.Embed(title="%s's pricing information" % title, description="Pricing info for %s" % title, color=color)
  
  embeded.set_thumbnail(url=random.choice(potential_logos))
  
  embeded.add_field(name="Open Price", value="$%s" % open_price, inline=True)
  embeded.add_field(name="Current Price", value="$%s" % current_price, inline=True)
  embeded.add_field(name="Previous Close", value="$%s" % previous_close, inline=True)
  embeded.add_field(name="High Price", value="$%s" % high_price, inline=True)
  embeded.add_field(name="Low Price", value="$%s" % low_price, inline=True)

  return embeded

"""
Command function template
Gets a stock price and displays it

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Sends a message always with data or unable to get data
@result: Deletes triggering message always
"""
async def command(client, message):
  message_args = message.content[8:]

  await delete_message(message)
  if (' ' in message_args):
    return

  quote_data = globals_file.finnhub_client.quote(message_args.upper())
  if (quote_data['c'] == 0 and quote_data['h'] == 0 and quote_data['l'] == 0 and quote_data['o'] == 0 and quote_data['pc'] == 0 and quote_data['t'] == 0):
    await send_message(message, 'No data available for %s' % message_args)
    return

  await message.channel.send(embed=creat_embeded(message_args.upper(), quote_data))

# String that triggers this command
TRIGGER = '!stonks'

def is_triggered(message_content):
  return message_content.lower().startswith(TRIGGER)