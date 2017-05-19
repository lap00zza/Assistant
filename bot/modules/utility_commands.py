from assistant import command
import subprocess
import shlex


class UtilityCommands:
    def __init__(self, assistant):
        self.assistant = assistant
        self.state = 0

    @command()
    async def test_state(self, message):
        self.state += 1
        await self.assistant.send_message(message.channel, self.state)

    @command("evaljs", description="Evaluate JS code.")
    async def _eval_js(self, message):
        body = message.content[7:]
        result = subprocess.run(["node", "-p", body], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        await self.assistant.send_message(message.channel, "```js\n{}```".format(result.stdout.decode()))

    @command("evalpy", description="Evaluate Python3 code.")
    async def _eval_py(self, message):
        body = message.content[7:]
        result = subprocess.run(["python", "-c", body], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        await self.assistant.send_message(message.channel, "```py\n{}```".format(result.stdout.decode()))

    @command("sh", description="Run shell commands.")
    async def _sh(self, message):
        body = message.content[3:]
        args = shlex.split(body)

        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        decoded_res = result.stdout.decode()
        if len(decoded_res) > 1900:
            decoded_res = decoded_res[:1900] + "\n[...]"

        await self.assistant.send_message(message.channel, "```\n{}```".format(decoded_res))


def load(assistant):
    """
    Every module needs a load function. This is responsible for initializing
    and doing the initial setup.

    Parameters
    ----------
    assistant: Assistant
        The reference to the assistant instance.
    """
    assistant.add_module(UtilityCommands(assistant))
