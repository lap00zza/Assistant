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

from assistant import Assistant
import os

my_assistant = Assistant()


@my_assistant.command("ping", description="A simple ping command!")
async def _ping(message):
    await my_assistant.send_message(message.channel, "pong")


@my_assistant.event_listener()
async def on_ready():
    print("Login Details\nUsername: {}\nUser ID: {}\n---".format(my_assistant.user.name, my_assistant.user.id))
    commands = "Loaded commands\n"
    for c in my_assistant.commands_list:
        commands += "name: {} | description: {}\n".format(c, my_assistant.commands_list[c].description)
    print(commands)

my_assistant.load_modules("modules.default")
my_assistant.run(os.environ.get("DISCORD_TOKEN"), bot=False)
