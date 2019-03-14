"""
Help function command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: sends a message with help information always
@result: deletes the triggering message always
"""
async def command(client, message):
  channel = message.channel if message.channel.name else message.author
  help_message = """Here are list of available commands:
  < !help >: *Displays a list of available commands*
  < !status >: *Replys indicating I am online*
  < !voice [channel_id] >: *Joins voice channel with specified Id (Special permissions required)*
  < !ping >: *Responds with your ping*
  < !stopvoice >: *Disconnects the bot from the current voice channel (Special permissions required)*
  < !clean [amount] >: *Removes all messages from the channel this command was invoked in that were sent by me or that were commands for the me*
  < !pizza >: *Just do it*
  < !downvote @user >: Downvotes a user and keeps track
  < !upvote @user >: Upvotes a user and keeps track
  < !votes >: Displays all votes
  < !lunchtime >: If it's 11:30AM it's lunch time!
  < /[emote] >: Invoking a slash command will make me search for a relevant gif and then post it
  My main purpose on this server is to announce when users leave or join the voice channel I am in.
  I am a little open source whore. See my birthday suit here: <https://github.com/20BBrown14/Voice_Channel_Discord_Bot>
  Vixxle is the creator of me, contact him if you have any questions.
  Last updated 03/13/2019"""
  await client.send_message(channel, help_message)
  await client.delete_message(message)

# String that triggers the help command
TRIGGER = '!help'