from client_interactions import delete_message, send_message

"""
Help function command
ex: !help

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: sends a message with help information always
@result: deletes the triggering message always
"""
async def command(client, message):
  channel = message.channel if message.channel.name else message.author
  help_message = """**Here are list of available commands:**
  < !help >: *Displays a list of available commands*
  < !clean [amount] >: *Removes all messages from the channel this command was invoked in that were sent by me or that were commands for the me*
  < !define [word] >: *Looks up the definition of the word provided*
  < !downvote @user >: *Downvotes a user and keeps track*
  < !emojify [text] >: *Emojifies the provided text*
  < !friday >: *Is it Friday?
  < !harrypotter [begin, stop, resume, pause] [HP#-Chapter##-Part##] [VoiceChannelId] >: *Reads you Harry Potter books*
  < !lunchtime > or < !lunch >: *Tells you if it's lunch time based on the !setlunch command*
  < !Mark >: *Let's you know how long it has been since Mark first got rekt at foosball*
  < !ping >: *Responds with your ping*
  < !pizza >: *Just do it*
  < !setlunch >: *Sets the lunch time for the !lunch command*
  < !singleresults ['count']>: *Lists the single result searches from slash command*
  < !status >: *Replys indicating I am online*
  < !upvote @user >: *Upvotes a user and keeps track*
  < !votes >: *Displays all votes from upvote and downvote commands.*
  < !weather [forecast] [zip=#####] >: *Looks up and displays weather for the given zipcode*
  < /[emote] >: *Invoking a slash command will make me search for a relevant gif and then post it*
  I am a little open source whore. See my birthday suit here: <https://github.com/20BBrown14/Voice_Channel_Discord_Bot>
  Nibikk#8335 is the creator of me, contact him if you have any questions.
  Last updated 03/06/2020"""
  await send_message(message, help_message)
  await delete_message(message)

# String that triggers the help command
TRIGGER = '!help'