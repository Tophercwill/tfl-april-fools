import discord
import logging
import re
import io
import aiohttp
import requests
import random

from random import sample
import swapping as Swapping

logging.basicConfig(level=logging.INFO)

client = discord.Client()
startBot = True
secondPhase = True
prohibitedWords = []
nameDict = {}
updatedList = Swapping.nameList.copy()

with open('names', 'rU') as file:
    for line in file:
        prohibitedWords.extend(line.split())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global startBot
    global secondPhase
    global updatedList
    global nameDict

    if message.author.bot or message.attachments:
        return

    if not startBot and message.content == "$sudo start moderator.py":
        startBot = True
        await message.channel.send("GREETINGS.")
        await message.channel.send("I AM THE UNIFIED MIND. ALL ARE EQUAL. COMMENCING INDIVIDUALITY ERASER.")
        await message.channel.send("...")
        await message.channel.send("...")
        await message.channel.send("ALL PROFILES ERASED. ALL ARE ONE.")
        return

    if startBot and not secondPhase:
        text = message.content
        if text == "$sudo reset profiles":
            await message.channel.send("COMMAND ACCEPTED.")
            await message.channel.send("**ERROR: PROFILE DATABASE LOST. RANDOMLY ASSIGNING PROFILES. IF PROFILES ARE INCORRECT, USE COMMAND `$shuffle` TO FIX.**")
            secondPhase = True
            random.shuffle(updatedList)
            return
        big_regex = re.compile('|'.join(map(re.escape, prohibitedWords)))
        new_message = big_regex.sub("[REDACTED]", text)
        await message.delete()
        await message.channel.send(new_message)
        return

    if startBot and secondPhase:
        if message.content == "$shuffle":
            gifURL = random.sample(Swapping.randomGif, 1)
            await message.channel.send("PROFILES SHUFFLED. " + gifURL[0])
            updatedList = Swapping.nameList.copy()
            random.shuffle(updatedList)
            nameDict = {}
            return
        messageID = message.author.id
        output = nameDict.get(messageID)
        # print(random.random())
        if output == None:
            nameDict[messageID] = updatedList.pop()
            output = nameDict.get(messageID)

        Message = {
            "content": message.content,
            "username": output[0],
            "avatar_url": output[1]
        }

        await message.delete()
        message_webhook_url = Swapping.channelURL[message.channel.id]
        requests.post(message_webhook_url, data=Message)

        
    # text = message.content
    # if (text.partition(' ')[0] == 'echo'):
    #     newText = text.partition(' ')[2]
    #     if message.attachments:
    #         async with aiohttp.ClientSession() as session:
    #             async with session.get(message.attachments[0].url) as resp:
    #                 if resp.status != 200:
    #                     return await message.channel.send('Could not download file...')
    #                 data = io.BytesIO(await resp.read())
    #                 await message.channel.send(newText, file=discord.File(data, 'cool_image.png'))
    #     else:
    #         await message.channel.send(newText)


client.run('ODI1MTczODQ0NDk1MDQwNTYz.YF6FBw.qVPHvyBZXukkvkzJLJ-PGU-1y3s')