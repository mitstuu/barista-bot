# Barista - An All-Purpose Discord Bot

Barista is a versatile Discord bot designed to enhance user interaction in your server as well as make moderators' lives easier. It welcomes new members, responds to various commands, and provides useful features to keep your server lively and engaging.

## Features

* **Welcoming new members**: Barista sends a warm welcome message to every new member joining your server.
* **Server Info & User Info**: Barista responds to various commands to provide information on the server it is currently in, as well as the userinfo.
* **Revive the Server**: This is a command that users can use to ping an opt-in role to drive traffic towards the channel that it was used in. This has a cooldown to it per-user.

## Getting Started

These instructions will get you a copy of the bot up and running on your local machine for development and testing purposes.

1. Clone the repository: `git clone https://github.com/mitstuu/barista-bot.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Create a new Discord application and obtain a bot token. Follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html) to create a new application and generate a bot token.
4. Create a `.env` file in the root directory of the project and add the following line: `DISCORD_TOKEN=your-bot-token`
5. Run the bot: `python bot.py`
6. The bot should now be online and ready to use in your Discord server.

Please note that these instructions assume you have Python 3.6 or higher installed on your machine.

### Prerequisites

* Python 3.6 or higher
* `discord.py` library
* `python-dotenv` library