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

import asyncio
from typing import Dict

__all__ = ["Command", "Common", "command"]


class Command:
    """
    Represents a command.

    Attributes
    ----------
    name: str
        The name of the command.
    callback: coroutine
        The coroutine to invoke when the command is used.
    description: str
        A short description of the command.
    """
    def __init__(self, name, callback, **kwargs):
        self.name = name
        self.callback = callback
        self.description = kwargs.get("description", "")
        self.instance = None

    def set_instance(self, instance):
        self.instance = instance

    async def run_command(self, message):
        if self.instance is None:
            await self.callback(message)
        else:
            await self.callback(self.instance, message)


class Common:
    def __init__(self, **kwargs):

        # Type hinting is used for some of the variables.
        # Don't remove any comments starting with type:
        self.commands_list = {}  # type: Dict[str, Command]

    def add_command(self, cmd):
        """
        Add a command to the commands list.

        Parameters
        ----------
        cmd: Command
            The command to add.
        """
        if cmd.__class__.__name__ is not "Command":
            raise TypeError("{} should be an instance of Command.".format(command))
        elif cmd.name in self.commands_list:
            raise Exception("This command already exists")
        else:
            self.commands_list[cmd.name] = cmd

    def command(self, *args, **kwargs):
        """
        This is a decorator. It invokes :meth:`command` and adds the command
        to the commands list using :meth:`add_command`
        """
        def decorator(func):
            cmd = command(*args, **kwargs)(func)
            self.add_command(cmd)
        return decorator


def command(name=None, **kwargs):
    """
    This function is a decorator. It is used to generate a :class:`Command` object.

    Parameters
    ----------
    name: [Optional] str
        The name of the command. If a name is not provided then the functions
        name ``func.__name__`` is used instead.

    Example
    -------
    .. code-block:: python

        # you don't always have to specify a name.
        # Although specifying a name can be helpful.
        @command()
        async def my_command(ctx):
            await ctx.send_message(message.channel, "Hello")

        @command(name="ping")
        async def _ping(ctx):
            await ctx.send_message(message.channel, "pong")

    Raises
    ------
    TypeError
        The callback function is not a coroutine.
    """

    # TODO: cmd names should be a single word
    def decorator(func):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Command must be a coroutine.")

        else:
            cmd_name = name or func.__name__
            cmd = Command(cmd_name, func, **kwargs)
            return cmd

    return decorator
