import discord
from discord.ext import commands
import datetime
import asyncio
import sqlite3


class MyDatabase:
    def __init__(self):
        self.db_connection = sqlite3.connect('sqlite.db')

    def get_messages_list(self):
        messages_list = []
        cursor = self.db_connection.cursor()
        for row in cursor.execute('select * from messages where sent=0'):
            execution_datetime = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            single_message = {'id': row[0], 'time': execution_datetime, 'message': row[2].replace('\\n', '\n'), 'sent': bool(row[3])}
            messages_list.append(single_message)
        return messages_list

    def mark_as_sent(self, row_id):
        cursor = self.db_connection.cursor()
        cursor.execute('update messages set sent = 1 where id = ?', (row_id,))
        self.db_connection.commit()


class DiscordMessageSender(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = None
        self.database = MyDatabase()
        self.prd_channel_id = 732307601202741301
        self.uat_channel_id = 744152884933034017
        self.hfwc_channel_id = 740594408952692898

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.bg_task = self.loop.create_task(self.send_message())

    async def on_message(self, message):
        print(message.created_at, message.author, message.content)

    async def send_message(self):
        await self.wait_until_ready()
        channel = self.get_channel(self.uat_channel_id)
        while True:
            messages_list = self.database.get_messages_list()
            for item in messages_list:
                if number_of_seconds_to_date(item['time']) <= 0 and not item['sent']:
                    self.database.mark_as_sent(item['id'])
                    await channel.send(item['message'], file=discord.File('Have Fun With CodING #2.ipynb'))
            await asyncio.sleep(1)

#
def number_of_seconds_to_date(date):
    now = datetime.datetime.now()
    return (date - now).total_seconds()


bot = DiscordMessageSender(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
f = open("token.txt", "r")
token = f.readline()

bot.run(token)
