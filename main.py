import os
import discord
from management import ReposManager, CmdlineManager, CsvParser


def main():
    initialize()
    reposManager = ReposManager()
    cmdlineManager = CmdlineManager(reposManager)
    discordClient(cmdlineManager)


def discordClient(cmdlineManager):
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author.id == 398855441804820480:
            await cmdlineManager.setCommand(message)

    client.run(open('token.txt', 'r').read())


def initialize():
    parser = CsvParser()
    parser.writeCsv()
    print(f'Script Management System started: (pid: {os.getpid()})')


if __name__ == "__main__":
    main()
