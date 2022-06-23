import os
import subprocess
import time
import csv
import discord
import multiprocessing
from zipfile import ZipFile
from management import ReposManager, CmdlineManager, CsvParser


def main():
    parser = CsvParser()
    parser.writeCsv()
    print(f'Script Management System started: <pid: {os.getpid()}>')
    reposManager = ReposManager('Repository')
    cmdlineManager = CmdlineManager(reposManager)
    client = discord.Client()

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author.id == 398855441804820480:
            await cmdlineManager.setCommand(message)

    client.run(open('token.txt', 'r').read())


if __name__ == "__main__":
    main()
