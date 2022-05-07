from twitchio.ext import commands
from dotenv import load_dotenv
import os
from tts import play_tts
import yaml
import pprint

# TODO:
# - contadores
# - requests
# - audios
# - resgates
# - subs
# - pomodoro
# - info na tela


printer = pprint.PrettyPrinter(indent=2)
load_dotenv()

TWITCH_ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")
TWITCH_REFRESH_TOKEN = os.getenv("TWITCH_REFRESH_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
PREFIX = "!"
BAGUNCINHA = True
BARULHO = True
TO_LOL_VOLUNTARIO = 10
TO_LOL_MOD = 60

with open("./simple_commands.yaml", "r", encoding="utf-8") as commands_file:
    simple_commands = yaml.load(commands_file, Loader=yaml.FullLoader)

parsed_commands = {}
for item in simple_commands:
    keywords = item["keywords"].split(",")
    for word in keywords:
        word = word.strip()
        parsed_commands[word] = item


class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(
            token=TWITCH_ACCESS_TOKEN, prefix=PREFIX, initial_channels=["jlugao"]
        )

    def is_simple_command(self, text):
        first_letter = text[0]
        if first_letter == PREFIX:
            return text[1:].lower() in parsed_commands
        return False

    async def handle_simple_command(self, message):
        ctx = await self.get_context(message)
        command = parsed_commands[message.content[1:].lower()]
        should_tts = False
        should_text = True

        if "flags" in command:
            if "baguncinha" in command["flags"] and BAGUNCINHA:
                should_tts = True
                should_text = True

            if "barulho" in command["flags"] and BARULHO:
                should_tts = True
                should_text = True
        # handle tts
        if should_tts and "tts" in command:
            for item in command["tts"]:
                play_tts(item)

        # handle text responses
        if should_text and "text" in command:
            for item in command["text"]:
                await ctx.send(item)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        if BARULHO:
            play_tts("Olá o bot iniciou")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        if self.is_simple_command(message.content):
            await self.handle_simple_command(message)
            return
        else:
            await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        play_tts(f"{ctx.author.name} deu um alozinho")
        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command(aliases=["iol", "loi", "ioi", "l0l", "i0l", "i0i", "l0i"])
    async def lol(self, ctx: commands.Context):
        if ctx.author.is_mod:
            lolzero = ctx.message.content.split(" ")[1]
            if lolzero[0] == "@":
                lolzero = lolzero[1:]
            await ctx.send(f"/timeout @{lolzero} {TO_LOL_MOD}")
            await ctx.send(f"{lolzero} tomou TO por ser um Lolzero safado!")
        else:
            await ctx.send(f"/timeout @{ctx.author.name} {TO_LOL_VOLUNTARIO}")
            await ctx.send(f"{ctx.author.name} tomou TO por ser um Lolzero safado!")
        if BARULHO:
            play_tts(f"Eca, lol não")

    @commands.command(aliases=["siga", "so", "s2", "sh"])
    async def indica(self, ctx: commands.Context):
        if ctx.author.is_mod:
            siga = ctx.message.content.split(" ")[1]
            if siga[0] == "@":
                siga = siga[1:]
            channel = await self.fetch_channel(siga)
            game = channel.game_name

            await ctx.send(
                f"Conheça {siga} que estava jogando {game}. Acesse https://twitch.tv/{siga}!"
            )
            if BARULHO:
                play_tts(f"segue essa pessoa linda aí pô")


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
