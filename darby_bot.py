import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as {}".format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        print("Message from {}. Says: {}".format(message.author, message.content))