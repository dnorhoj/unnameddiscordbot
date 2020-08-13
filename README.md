# Unnamed Discord Bot

I have no idea what I'll call this bot.

This bot is made in Python 3.8 with the [discord.py](https://github.com/Rapptz/discord.py){:target="_blank"} library

## Table of contents

- [Unnamed Discord Bot](#unnamed-discord-bot)
  - [Table of contents](#table-of-contents)
  - [Setting up](#setting-up)
    - [Create a Discord bot](#create-a-discord-bot)
    - [Create a Reddit application](#create-a-reddit-application)
    - [Installing requirements](#installing-requirements)
    - [Setting up the environment](#setting-up-the-environment)
    - [Running the bot](#running-the-bot)
  - [TODO](#todo)
- [Contributing](#contributing)
- [License](#license)

## Setting up

To set this bot up you need to do a few things.

### Create a Discord bot

1. First off, go to the [Discord developer portal](https://discord.com/developers/applications){:target="_blank"}
2. Log in to your normal discord account
3. Create a new Application
4. Choose a name for the bot and have the team set to Personal
5. Then, in the sidebar, navigate to `Bot`
6. Then press on the button that says `Add Bot`
7. Then choose a username for the bot
8. Press on `Click to Reveal Token`
9. Bam, now you have your token which you will need later.

### Create a Reddit application

This will enable the bot to get memes and other image posts from reddit.

1. Go to [Reddit application preferences](https://www.reddit.com/prefs/apps){:target="_blank"}
2. Register or Log in to Reddit
3. Create a new app by clicking on `Create another app...`
4. Fill out the text fields
5. Choose `web app` as application type
6. You should now see the client id and secret on the page

### Installing requirements

First of all you need to install the requirements.
Make sure that you have python3 and pip3 installed and that they are both in your path. Then run this command:

    pip3 install -U -r requirements.txt

### Setting up the environment

This project requires a few environment variables to work.
To load the environment variables I have chosen to use the Python library, [python-dotenv](https://pypi.org/project/python-dotenv/){:target="_blank"}.

Create a file at `bot/.env` the content should look like this:

    DISCORD_TOKEN="{Your bot token here}"
    praw_client_id="{Reddit client id}"
    praw_client_secret="{Reddit client secret}"

To find your Tokens etc. read [Create a Reddit application](#create-a-reddit-application) and [Create a Discord bot](#create-a-discord-bot)

### Running the bot

NOTE: Please keep in mind that `src/bot.py` shuld be launched from the directory `src/` or else files like `config.json` will not get loaded properly.

The first time you launch `src/bot.py` it will create the file `src/config/config.json` where you can customize the settings to your likings.

## TODO

- [ ] Find a name for the bot (lol)
- [ ] Add more functionality
- [ ] Make better README
- [ ] Clean up code
- [ ] Finish TODO list (lol)

# Contributing

I am not really looking for any contributions, but if you do want to make one, just make a pull request and I will be sure check it out.

# License

This project uses the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/){:target="_blank"} license.

The license is stated in [LICENSE](LICENSE).