import discord
import requests
import json
import random
from replit import db
import random
import asyncio

client = discord.Client()
greet = ("Hello", "Hi", "Hey", "hello", "hi", "hey")
sad_words = ('lonely','heartbroken','gloomy','disappointed','hopeless'
             ,'grieved','unhappy','lost','troubled','resigned','miserable', 'felling low')
starter_encouragement = ['Cheer up!', "Hang in there.",
                         'you are a great person']

if "responding" not in db.keys():
  db["responding"]= True

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")

    json_data = json.loads(response.text)
    x=json_data[0]

    quote = x
    # quote = json_data

    return (quote)

def update_encouragement(encouragement_message):
  if 'encouragements' in db.keys():
    encouragement = db["encouragements"]
    encouragement.append(encouragement_message)
    db["encouragements"]=encouragement
  else:
    db["encouragements"] = encouragement_message 

def delete_encouragement(index):
  encouragements=db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
    print("Hello, Sir I have logged in as {0.user}".format(client))
    # try using client.User



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith(greet):
        await message.channel.send("Hey! I am Ashish's bot he is busy how can I help you")
    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote['q'])
    if ["responding"]:
      options = starter_encouragement

      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ", 1)[1]
      update_encouragement(encouraging_message)
      await message.channel.send("New encouraging message added")
      

    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split(".del", 1)[1])
        delete_encouragement(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("$list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("$responding"):
      value = msg.split("responding ",1)[1]

      if value.lower == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")

      else:
        db["responding"] = True
        await message.channel.send("Responding is on.")
@client.event
async def on_member_join(member):
    print(f'{member} has join the server')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long it was {answer}.')

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send(f'Oops. It is actually {answer}.')

client = MyClient()
client.run('OTQ0NDY0NDMwNzY5NTM3MDI0.YhB_Cw.tfltkl2Eecu5stAvC0i6Yxp-B64')


