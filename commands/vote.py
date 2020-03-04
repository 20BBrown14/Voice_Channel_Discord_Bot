from pathlib import Path
from collections import OrderedDict
import csv
import os

from client_interactions import send_message, add_reaction, delete_message


"""
Vote command
Handles upvoting and downvoting in the chat

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param vote: String representing the kind of vote
@result: Sends a message if the vote list was requested
@result: Deletes a message only if the vote list was requested
@result: Adds a react if the bot user was upvoted or downvoted
"""
async def command(client, message, vote):
  content = ''
  if(vote != 'display' and vote == 'down'):
    content = message.content[10:]
  elif(vote != 'display' and vote == 'up'):
    content = message.content[8:]
  votesFile = ''
  rows = []
  foundName = False
  displayString = 'Name, Upvotes, Downvotes, Net score\n'
  mentions = message.mentions
  if(len(mentions) == 0 and vote != 'display'):
    return 0
  if not (Path('votes.csv').is_file()):
    votesFile = open('votes.csv', "x")
    votesFile.write("name,upvotes,downvotes,net")
    votesFile.close()
  with open('votes.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
      if(vote == 'display'):
        foundName = True
        newStringLine = row['name']+': '+row['upvotes'] + ", " + row['downvotes'] + ", " + row['net']
        displayString = displayString + newStringLine + "\n"
      if(is_user_mentioned(row['name'], mentions)):
        foundName = True
        if(vote == 'down' and row['name'] != message.author.mention):
          row['downvotes'] = str(int(row['downvotes']) - 1)
          row['net'] = str(int(row['net']) - 1)
        elif(vote == 'up' and row['name'] != message.author.mention):
          row['upvotes'] = str(int(row['upvotes']) + 1)
          row['net'] = str(int(row['net']) + 1)
        else:
          await send_message(client, message, "Stop trying to " + vote + "vote yourself you goddamn hooligan!", True)
          print("Someone tried to upvote themselves")
      rows.append(row)
    if not foundName:
      if(vote == 'down' and content != message.author.mention):
        newRow = OrderedDict([('name', content), ('upvotes', '0'), ('downvotes', '-1'), ('net', '-1')])
      elif(vote == 'up' and content != message.author.mention):
        newRow = OrderedDict([('name', content), ('upvotes', '1'), ('downvotes', '0'), ('net', '1')])
      rows.append(newRow)
  with open('votes.csv', mode='w') as csv_file:
    fieldnames=['name','upvotes','downvotes','net']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for row in rows:
      writer.writerow(row)
  if(message.content == '!upvote <@!335445369930514433>'):
    thankList = ["🇹", "🇭", "🇦", "🇳", "🇰"]
    youList = ["🇾", "🇴", "🇺"]
    for emoji in thankList:
      await add_reaction(client, message, emoji)
    await add_reaction(client, message, "⬛")
    for emoji in youList:
      await add_reaction(client, message, emoji)
  elif(message.content == '!downvote <@!335445369930514433>'):
    thankList = ["🇸", "🇨", "🇷", "🇪", "🇼"]
    youList = ["🇾", "🇴", "🇺"]
    for emoji in thankList:
      await add_reaction(client, message, emoji)
    await add_reaction(client, message,  "⬛")
    for emoji in youList:
      await add_reaction(client, message, emoji)
  #await client.send_message(message.channel, displayString)
  if(vote == 'display'):
    await send_message(client, message, displayString)
    await delete_message(client, message)

def is_user_mentioned(id, mentions):
  for member in mentions:
    if member.id in id:
      return True
  return False

# String that triggers this command
UPVOTE_TRIGGER = '!upvote'
DOWNVOTE_TRIGGER = '!downvote'
VOTES_TRIGGER = '!votes'

def is_triggered(message_content):
  return message_content.lower().startswith(UPVOTE_TRIGGER) or message_content.lower().startswith(DOWNVOTE_TRIGGER) or message_content.lower().startswith(VOTES_TRIGGER)

def is_upvote(message_content):
  return message_content.lower().startswith(UPVOTE_TRIGGER)

def is_downvote(message_content):
  return message_content.lower().startswith(DOWNVOTE_TRIGGER)


def is_display(message_content):
  return message_content.lower().startswith(VOTES_TRIGGER)
