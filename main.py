import discord
from discord.ext import commands
from discord import app_commands
import requests
import random as rd
from typing import Optional
import threading
import time
token = ""
bot = commands.Bot(command_prefix = '>',intents = discord.Intents.all(),case_insensitive = True)


@bot.command()
@commands.is_owner()
@commands.guild_only()
async def sync(ctx):
    ctx.bot.tree.copy_global_to(guild=ctx.guild)
    synced = await ctx.bot.tree.sync(guild=ctx.guild) #owner of the bot can sync commands to the guild the bot currently is in
    await ctx.send(f"Synced {len(synced)} commands to the current guild.")
    
 
worked = 0
failed = 0
@app_commands.describe(url = "Url to the ebay product",views = "Amount of views to add")
@bot.tree.command(description = "Send views to an ebay product")
async def ebay(interaction:discord.Interaction,url:str,views:int):
    global worked, failed
    path = url.replace("https://","").split("/")[1:]
    path = '/'.join(path)
    headers = {
    "authority": "www.ebay.co.uk",
    "method": "GET",
    "path": path,
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}
    def send_views(url,t_views):
        global worked, failed
        for i in range(t_views):
            proxy = rd.choice(proxies)
            spl = proxy.split(':')
            proxy = f'{spl[2]}:{spl[3]}@{spl[0]}:{spl[1]}'
            proxy = {"http://":proxy,"https://":proxy}
            resp = requests.get(url,headers=headers,proxies=proxy)
            if resp.status_code == 200:
                with lock:
                    worked += 1
            else:
                with lock:
                    failed += 1
            time.sleep(0.1)
    num_threads = (views + 9) // 10
    dviews = views // num_threads
    remainder = views % num_threads
    threads = []
    await interaction.response.send_message(f"Attempting to send {views} views to {url}...")
    lock = threading.Lock()
    for i in range(num_threads):
        if i < remainder:
            t_views = dviews + 1
        else:
            t_views = dviews
        t = threading.Thread(target=send_views, args=(url,t_views,), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    await interaction.followup.send(f"Successfully added {worked} views to {url} | Failed: {failed}")
    worked = 0
    failed = 0
    
    
# put proxies in a proxies.txt file
proxies = []
with open("proxies.txt", 'r') as f:
        lines = f.read().split("\n")
        for line in lines:
            proxies.append(line)
bot.run(token)
