

class CmdlineManager:
    class Command:
        def __init__(self, msg):
            self.content = msg.content.split(' ')

    def __init__(self, reposManager):
        self.reposManager = reposManager
        self.command = None
        self.message = None

    async def setCommand(self, message):
        self.command = self.Command(message)
        self.message = message
        await self._provideCommand()

    async def _provideCommand(self):
        if self.command.content[0] == '$update':
            if self.command.content[1] == 'repository_list':
                self.reposManager.updateRepos()
                await self.message.channel.send('All repos are updated.')

            if self.command.content[1] == 'repository_code':
                elapsedTime = self.reposManager.copyRepos()
                await self.message.channel.send(f'Original code of repos are copied. ({elapsedTime}s)')

        if self.command.content[0] == '$stop':
            if self.command.content[1] == 'all_repository':
                self.reposManager.stopRepos()
                await self.message.channel.send('All repos are stopped.')
