"""
Assistant - a simple discord assistant
Copyright (C) 2017 Jewel Mahanta <jewelmahanta@gmail.com>

This file is part of Assistant.

Assistant is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Assistant is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Assistant.  If not, see <http://www.gnu.org/licenses/>.
"""

from assistant import command
import subprocess
import shlex


class UtilityCommands:
    def __init__(self, assistant):
        self.assistant = assistant
        self.state = 0

        # Register the event listeners.
        # self.assistant.event_listener(event="on_message")(self.handle_message)

    @command(description="A sample command to demonstrate stateful behaviour.")
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

    # async def handle_message(self, message):
    #     print(message.content)


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
