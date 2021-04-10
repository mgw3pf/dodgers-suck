import requests
import re
import os
import discord
from dotenv import load_dotenv
from pprint import pprint
from bs4 import BeautifulSoup
import json

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


def scrape_espn():
    url = "https://www.espn.com/mlb/scoreboard"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    rough_json_data = soup.find(text=re.compile("window.espn.scoreboardData"))
    return rough_json_data

#site_json=json.loads(soup.text)
data = scrape_espn()
data_end_stripped = data[:data.index(';window.espn.scoreboardSettings')]
data_json_formatted = data_end_stripped[data.index('{'):]
data_json = json.loads(data_json_formatted)
response = ""
#data_events = json.loads(data_json['events'][0])
games = data_json['events']
dodgers_home = False
for game in games:
    if "Dodgers" in game['name']: # found the dodgers game
        home_team_runs = game['competitions'][0]['competitors'][0]['score']
        away_team_runs = game['competitions'][0]['competitors'][1]['score']
        teams = game['name'].split(' at ')
        if game['status']['type']['completed']: # if the game is over
            if "Dodgers" in teams[1]: # if true, dodgers are the home team, if false they're away
                dodgers_home = True
                #print(game['status']['type']['completed'])
            if dodgers_home:
                if home_team_runs < away_team_runs:
                    response = "DODGERS LOST!"
                    break
                    # PERFORM DISCORD MESSAGE SEND ACTION, DODGERS LOST
            else:
                if away_team_runs < home_team_runs:
                    response = "DODGERS LOST!"
                    break
                    # PERFORM DISCORD MESSAGE SEND ACTION, DODGERS LOST
            response = "Dodgers won :("
            break
        response = "Dodgers game is not complete."
response = "Dodgers do not play today."

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    await message.channel.send(response)

client.run(TOKEN)

        


            
            
        
#pprint(data_json['events'][0].keys())

