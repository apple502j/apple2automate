﻿import re
import logging
import random
import json
from urllib.parse import quote
import asyncio as a
import discord as d
from discord.ext.commands import Bot
from discord.ext.commands import command
from discord.ext.commands import bot_has_permissions
from discord.ext import commands as c
from aiohttp import ClientSession
import wordsDict
import requests
import time
import platform
import minesweeper
import secret
import threading
import os

global ALERT_USERS
ALERT_USERS={}
global WARNING_USERS
WARNING_USERS={}
async def bMsg(ctx,user,client):
    logger.info('Block Checker:'+user, extra={'invoker': ctx.message.author.name})
    if secret.isBlocked(user):
        if ctx.author.dm_channel is None:
            await ctx.author.create_dm()
        await ctx.author.dm_channel.send("You have been blocked! Please send apple502j DM if you want to be unblocked.")
        await ctx.message.delete()
        logger.info('Blocked:'+user, extra={'invoker': ctx.message.author.name})
        return True
    else:
        return False

async def alertMsg(ctx,user,reason,client):
    global ALERT_USERS
    logger.info('Alert:'+user+' Reason:'+reason, extra={'invoker': ctx.message.author.name})
    if ctx.author.dm_channel is None:
            await ctx.author.create_dm()
    await ctx.author.dm_channel.send("Alert:"+reason)
    secret.setWarnType(user,"alert")
    if user not in ALERT_USERS.keys():
        ALERT_USERS[user] = 1
    elif ALERT_USERS[user] == 2:
        secret.setWarnType(user,"block")
        ALERT_USERS[user] = 0
    else:
        ALERT_USERS[user] = ALERT_USERS[user] + 1

async def warnMsg(ctx,user,reason,client):
    global WARNING_USERS
    global ALERT_USERS
    if user in ALERT_USERS.keys():
        await alertMsg(ctx,user,reason,client)
    logger.info('Warning:'+user+' Reason:'+reason, extra={'invoker': ctx.message.author.name})
    if ctx.author.dm_channel is None:
            await ctx.author.create_dm()
    await ctx.author.dm_channel.send("Warning:"+reason)
    secret.setWarnType(user,"warning")
    if user not in WARNING_USERS.keys():
        WARNING_USERS[user] = 1
    elif WARNING_USERS[user] == 2:
        await alertMsg(ctx,user,reason,client)
        WARNING_USERS[user] = 0
    else:
        WARNING_USERS[user] = WARNING_USERS[user] + 1
        
logfmt = logging.Formatter(
    fmt='{asctime} {invoker}: {message}',
    datefmt='%Y-%m-%dT%H:%M:%SZ',
    style='{'
)

class CustomHandler(logging.Handler):
    def emit(self, record):
        print(self.format(record))

handler = CustomHandler()
handler.setFormatter(logfmt)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

secret.clearAllWarnings()

client = Bot(description="A testing Discord bot.", command_prefix="$")

@client.command()
async def ban(msg,whotoban):
    if msg.author.name != "apple502j":
        pass
    else:
        secret.setWarnType(whotoban,"block")
    await msg.delete()

@client.command()
async def unban(msg,whotounban):
    if msg.author.name != "apple502j":
        pass
    else:
        secret.setWarnType(whotounban,"block",remove=True)
    await msg.delete()


@client.command()
async def say(ctx):
    """For owner"""
    if ctx.message.author.name != "apple502j":
        return
    await ctx.message.delete()
    await ctx.send(input("What to say >"))

@client.command()
async def clear(ctx):
    """ CLEAR! """
    await ctx.send('_' + ('\n' * 40) + 'Clear!')

@client.command()
async def botinfo(ctx,infonum):
    """ Bot Info """
    try:
        info_txt_f=open(os.getcwd() + "\\info\\" + infonum + ".txt","r")
    except:
        await ctx.send("botinfo -1: I can't find the file!")
        return
    await ctx.send(info_txt_f.read())
    info_txt_f.close()



class Regexes(object):
    """Regex commands - Python flavored."""
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def search(self, ctx, pattern, string, flags=None):
        """Make a Python-flavored regex search! All groups are shown."""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Regexes.search: \"' + '\" \"'.join((pattern, string, flags)) + '\"', extra={'invoker': ctx.message.author.name})
        if flags is not None:
            exp = '(?' + flags.lower().replace('l', 'L') + ')(?:' + pattern + ')'
        else:
            exp = pattern
        try:
            m = re.search(exp, string)
        except Exception:
            m = False
        if m:
            result = '```\nGroups:\n' + m.group(0) + '\n'
            for group in m.groups():
                result += (group or '') + '\n'
            result += '```'
        elif m is False:
            result = '```\nError in flags or expression.\n```'
        else:
            result = '```\nNo match :(\n```'
        await ctx.send(result)

    @command()
    async def findall(self, ctx, pattern, string, flags=None):
        """Use a Python-flavor regex to find all occurences of a pattern!"""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Regexes.findall: \"' + '\" \"'.join((pattern, string, flags)) + '\"', extra={'invoker': ctx.message.author.name})
        if flags is not None:
            exp = '(?' + flags.lower().replace('l', 'L') + ')(?:' + pattern + ')'
        else:
            exp = pattern
        gen = re.finditer(exp, string)
        result = '```\nResults:\n'
        try:
            for m in gen:
                result += m.group(0) + ('\t' if len(m.groups()) > 0 else '') + '\t'.join(m.groups()) + '\n'
        except Exception:
            result += 'Error in flags or expression.\n'
        if result == '```\nResults:\n':
            result += 'No results :(\n'
        if '\t' in result:
            ms = re.finditer('([^\t\n]*\t)+[^\t\n]*\n?', result)
            ms = [len(m.group(0).strip().split('\t')) for m in ms]
            ms = max(ms)
            result = result[:13] \
                 + '\t'.join(['Gp{}'.format(i) for i in range(ms-1)]) \
                 + '\n' + result[13:]
        result += '```'
        await ctx.send(result)

client.add_cog(Regexes(client))

DGHANGMANSHANPES = [
    '```\n_\n\n\n\n_```',
    '```\n_\n\n\n\u2500\u2500\u2500\u2500\u2500\n```',
    '```\n\u250c\u2500\u2500\u2500\u2510\n\u2502\n\u2502\n\u2502\n\u2514\u2500\u2500\u2500\u2500\n```',
    '```\n\u250c\u2500\u2500\u2500\u2510\n\u2502   O\n\u2502\n\u2502\n\u2514\u2500\u2500\u2500\u2500\n```',
    '```\n\u250c\u2500\u2500\u2500\u2510\n\u2502   O\n\u2502  /\n\u2502\n\u2514\u2500\u2500\u2500\u2500\n```',
    '```\n\u250c\u2500\u2500\u2500\u2510\n\u2502   O\n\u2502  / \\\n\u2502\n\u2514\u2500\u2500\u2500\u2500\n```',
    '```\n\u250c\u2500\u2500\u2500\u2510\n\u2502   O\n\u2502  /|\\\n\u2502\n\u2514\u2500\u2500\u2500\u2500\n```',
    '```\n\u250c\u2500\u2500\u2500\u2510\n\u2502   O\n\u2502  /|\\\n\u2502  /\n\u2514\u2500\u2500\u2500\u2500\n```',
    '```\n\u250c\u2500\u2500\u2500\u2510\n\u2502   O\n\u2502  /|\\\n\u2502  / \\\n\u2514\u2500\u2500\u2500\u2500\n```'
]

class Games(object):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def numguess(self, ctx):
        """Play a fun number-guessing game!"""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Games.numguess', extra={'invoker': ctx.message.author.name})
        guess = None
        limDn = 0
        limUp = 100
        tries = 7
        secret = random.randint(1, 100)
        await ctx.send("""Arr! I'm the Dread Pirate Roberts, and I have a secret!
It's a number from {} to {}. I'll give you {} tries.
Send a number to guess it.""".format(limDn, limUp, tries))
        while guess != secret and tries > 0:
            await ctx.send("What's yer guess, matey?")
            result = ''
            guess = await ctx.bot.wait_for('message',
                check=lambda m: m.channel == ctx.channel and re.match('[0-9]+', m.content))
            guess = int(guess.content)
            if guess == secret:
                break
            elif guess < limDn or guess > limUp:
                result += "Out of range, ye swab!\n"
            elif guess < secret:
                result += "Too low, ye scurvy dog!\n"
                limDn = guess
            elif guess > secret:
                result += "Too high, landlubber!\n"
                limUp = guess
            tries -= 1
            result += "Yer range is {} to {}; ye have {} tries left.".format(limDn, limUp, tries)
            await ctx.send(result)
        if guess == secret:
            await ctx.send("Avast! Ye got it! Found my secret, ye did! With {} tries left!".format(tries))
        else:
            await ctx.send("No more tries, matey! Better luck next time! The secret number was {}.".format(secret))

    @staticmethod
    def substrs(sub, string):
        last_found = -1
        while 1:
            last_found = string.find(sub, last_found + 1)
            if last_found == -1:
                break
            yield last_found

    channels_occupied_hangman = set()
    channels_occupied_mine = set()
    
    @command()
    async def minesweeper(self,ctx):
        """ Minesweeper Beta
        Answer is (column)(space)(row) like 5 2.
        ? is unknown, _ is nothing, and X is mine.
        """
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Games.minesweeper', extra={'invoker': ctx.message.author.name})
        if ctx.channel in self.channels_occupied_mine:
            return await ctx.send("There is already a game going on in this channel!")
        self.channels_occupied_mine.add(ctx.channel)
        await minesweeper.play(ctx)
        self.channels_occupied_mine.remove(ctx.channel)
    @command()
    async def hangman(self, ctx, defaultWord = ""):
        """Yes, it's hangman!

        Use this first in the server, to start the game in that channel;
        Next, send the word in a DM with the bot, to set it.
        Once that's been done, guess a letter by sending it.
        """
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Games.hangman', extra={'invoker': ctx.message.author.name})
        if ctx.channel in self.channels_occupied_hangman:
            return await ctx.send("There is already a game going on in this channel!")
        self.channels_occupied_hangman.add(ctx.channel)
        if defaultWord == "":
            await ctx.send("Awaiting DM with word...")
            WORD = await ctx.bot.wait_for('message',
                check=lambda m: isinstance(m.channel, d.DMChannel) and m.author == ctx.message.author)
        else:
            WORD = defaultWord
        WORD = WORD.content.lower()
        letters = ['_'] * len(WORD)
        lowers = (
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z'
        )
        for i in range(len(WORD)):
            if WORD[i] not in lowers:
                letters[i] = WORD[i]
        missed = []
        shanpe = 0
        await ctx.send(DGHANGMANSHANPES[shanpe] + '\n' + 'Missed:\nGotten: `' + "".join(letters) + '`')
        while "".join(letters) != WORD and shanpe < len(DGHANGMANSHANPES) - 1:
            letter = (await ctx.bot.wait_for('message',
                check=lambda m: m.channel == ctx.channel and m.content in lowers)).content
            if WORD.find(letter) != -1:
                for i in self.substrs(letter, WORD):
                    letters[i] = letter
            else:
                if letter not in missed:
                    missed.append(letter)
                    shanpe += 1
            await ctx.send(DGHANGMANSHANPES[shanpe] + '\nMissed: ' + ','.join(missed) + '\nGotten: `' + "".join(letters) + '`')
        if "".join(letters) == WORD:
            await ctx.send('Congratulations! You have guessed the complete word!')
        else:
            await ctx.send('You lost! The word was \"{}\".'.format(WORD))
        self.channels_occupied.remove(ctx.channel)
    
#    @command()
#    async def fungman(self,ctx):
#        """
#        This is hangman. The text is generated automatically, and usually it's funny.
#        """
#        client.invoke(ctx,self.hangman(self,ctx,defaultWord=wordsDict.generate()))

    @command()
    async def saytext(self,ctx):
        """
        Say automatically-generated text, and it's usually funny. 
        """
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Games.saytext', extra={'invoker': ctx.message.author.name})
        await ctx.send(wordsDict.generate())
    
    @command()
    @bot_has_permissions(manage_messages=True)
    async def localhangman(self, ctx):
        """Hangman completely within one channel!

        Use this in the channel to start the game there,
        send the word to set it,
        then send letters to guess them.
        """
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Games.localhangman', extra={'invoker': ctx.message.author.name})
        if ctx.channel in self.channels_occupied:
            await ctx.send('There is already a game going on in this channel!')
        self.channels_occupied.add(ctx.channel)
        await ctx.send('Awaiting DM with word...')
        msg = await ctx.bot.wait_for('message',
            check=lambda m: isinstance(m.channel, d.DMChannel) and m.author == ctx.author)
        WORD = msg.content.lower()
        letters = ['_'] * len(WORD)
        lowers = (
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
            'w', 'x', 'y', 'z'
        )
        for i in range(len(WORD)):
            if WORD[i] not in lowers:
                letters[i] = WORD[i]
        missed = []
        shanpe = 0
        status = await ctx.send(DGHANGMANSHANPES[shanpe] + '\nMissed: ' + ', '.join(missed) + '\nGotten: `' + "".join(letters) + '`')
        while "".join(letters) != WORD and shanpe < len(DGHANGMANSHANPES) - 1:
            guess = await ctx.bot.wait_for('message',
                check=lambda m: m.channel == ctx.channel and m.content in lowers)
            letter = guess.content
            await guess.delete()
            if WORD.find(letter) != -1:
                for i in self.substrs(letter, WORD):
                    letters[i] = letter
            else:
                if letter not in missed:
                    missed.append(letter)
                    shanpe += 1
            await status.edit(content=(DGHANGMANSHANPES[shanpe] + '\nMissed: ' + ', '.join(missed) + '\nGotten: `' + "".join(letters) + '`'))
        if "".join(letters) == WORD:
            await ctx.send('Congratulations! You have guessed the complete word!')
        else:
            await ctx.send('You lost! The word was \"{}\".'.format(WORD))
        self.channels_occupied.remove(ctx.channel)

    @localhangman.error
    async def on_localhangman_err(self, ctx, error):
        logger.error('Games.localhangman failed: ' + str(error), extra={'invoker': ctx.message.author.name})
        if isinstance(error, c.BotMissingPermissions):
            await ctx.send(str(error))

client.add_cog(Games(client))

SESH = None

class Wiki(object):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def req(params):
        params['format'] = 'json'
        async with SESH.get('https://en.scratch-wiki.info/w/api.php', params=params) as resp:
            return await resp.json()

    @command()
    async def page(self, ctx, *, title):
        """Get the contents of a page."""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Wiki.page: ' + title, extra={'invoker': ctx.message.author.name})
        async with ctx.channel.typing():
            try:
                content = await self.req({
                    'action': 'query',
                    'prop': 'revisions',
                    'titles': title,
                    'rvlimit': '1',
                    'rvprop': 'content',
                })
            except Exception:
                await ctx.send('Fetching content failed. The page is likely too large. Sorry!')
                return
            content = list(content['query']['pages'].values())[0]['revisions'][0]['*']
            content = content.splitlines()
            contents = ['```\n']
            i = 0
            for line in content:
                contents[i] += line + '\n'
                if len(contents[i]) + 3 > 2000:
                    contents.append('```')
                    contents[i], contents[i+1] = contents[i].rsplit('\n', 1)
                    contents[i] += '```'
                    i += 1
                    contents[i] = '```\n' + contents[i]
            contents[-1] += '```'
            for msg in contents:
                await ctx.send(msg)

    @command()
    async def recentchanges(self, ctx, limit=50):
        """Get recent changes on the Wiki."""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Wiki.recentchanges: ' + str(limit), extra={'invoker': ctx.message.author.name})
        twenties, limit = divmod(limit, 20)
        async with ctx.channel.typing():
            result = ['']
            changes = []
            start = 'now'
            for i in [20 for j in range(twenties)] + [limit]:
                resp = await self.req({
                    'action': 'query',
                    'list': 'recentchanges',
                    'rcprop': 'user|timestamp|comment|title|sizes|flags',
                        'rctype': 'edit|new',
                    'rclimit': i,
                    'rcstart': start
                })
                changes.extend(resp['query']['recentchanges'])
                start = resp['query']['recentchanges'][-1]['timestamp']
            i = 0
            for ch in changes:
                change = '\n'
                change += ch['timestamp']
                change += ': '
                change += ch['title']
                change += '; '
                sizechange = ch['newlen'] - ch['oldlen']
                if sizechange <= -500 or sizechange >= 500:
                    change += '**'
                change += '('
                if sizechange <= 0:
                    change += str(sizechange)
                if sizechange > 0:
                    change += '+' + str(sizechange)
                change += ')'
                if sizechange <= -500 or sizechange >= 500:
                    change += '**'
                change += ' . . '
                change += ch['user']
                change += ' _('
                change += ch['comment'].replace('*', '\\*').replace('_', '\\_').replace('`', '\\`')
                change += ')_'
                result[i] += change
                if len(result[i]) > 2000:
                    result.append('')
                    result[i], result[i+1] = result[i].rsplit('\n', 1)
                    i += 1
            for r in result:
                await ctx.send(r)

    @command()
    async def randompage(self, ctx):
        """Get a link to a random Wiki page!"""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Wiki.randompage', extra={'invoker': ctx.message.author.name})
        rn = await self.req({
            'action': 'query',
            'list': 'random',
            'rnlimit': '1',
            'rnnamespace': '0'
        })
        title = rn['query']['random'][0]['title']
        title = title.replace(' ', '_').capitalize()
        title = quote(title, safe='/:')
        await ctx.send('https://en.scratch-wiki.info/wiki/' + title)

client.add_cog(Wiki(client))

global TRANSLATELIMIT
TRANSLATELIMIT=time.time() - 20

class Scratch(object):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def req(url):
        async with SESH.get(url) as resp:
            if resp.status >= 400:
                return None
            else:
                return await resp.text()
    @staticmethod
    def req2(url):
        resp=requests.get(url)
        if resp.status_code >= 400:
            return None
        else:
            return resp.text

    async def translater(self,ctx,lang="ja",txt=None):
        global TRANSLATELIMIT
        if time.time() < TRANSLATELIMIT + 20:
            await ctx.send("You need to wait 20 seconds between translating commands!")
            await warnMsg(ctx,ctx.message.author.name,"Please don't use translate commands so quickly.",client)
            return
        if txt == None:
            return
        resp=self.req2("https://translate-service.scratch.mit.edu/supported")
        if resp == None:
            return
        respjson=json.loads(resp)
        supported=map(lambda x:x["code"],respjson["result"])
        if lang not in supported:
            lang="ja"
        addr="https://translate-service.scratch.mit.edu/translate?language={0}&text={1}".format(lang,txt)
        resp=self.req2(addr)
        if resp == None:
            return
        logger.info('Scratch.translater {0} {1} {2}'.format(lang,txt,addr), extra={'invoker': ctx.message.author.name})
        await ctx.send(json.loads(resp)["result"])
        TRANSLATELIMIT = time.time()
        return

    @command()
    async def randomproject(self, ctx):
        """Get a random project link!"""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Scratch.randomproject', extra={'invoker': ctx.message.author.name})
        async with ctx.channel.typing():
            count = json.loads(await self.req('https://api.scratch.mit.edu/projects/count/all'))['count']
            comments = None
            while comments is None:
                pid = random.randint(1, count)
                comments = await self.req('https://scratch.mit.edu/site-api/comments/project/' + str(pid))
            await ctx.send('https://scratch.mit.edu/projects/' + str(pid))

    @command()
    async def messagecount(self, ctx, name=None):
        """How many messages do you have on Scratch?"""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        async with ctx.channel.typing():
            username = name
            if username is None:
                username = ctx.message.author.name
            resp = await self.req('https://api.scratch.mit.edu/users/' + username + '/messages/count')
            if resp is None and name is None:
                username = getattr(ctx.message.author, 'nick', '_')
                resp = await self.req('https://api.scratch.mit.edu/users/' + username + '/messages/count')
            logger.info('Scratch.messagecount: ' + username, extra={'invoker': ctx.message.author.name})
            if resp is None:
                await ctx.send("Couldn't get message count for " + username)
            else:
                await ctx.send('{} has {} messages'.format(
                    username,
                    json.loads(resp)['count']
                ))

    @command()
    async def news(self, ctx):
        """Get Scratch news."""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        logger.info('Scratch.news', extra={'invoker': ctx.message.author.name})
        content = await self.req('https://api.scratch.mit.edu/news')
        content = json.loads(content)
        for new in content[0:5]:
            await ctx.send(
                '**' + new['headline'] + '**'
                + '\n' + new['copy'] + '\n' + new['url']
            )



    @command()
    async def translate(self,ctx,lang="ja",txt=None):
        """ Apple can speak many languages!
translate <lang=ja> <text=None>
Never forget to write \" before and after the text you translate! """
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        await self.translater(ctx,lang,txt)

    @command()
    async def funslate(self,ctx,lang="ja"):
        """ Translate funny text.
funslate <lang=ja>"""
        if await bMsg(ctx,ctx.message.author.name,client):
            return
        await self.translater(ctx,lang,wordsDict.generate())


client.add_cog(Scratch(client))

@client.event
async def on_ready(*_, **__):
    global SESH
    logger.info('Ready!', extra={'invoker': '(core)'})
    SESH = ClientSession()
    await client.change_presence(activity=d.Game(name="Help is:$help"))

@client.command()
async def repeat(ctx, *, arg):
    """Repeat what you say, right back at ya."""
    if await bMsg(ctx,ctx.message.author.name,client):
            return
    logger.info('repeat: ' + arg, extra={'invoker': ctx.message.author.name})
    await ctx.send(arg)

@client.command()
async def hello(ctx):
    """Test whether the bot is running! Simply says "Hello World!"."""
    if await bMsg(ctx,ctx.message.author.name,client):
            return
    logger.info('Hello World!', extra={'invoker': ctx.message.author.name})
    await ctx.send('Hello World!')

@client.command()
async def hmmst(ctx):
    """hmmst"""
    if await bMsg(ctx,ctx.message.author.name,client):
            return
    logger.info('hmmst', extra={'invoker': ctx.message.author.name})
    await ctx.send('hmmst')


@client.command()
async def whichpc(ctx):
    """ Check which PC is running the bot."""
    if await bMsg(ctx,ctx.message.author.name,client):
            return
    if platform.win32_ver()[0] == '7':
        await ctx.send("My main PC (Windows 7)")
    else:
        await ctx.send("My mobile PC (Windows 10)")

@client.command()
async def mine(ctx):
    """Shortcut of minesweeper."""
    if await bMsg(ctx,ctx.message.author.name,client):
            return
    await ctx.send('Hey, this command is **mine**!')

@client.command()
async def whoami(ctx):
    await ctx.send(ctx.message.author.name)

DGBANSERVERID = 328938947717890058
#DGBANSERVERID = 337100820371996675

@client.command()
@bot_has_permissions(ban_members=True, add_reactions=True, read_message_history=True)
async def votetoban(ctx, *, user: d.Member):
    """Start a vote to ban someone from the server. Abuse results in a ban."""
    if await bMsg(ctx,ctx.message.author.name,client):
            return
    logger.info('votetoban: ' + user.mention, extra={'invoker': ctx.message.author.name})
    if ctx.guild.id != DGBANSERVERID:
        return
    for member in ctx.guild.members:
        if (not str(member.status) == 'offline') \
                and ctx.channel.permissions_for(member).administrator:
            await ctx.send(member.mention + ', someone requests for ' + user.mention + ' to be banned!')
            return
    DOBAN = '陜}ｩ'
    NOBAN = '陜qd'
    msg = await ctx.send('**Vote to ban ' + user.mention + '**\nReact ' + DOBAN + ' to vote to ban; react ' + NOBAN + ' to vote to keep.')
    await msg.add_reaction(DOBAN)
    await msg.add_reaction(NOBAN)
    try:
        await ctx.bot.wait_for('member_update',
            check=lambda o, m: \
                ctx.channel.permissions_for(m).administrator \
                and not str(m.status) == 'offline',
            timeout=180.0
        )
        await msg.delete()
        await ctx.send('An admin has come online! The vote has been cancelled. Please ask them instead.')
    except a.TimeoutError:
        msg = await ctx.get_message(msg.id)
        dos = 0
        nos = 0
        for r in msg.reactions:
            if r.emoji == DOBAN:
                dos = r.count - 1
            elif r.emoji == NOBAN:
                nos = r.count - 1
        await msg.delete()
        if dos + nos < 3:
            await ctx.send('Not enough people voted! ({} total, minimum is 3.) The user stays.'.format(dos + nos))
        elif dos > nos:
            await ctx.send('{} votes for and {} votes against. The user has been banned.'.format(dos, nos))
            await user.ban(reason='Banned after vote'
                    + ' {} against {}'.format(dos, nos)
                    + ' when admins were gone.')
        else:
            await ctx.send('{} votes for and {} votes against. The user stays.'.format(dos, nos))

@votetoban.error
async def on_votetoban_err(ctx, error):
    logger.error('votetoban failed: ' + str(error), extra={'invoker': ctx.message.author.name})
    if isinstance(error, c.BotMissingPermissions):
        await ctx.send(str(error))
    else:
        raise error


if True:
    print('Defined stuff')

    with open('login.txt') as f:
        token = f.read().strip()

    client.run(token)

