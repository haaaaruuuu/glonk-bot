# discord embed
from discord import Embed

# youtube
from googleapiclient.discovery import build
import googleapiclient.errors
import google_auth_oauthlib.flow
import google_auth_httplib2

# datetime
import datetime

# env
import os
from dotenv import load_dotenv

# json
import json


# load api keys
load_dotenv()
go_api_key = os.getenv('A_YOUTUBE')

# social media accs
yt_channel = os.getenv('S_YOUTUBE')
boolT = os.getenv('boolT')
boolI = os.getenv('boolI')
boolM = os.getenv('boolM')
boolP = os.getenv('boolP')
linkT = os.getenv('linkT')
linkI = os.getenv('linkI')
linkM = os.getenv('linkM')
linkP = os.getenv('linkP')

# get playlist of all uploads from channel
# to get most recent upload
# playlist is simply channelid, but replace the 'C' with 'U'
yt_chan_uplist = list(yt_channel)
yt_chan_uplist[1] = "U"
yt_chan_uplist = "".join(yt_chan_uplist)

# getter for info
# makes three api calls
# inefficient i know...
def get_info(key):
    youtube = build('youtube', 'v3', developerKey=key)

    # channel name, channel avatar, subs, views
    firstrequest = youtube.channels().list(
        part='snippet, statistics', 
        id=yt_channel
        )
    stats = firstrequest.execute()
    set_info('ytstats.json', stats)

    # video title, upload date, desc, thumb,
    secondrequest = youtube.playlistItems().list(
        part="snippet",
        maxResults=1,
        playlistId=yt_chan_uplist
    )
    vids = secondrequest.execute()
    set_info('ytvids.json', vids)

    # livestream status + link
    thirdrequest = youtube.search().list(
        part = 'snippet',
        channelId = yt_channel,
        eventType = 'live',
        type = 'video'
    )

    livestatus = thirdrequest.execute()
    set_info('ytlive.json', livestatus)

def set_info(file, info):
    with open(file, 'w') as f:
        json.dump(info, f)

# used in posting board and update board
# 3 requests to update board as well... wow
async def build_board():
    if is_valid() == True:
        # initial requests
        get_info(go_api_key)
        # load json into variables
        with open('ytstats.json') as x:
            ytdata1 = json.load(x)
        
        if ytdata1['pageInfo']['totalResults'] > 0:
            daysago = ""
            channelurl = ytdata1['items'][0]['id']
            channelname = ytdata1['items'][0]['snippet']['title']
            channelicon = ytdata1['items'][0]['snippet']['thumbnails']['default']['url']
            totalviews = ytdata1['items'][0]['statistics']['viewCount']
            totalsubs = ytdata1['items'][0]['statistics']['subscriberCount']

            with open('ytvids.json') as u:
                ytdata2 = json.load(u)
                
            vidtitle = ytdata2['items'][0]['snippet']['title']
            
            viddesc = ytdata2['items'][0]['snippet']['description']
            strdesc = str(viddesc)
            strdesc = strdesc[:int(len(strdesc) * .10)]
            
            vidpub = ytdata2['items'][0]['snippet']['publishedAt']
            vidpub = datetime.datetime.fromisoformat(vidpub[:10])
            now = datetime.datetime.now()
            daysago = str(now - vidpub)
            
            vidthumb = ytdata2['items'][0]['snippet']['thumbnails']['standard']['url']
            vidurl = ytdata2['items'][0]['snippet']['resourceId']['videoId']

            with open('ytlive.json') as w:
                ytdata3 = json.load(w)

            # totalresults can also be >0 AND still be offline wtf
            if ytdata3['pageInfo']['totalResults'] > 0:
                status= ytdata3['items'][0]['liveBroadcastContent']

                if status == 'live':
                    embedColor = 0x00c800
                    liveid = ytdata3['items'][0]['videoId']
                else:
                    embedColor = 0xc80000

                if embedColor == 0x00c800:
                    livevalue = "[NOW STREAMING](https://www.youtube.com/watch?v=" + liveid + ")"
                else:
                    livevalue = "offline..."
            else:
                embedColor = 0xc80000
                livevalue = "offline..."

            linkval = create_link(boolT, boolI, boolM, boolP, linkT, linkI, linkM, linkP)

            embed=Embed(title=vidtitle, url="https://www.youtube.com/watch?v=" + vidurl, description= strdesc + "....", color=embedColor)
            embed.set_author(name=channelname, url="https://www.youtube.com/channel/" + channelurl, icon_url=channelicon)
            embed.set_thumbnail(url=vidthumb)
            embed.add_field(name="Livestream Status", value=livevalue, inline=True)
            embed.add_field(name="Recent Tweet", value='\u200B', inline=False)
            embed.add_field(name='\u200B', value=linkval, inline=False)
            embed.set_footer(text=" Sub Count: " + totalsubs + " | Total Views: " + totalviews + " | Last Uploaded: " + daysago[:2] + "d ago")
        else:
            embed = error_embed()
    else:
        embed = error_embed()

    return embed

def create_link(boolT, boolI, boolM, boolP, linkT, linkI, linkM, linkP):
    link = ""

    if boolT == "True":
        link += "[Twitter](https://twitter.com/" + linkT + ")"
    
    if boolI and boolT == "True":
        link += " | " + "[Instagram](https://instagram.com/" + linkI + ")"
    elif boolI == "True" and boolT == "False":
        link += "[Instagram](https://instagram.com/" + linkI + ")"

    if boolM == "True" and (boolT or boolI) == "True":
        link += " | " + "[Merch](" + linkM + ")"
    elif boolM == "True" and (boolT and boolI) == "False":
        link += "[Merch](" + linkM + ")"

    if boolP == "True" and (boolT or boolI or boolM) == "True":
        link += " | " + "[Patreon](https://patreon.com/" + linkP + ")"
    elif boolP == "True" and (boolT and boolI and boolM) == "False":
        link += "[Patreon](https://patreon.com/" + linkP + ")"

    if link == "":
        link = '\u200B'

    return link

# checks if channel ID is valid
def is_valid():
    x = True

    if yt_channel[:2] != "UC" or not yt_channel:
        x = False

    return x

def error_embed():
    msg = "Channel ID var improperly set."
    suggestions = "Grab Channel ID [here](http://www.youtube.com/account_advanced)"

    with open('ytstats.json') as x:
        ytdata = json.load(x)

    if ytdata['pageInfo']['totalResults'] == 0 and yt_channel[:2] == "UC":
        msg = "Channel not found."
        suggestions = "Verify channel and ID then try again."

    embed=Embed(title="Error:", description=msg, color=0xffffff)
    embed.set_author(name="Exception Raised", url="https://github.com/haaaaruuuu")
    embed.add_field(name="Valid Format:", value="UCGzlNCXyzzaFYHIa_DlXs-w", inline=False)
    embed.add_field(name="Suggestion(s):", value=suggestions, inline=False)
    embed.set_footer(text="-haru", icon_url="https://avatars.githubusercontent.com/u/77024043?s=460&u=7de1214b1fdc75eda2598378f4cf6104a3104934&v=4")
    return embed
