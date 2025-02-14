import os
import discord
from management.reposMgmt import ReposMgmt
from management import CmdlineManager


def main():
    initialize()
    reposMgmt = ReposMgmt()
    reposMgmt.startRepos()
    # reposManager = ReposManager()
    cmdlineManager = CmdlineManager(reposMgmt)
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
    print(f'Script Management System started: (pid: {os.getpid()})')


if __name__ == "__main__":
    main()
