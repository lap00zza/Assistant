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

import discord
import asyncio
import importlib
import inspect
from .core import Common, Command


class Assistant(Common, discord.Client):
    def __init__(self, **kwargs):
        Common.__init__(self)
        discord.Client.__init__(self, **kwargs)

        # Modules Bucket
        self.modules = {}

        # Event listeners store
        self._assistant_listeners = {}

    # Helper function for handling our custom events
    # noinspection PyBroadException
    async def _assistant_handle_event(self, callback, event_name, *args, **kwargs):
        try:
            await callback(self, *args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            try:
                await self.on_error(event_name, *args, **kwargs)
            except asyncio.CancelledError:
                pass

    # Override discords event dispatch so that we
    # can run our own events
    def dispatch(self, event_name, *args, **kwargs):
        super().dispatch(event_name, *args, **kwargs)
        event = 'on_' + event_name
        # print(event)
        if event in self._assistant_listeners:
            for callback in self._assistant_listeners[event]:
                handle = self._assistant_handle_event(callback, event_name, *args, **kwargs)
                discord.compat.create_task(handle, loop=self.loop)

    def add_event_listener(self, callback, event=None):
        """
        Add a new event listener.

        Parameters
        ----------
        callback: coroutine
            The coroutine to call when this event is triggered. The callback
            **must** be a coroutine.

        event: [Optional] str
            The name of the event for which the callback is being registered.
            If a name is not given, ``callback.__name__`` will be used.

        Raises
        ------
        TypeError
            The callback is not a coroutine.
        """
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Listener must be a coroutine.")

        event_name = event or callback.__name__
        if event_name in self._assistant_listeners:
            self._assistant_listeners[event_name].append(callback)
        else:
            self._assistant_listeners[event_name] = [callback]

    def remove_event_listener(self, callback, event=None):
        """
        Remove an event listener.

        Parameters
        ----------
        callback: coroutine
            The coroutine to remove.

        event: [Optional] str
            The name of the event listener to remove. If a name is not given,
            ``callback.__name__`` will be used.
        """
        if event in self._assistant_listeners:
            self._assistant_listeners[event].remove(callback)

    def add_module(self, module):
        """
        Add a new module to Assistant.

        Parameters
        ----------
        module
            The module to add.

        Notes
        -----
        This function is called from the ``load`` function of the module.
        """
        members = inspect.getmembers(module)
        self.modules[type(module).__name__] = module
        # print(self.modules)

        for name, member in members:
            if isinstance(member, Command):
                # Set the instance for the command as
                # the current module. This will be require
                # when we are invoking the function.
                member.set_instance(module)
                self.add_command(member)

    def load_modules(self, name):
        """
        Load a module. Modules are collection of commands and custom event listeners.
        They are stateful. Sample modules can be found in ``/bot/modules`` directory.
        **All modules must have a load function.**

        Parameters
        ----------
        name: str
            The name of the module to load. See Notes for clarification.

        Raises
        ------
        AttributeError
            Module does not have a load function.

        TypeError
            You are trying to access a module using relative path. See Notes for correct
            name convention.

        Notes
        -----
            ::

                +---run.py (or any file with run())
                |
                +---subdirectory---+---hello.py
                                   |
                                   +---hello_again.py

        Modules should be placed in a sub-directory from where run() is used. For example,
        (*using the above diagram as reference*) if the name of your module file is `hello.py`
        and it is placed inside subdirectory then run.py will look something like this:
            .. code-block:: python

                from assistant import Assistant
                my_assistant = Assistant()
                # Remember, no need to append .py
                my_assistant.load_modules("subdirectory.hello")
                my_assistant.run()

        """
        module = importlib.import_module(name)
        module.load(self)

    # NOTE:
    # This on_message is responsible for handling all the
    # commands.This should never be removed from here.
    async def on_message(self, message):
        if message.author.id == self.user.id:
            split_content = message.content.split()
            try:
                command = split_content[0]
                if command in self.commands_list:
                    cmd = self.commands_list[command]
                    await cmd.run_command(message)

            except IndexError as e:
                print(e, message.content)
