# This is Glonk.
Glonk bot is a super simple bot made for YouTubers. The bot displays a 'glonk' of information. It
then updates that glonk every 15 minutes with new information. This is built in a way to reduce clutter, and
prevent bots spamming a text channel with the same link (ie your stream link).


This project is my first exposure to python, rest api, etc. I simply just translated basic knowledge learned from my university classes that use C++ to Python. There's a lot of improvement to be done in all areas.

## What is a glonk?
A glonk is a hub of information that updates on a set interval.

## Glonking
This uses dotenv to control credential variables. To use glonkbot, edit the values of the variables in the '.env' file.

You'll need:

`Google API Key`

`YouTube Channel ID` e.g. https://www.youtube.com/channel/ >>> UCGzlNCXyzzaFYHIa_DlXs-w <<<

You shouldn't have to mess with anything other than the '.env' file to have it working with your details.
### Prerequisites

`discord`

`googleapiclient`

`google_auth_oauthlib`


## Author
haaaaruuuuu


See the bot in action in Glink's Discord Server: https://discord.gg/xtwYypf

This will be a preview of the most recent version before a public update.
## To-do List
* Fetch tweets (will implement once Twitter accepts my dev app....)

* Full exception/input error handling

* Cleaner way to concat 'link' value string

* Clean up logic

* Proper comprehensive logging system

* Everything

