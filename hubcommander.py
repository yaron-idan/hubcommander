"""
.. module: hubcommander
    :platform: Unix
    :copyright: (c) 2017 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.

.. moduleauthor:: Mike Grima <mgrima@netflix.com>
"""
import sys
from rtmbot.core import Plugin

from hubcommander.auth_plugins.enabled_plugins import AUTH_PLUGINS
from hubcommander.bot_components.slack_comm import get_user_data, send_error, send_info
from hubcommander.command_plugins.enabled_plugins import COMMAND_PLUGINS
from hubcommander.config import IGNORE_ROOMS, ONLY_LISTEN
from hubcommander.decrypt_creds import get_credentials

HELP_TEXT = []


def print_help(data):
    text = "I support the following commands:\n"

    for txt in HELP_TEXT:
        text += txt

    text += "`!Help` - This command."

    send_info(data["channel"], text, markdown=True)


COMMANDS = {
    "!help": {"func": print_help, "user_data_required": False},
}


class HubCommander(Plugin):
    def __init__(self, **kwargs):
        super(HubCommander, self).__init__(**kwargs)
        setup(self.slack_client)

    def process_message(self, data):
        """
        The Slack Bot's only required method -- checks if the message involves this bot.
        :param data:
        :return:
        """
        print("A message has arrived with the following text - %s" % (data["text"]))
        if data["channel"] in IGNORE_ROOMS:
            return
        print("Message was not in an ignored room")
        if len(ONLY_LISTEN) > 0 and data["channel"] not in ONLY_LISTEN:
            return
        print("Message was not in an ignored or only listen room")
        # Only process if it starts with one of our GitHub commands:
        command_prefix = data["text"].split(" ")[0].lower()
        if COMMANDS.get(command_prefix):
            process_the_command(data, command_prefix)
            print("Command %s was processed by hubby" % (command_prefix))
        else: 
            print("Command %s was not recognized by hubby" % (command_prefix))


def process_the_command(data, command_prefix):
    """
    Will perform all command_plugins duties if a command_plugins arrived.

    :param data:
    :param command_prefix:
    :return:
    """
    # Reach out to slack to get the user's information:
    user_data, error = get_user_data(data)
    if error:
        send_error(data["channel"], "ERROR: Unable to communicate with the Slack API. Error:\n{}".format(error))
        return

    # Execute the message:
    if COMMANDS[command_prefix]["user_data_required"]:
        COMMANDS[command_prefix]["func"](data, user_data)

    else:
        COMMANDS[command_prefix]["func"](data)


def setup(slackclient):
    """
    This is called by the Slack RTM Bot to initialize the plugin.

    This contains code to load all the secrets that are used by all the other services.
    :return:
    """
    # Need to open the secrets file:
    secrets = get_credentials()
    from . import bot_components
    bot_components.SLACK_CLIENT = slackclient

    print("[-->] Enabling Auth Plugins",file=sys.stderr)
    for name, plugin in AUTH_PLUGINS.items():
        print("\t[ ] Enabling Auth Plugin: {}".format(name),file=sys.stderr)
        plugin.setup(secrets)
        print("\t[+] Successfully enabled auth plugin \"{}\"".format(name),file=sys.stderr)
    print("[V] Completed enabling auth plugins plugins.",file=sys.stderr)

    print("[-->] Enabling Command Plugins",file=sys.stderr)

    # Register the command_plugins plugins:
    for name, plugin in COMMAND_PLUGINS.items():
        print("[ ] Enabling Command Plugin: {}".format(name),file=sys.stderr)
        plugin.setup(secrets)
        for cmd in plugin.commands.values():
            if cmd["enabled"]:
                print("\t[+] Adding command: \'{cmd}\'".format(cmd=cmd["command"]),file=sys.stderr)
                COMMANDS[cmd["command"].lower()] = cmd

                # Hidden commands: don't show on the help:
                if cmd.get("help"):
                    HELP_TEXT.append("`{cmd}` - {help}\n".format(cmd=cmd["command"], help=cmd["help"]))
                else:
                    print("\t[!] Not adding help text for hidden command: {}".format(cmd["command"]),file=sys.stderr)
            else:
                print("\t[/] Skipping disabled command: \'{cmd}\'".format(cmd=cmd["command"]),file=sys.stderr)
        print("[+] Successfully enabled command plugin \"{}\"".format(name),file=sys.stderr)

    print("[V] Completed enabling command plugins.",file=sys.stderr)
