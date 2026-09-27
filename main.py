# Skids Go Away Else I'll kidnap your basements kids




import os
import discord, time, requests, asyncio, random, json, colorama
import re
from discord.ext import commands
from discord.ext import tasks
import wonderwords
from wonderwords import RandomSentence
from datetime import timedelta
from io import BytesIO
import base64
from solver import auth, solve_owo
from captcha_solver import ImageToTextSolver, solve_image_by_scrappey, fetch_hcaptcha_balance, fetch_texttoimage_balance
from colorama import Fore
import sys
sentences = RandomSentence()


version = "1.8" # Logic * 69999999999999999

def clear():
    os.system("title Advanced Auto OwO && cls" if os.name == "nt" else "clear")


with open("config.json") as f:
    config = json.load(f)
try:
    prefix = config.get("prefix")
    token = config.get("token")
    owodm = config['settings']['owodm_channelid']
    captcha_hook_url = config["notifications"]["captcha_alerts"]
    daily_hook_url = config["notifications"]["daily_claim_alerts"]
    huntbot_hook_url = config["notifications"]["huntbot_alert"]
    funds_hook_url = config["notifications"]["funds_alerts"]
    huntbot_key = config["captcha"]["huntbot_key"]
    
except:
    print("no token found")
owochannels = config["settings"]["channel_ids"]
change_channel_after = config["settings"]["channel_change_interval"]
owochannel = 0



    
banner = """

              _                               _                 _           ____                
     /\\      | |                             | |     /\\        | |         / __ \\               
    /  \\   __| |_   ____ _ _ __   ___ ___  __| |    /  \\  _   _| |_ ___   | |  | |_      _____  
   / /\\ \\ / _` \\ \\ / / _` | '_ \\ / __/ _ \\/ _` |   / /\\ \\| | | | __/ _ \\  | |  | \\ \\ /\\ / / _ \\ 
  / ____ \\ (_| |\\ V / (_| | | | | (_|  __/ (_| |  / ____ \\ |_| | || (_) | | |__| |\\ V  V / (_) |
 /_/    \\_\\__,_| \\_/ \\__,_|_| |_|\\___\\___||__,_| /_/    \\_\\__,_|\\__\\___/   \\____/  \\_/\\_/ \\___/ 
                    ____                _______ _                                                
                   |  _ \\           ___|__   __| |            /\\                                 
                   | |_) |_   _    / __ \\ | |  | |__   ___   /  \\   __  _____  ___               
                   |  _ <| | | |  / / _` || |  | '_ \\ / _ \\ / /\\ \\  \\ \\/ / _ \\/ __|              
                   | |_) | |_| | | | (_| || |  | | | |  __// ____ \\  >  <  __/\\__ \\              
                   |____/ \\__, |  \\ \\__,_||_|  |_| |_|\\___/_/    \\_\\/_/\\_\\___||___/              
                           __/ |   \\____/                                                        
                          |___/                                                                  

"""
user_data = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).json()
globalname = user_data.get("global_name")
if not globalname:
    print(f"{Fore.RED}[Error] Incorrect Token Provided{Fore.RESET}")
    os.system('exit')

all_tasks = []
all_tasks_stop = []

# New variables for spam farming
farming_active = False
farming_task = None
user_token = None
target_channel = None
message_to_send = "owo h\nowo b"
interval = 25


def create_tasks():
    global all_tasks
    global all_tasks_stop
    plugins = config["plugins"]
    try:
        if plugins["autohunt"] == "true":
            all_tasks.append(autohunter)
            all_tasks_stop.append(autohunter)
        if plugins["autolevelup"] == "true":
            all_tasks.append(autolevelup)
            all_tasks_stop.append(autolevelup)
        if plugins["autoslot"] == "true":
            all_tasks.append(autoslot)
            all_tasks_stop.append(autoslot)
        if plugins["autocoinflip"] == "true":
            all_tasks.append(autocf)
            all_tasks_stop.append(autocf)
        if plugins["autopray"] == "true":
            all_tasks.append(autopray)
            all_tasks_stop.append(autopray)
        if plugins["autosell"] == "true":
            all_tasks.append(autosell)
            all_tasks_stop.append(autosell)
        if plugins["use_random_commands"] == "true":
            all_tasks.append(autorandomcommand)
            all_tasks_stop.append(autorandomcommand)
        if plugins["autohuntbot"] == "true":
            all_tasks.append(autohuntbot)
            all_tasks_stop.append(autohuntbot)
    except Exception as e:
        print(e)
    print("")
    try:
       
        all_tasks.append(owobalace)
        all_tasks.append(autodaily)
        all_tasks.append(autosleep)
        all_tasks.append(auto_channelchange)
        all_tasks.append(balanace_alerts)
        all_tasks_stop.append(autodaily)
        all_tasks_stop.append(owobalace)
        all_tasks_stop.append(autosleep)
        all_tasks_stop.append(auto_channelchange)
        all_tasks_stop.append(balanace_alerts)

    except Exception as e:
        print(e)


client = commands.Bot(
    description="Advanced Auto OwO",
    command_prefix=prefix,
    case_insensitive=True,
    self_bot=True,
    help_command=None,
    sync_presence=False
)


def check_version():
    r = requests.get(
        "https://raw.githubusercontent.com/TheAxes/Advance-Auto-Owo/main/Current-version.txt"
    )
    if r.text.rstrip() == version:
        return ""
    else:
        print(r.text)
        return f"{Fore.LIGHTMAGENTA_EX}A Newer Version Is Available: {r.text}\nConsider updating it: https://github.com/TheAxes/Advance-Auto-Owo{Fore.RESET}"


def get_entry():
    file_path = "entry.json"
    with open(file_path, "r") as file:
        data = json.load(file)
        cowoncy, nextdaily, cookie, nexthuntbot = (
            data.get("cowoncy", ""),
            data.get("nextdaily", ""),
            data.get("cookie", ""),
            data.get("nexthuntbot")
        )
        return cowoncy, nextdaily, cookie, nexthuntbot, 


def update_entry(new_cowoncy=None, new_nextdaily=None, new_cookie=None, new_nexthuntbot=None):
    file_path = "entry.json"
    with open(file_path, "r+") as file:
        data = json.load(file)
        if new_cowoncy is not None:
            data["cowoncy"] = new_cowoncy
        if new_nextdaily is not None:
            data["nextdaily"] = new_nextdaily
        if new_cookie is not None:
            data["cookie"] = new_cookie
        if new_nexthuntbot is not None:
            data["nexthuntbot"] = new_nexthuntbot
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def solvecap(problem, lambaa=None):
    if problem == "https://owobot.com/captcha":
        cooked = get_entry()[2]
        sol = solve_owo(cooked)
        return f"{sol}|hcap"
    else:
        sol = ImageToTextSolver(image=problem, length=lambaa, mode='captcha')
        return f"{sol}|image"


def sendhook(hook_url, content, description, image_url):
    payload = {
        "username": "OwO Logger",  # Set the username here
        "content": content,
        "embeds": [
            {
                "title": "Auto OwO",
                "description": description,
                "image": {
                    "url": image_url
                },
                "footer": {
                    "text": "Made By @Theaxes",
                    "icon_url": "https://images-ext-1.discordapp.net/external/LEdJvbRy1zsqteshdxeKJ9sk5GCksjlNwiEO5_bCYhk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/824522317899235360/2cbb49[...]
                },
            }
        ],
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(hook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"{Fore.LIGHTGREEN_EX}[Notification] Sent A Webhook{Fore.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[Notification] Unable to Sent A Webhook: {e}{Fore.RESET}")


@client.event
async def on_connect():
    print("please wait, bot loading")
    create_tasks()
    
    clear()
    print(f"{Fore.LIGHTCYAN_EX}{banner}{Fore.RESET}")
    print(f"Account : {globalname}")
    print(f"prefix : {prefix}")
    print(check_version())
    await client.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Auto OwO",
            details="Made By @TheAxes",
            timestamps={"start": time.time()},
            state="youtube.com/@theaxes",
            buttons=["TheAxes", "Made Only For You ❤️"],
            metadata=["https://youtube.com/@theaxes", "https://youtube.com/@theaxes"],
            assets=
    {"large_image": "https://media.discordapp.net/attachments/1336378795665657958/1341091056351051776/2cbb4933cb3c03a205f4ed85167a8530.png?ex=67b4bbe0&is=67b36a60&hm=b47625464d95638d8b40be15d6502[...]
    "large_text": "axesarecool",
    "small_image": "https://media.discordapp.net/attachments/1115605458602971157/1341089828187668572/1a449430e3a9a830efebb8c57917f943.png?ex=67b4babb&is=67b3693b&hm=d8cf73451fc369c56439986d608a33[...]
    "small_text": "uwuuwu"
        }), 
    )

def normalize_message(content):
    # Remove zero-width characters or any unintended space splitting
    return re.sub(r"\s+", " ", content.replace("\u200b", ""))

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot:
        if message.author.id == 408785106942164992:
                # Check for captcha detection messagetent 
                message.content = normalize_message(message.content)
                if message.channel.id in owochannels or message.channel.id == owodm:
                    if ("⚠️" in message.content) and (("letter word" in message.content)
                    or ("link" in message.content or "https://owobot.com" in message.content)
                ):
                        for task in all_tasks_stop:
                            task.cancel()
                        captchamsg = message.jump_url
                        try:
                            captcha = message.attachments[0].url
                        except:
                            captcha = "https://owobot.com/captcha"
                        sendhook(hook_url=captcha_hook_url,
                        content=f"@everyone Captcha Alert!",
                        description=f"A Captcha Has Been Detected!\n*Captcha Message*: [Jump to Message]({captchamsg})", image_url="https://images-ext-1.discordapp.net/external/mflqo1HcoLk6g1HEXd[...]
                        
                        if "letter word" in message.content:
                            solution = solvecap(
                            captcha, lambaa=message.content[message.content.find("letter word") - 2]
                        )
                        else:
                            cook = auth(token=token)
                            if cook is None:
                                return
                            else:
                                update_entry(new_cookie=cook)
                            print(f"{Fore.GREEN}Solving Hcaptcha{Fore.RESET}")
                            solution = solvecap(captcha, lambaa=None)
                        user = client.get_user(408785106942164992)
                        if solution.split("|")[1] == "image":
                            await user.send(solution.split("|")[0])
                            try:
                                    verification_message = await asyncio.wait_for(
                                    client.wait_for(
                                        "message", check=lambda m: m.author == message.author
                                        and "I have verified that you are human! Thank you! :3"
                                        in m.content
                                        ), timeout=240)
                                    if "I have verified" in verification_message.content:
                                        channel = client.get_channel(owochannel)
                                        sendhook(hook_url=captcha_hook_url, content=f"@everyone Captcha Alert!", description=f"Captcha Has Been Solved!", image_url="https://images-ext-1.discordap[...]
                                        await channel.send(f"{prefix}autoowo")
                                    else:
                                        sendhook(hook_url=captcha_hook_url, image_url="https://images-ext-1.discordapp.net/external/mflqo1HcoLk6g1HEXdHLOBbKSVZ8Lq690mXrNA3yeX4/https/repository-im[...]
                                        time.sleep(4)
                                        sys.exit()
                            except asyncio.TimeoutError:
                                print(f"{Fore.RED}[Timeout] captcha timed out.{Fore.RESET}")
                                sendhook(hook_url=captcha_hook_url, image_url="https://images-ext-1.discordapp.net/external/mflqo1HcoLk6g1HEXdHLOBbKSVZ8Lq690mXrNA3yeX4/https/repository-images.git[...]
                                time.sleep(5)
                                sys.exit()
                        elif solution.split("|")[0] == "solved":
                            channel = client.get_channel(owochannel)
                            sendhook(hook_url=captcha_hook_url, content=f"@everyone Captcha Alert!", description=f"Captcha Has Been Solved!", image_url="https://images-ext-1.discordapp.net/extern[...]
                            await channel.send(f"{prefix}autoowo")
                        else:
                            sendhook(hook_url=captcha_hook_url, image_url="https://images-ext-1.discordapp.net/external/mflqo1HcoLk6g1HEXdHLOBbKSVZ8Lq690mXrNA3yeX4/https/repository-images.githubu[...]
                            time.sleep(4)
                            sys.exit()
                        
                    
                    elif "nu" or "your next" or "your daily" in message.content.lower():
                        if globalname in message.content:
                            target_message = message
                            if "nu" in target_message.content.lower():
                                pattern = r"(\d+)H (\d+)M (\d+)S"
                                match = re.search(pattern, target_message.content)
                                hours = int(match.group(1))
                                minutes = int(match.group(2))
                                seconds = int(match.group(3))
                                total_seconds = hours * 3600 + minutes * 60 + seconds
                                next_daily = time.time() + total_seconds
                                update_entry(new_nextdaily=next_daily)
                                print(
                                    f"{Fore.LIGHTYELLOW_EX}[Logger] Your Next Daily: {str(timedelta(seconds=total_seconds))}s{Fore.RESET}"
                                )
                            else:
                                return
                else:
                    return 
                
def change_channel():
    global owochannel
    new_owochannel = random.choice(owochannels)
    after = client.get_channel(new_owochannel)
    owochannel = new_owochannel
    print(f"{Fore.YELLOW}[Logger] Set OwO Channel To #{after.name}")

@tasks.loop(seconds=random.randrange(16, 45))
async def autohunter():
    channel = client.get_channel(owochannel)
    await channel.typing()
    await asyncio.sleep(2)
    await channel.send("owo hunt")
    await asyncio.sleep(15)
    await channel.send("owo battle")


@tasks.loop(minutes=random.randrange(5, 7))
async def autopray():
    channel = client.get_channel(owochannel)
    await asyncio.sleep(15)
    await channel.typing()
    await channel.send("owo pray")


@tasks.loop(seconds=random.randrange(15, 60))
async def autolevelup():
    channel = client.get_channel(owochannel)
    await channel.typing()
    await asyncio.sleep(11)
    xp = random.choice(("owo", "UwUUwU", "uwu"))
    message = random.choice((xp, f"{sentences.sentence()}owo"))
    await channel.send(message)
    await asyncio.sleep(3)


@tasks.loop(minutes=5)
async def autodaily():
    channel = client.get_channel(owochannel)
    if not get_entry()[1] - time.time() <= 0:
        return
    await channel.typing()
    await asyncio.sleep(3)
    await channel.send("owo daily")
    daily_message = await asyncio.wait_for(
                            client.wait_for(
                                "message",
                                check=lambda m: "Here is your daily"
                                in m.content,
                            ),
                            timeout=60,
                        )
    if daily_message:
        sendhook(content="Daily Alert!!", description="A Daily Has been Claimed", hook_url=daily_hook_url, image_url="https://cdn.discordapp.com/emojis/427352600476647425.webp?size=56&quality=los[...]
    await channel.send("owo cookie <@408785106942164992>")


@tasks.loop(minutes=10)
async def autosell():
    channel = client.get_channel(owochannel)
    await asyncio.sleep(16)
    await channel.send(f"owo sell {config['settings']['animal_types']}")


@tasks.loop(minutes=8)
async def autoslot():
    channel = client.get_channel(owochannel)
    amount = random.choice(config["settings"]["slotamount"])
    await channel.send(f"owo s {amount}")

@tasks.loop(minutes=5)
async def autocf():
    channel = client.get_channel(owochannel)
    amount = random.choice(config["settings"]["autocoinflip_amount"])
    await channel.send(f"owo cf {amount}")


@tasks.loop(minutes=15)
async def owobalace():
    channel = client.get_channel(owochannel)
    await asyncio.sleep(5)
    await channel.send(f"owo cash")
    balance_message = await asyncio.wait_for(
                            client.wait_for(
                                "message",
                                check=lambda m: "cowoncy" 
                                in m.content,
                            ),
                            timeout=60,
                        )
    if "cowoncy" in balance_message.content and not "sent" in balance_message.content:
                pattern = r"\| {}\*\*, you currently have \*\*__([\d,]+)__ cowoncy!".format(
                    re.escape(globalname)
                )
                match = re.search(pattern, balance_message.content)
                if match:
                    cowoncy_amount = match.group(1).replace(",", "")
                    print(
                        f"{Fore.LIGHTYELLOW_EX}[Logger] You Have {cowoncy_amount} Cowoncy{Fore.RESET}"
                    )
                    update_entry(new_cowoncy=cowoncy_amount)
                return
            


@tasks.loop(minutes=random.randrange(15, 20))
async def autosleep():
    tosleep =random.randrange(3, 8)
    print(f"{Fore.LIGHTGREEN_EX}[Sleeper] Bot Sleeping for {tosleep} Minutes{Fore.RESET}")
    all_tasks_stop.remove(autosleep)
    if config['plugins']["autohuntbot"] == "true":
        all_tasks_stop.remove(autohuntbot)
    try:
        for task in all_tasks_stop:
            task.cancel()
    except RuntimeError:
        return
    await asyncio.sleep(tosleep*60)
    all_tasks_stop.append(autosleep)
    if config['plugins']["autohuntbot"] == "true":
        all_tasks_stop.append(autohuntbot) 
    print(f"{Fore.LIGHTGREEN_EX}[Sleeper] Bot Again Resumed{Fore.RESET}")
    try:
        for task in all_tasks:
            task.start()
            await asyncio.sleep(5)
    except RuntimeError:
        return
    
def extract_amount(text):
    pattern = r'owo\s+autohunt\s+(\d+)'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    else:
        return None
    
@tasks.loop(minutes=6)
async def autohuntbot():
    channel = client.get_channel(owochannel)
    if not get_entry()[3] - time.time() <= 0:
        return
    else:
        await asyncio.sleep(3)
        await channel.send("owo autohunt")
        await asyncio.sleep(30)
        await channel.send("owo autohunt 1d")
        amount_message = await asyncio.wait_for(
                            client.wait_for(
                                "message",
                                check=lambda m: "password"
                                in m.content,
                            ),
                            timeout=60,
                        )
        if amount_message.attachments[0].url:
            password = requests.post("https://huntbot-api.vercel.app/process_image", json={"image_url": amount_message.attachments[0].url , "api_key": huntbot_key}).json()['result']
            amount = extract_amount(amount_message.content)
            await channel.send(f"owo autohunt {amount} {password} ")
            huntbot_msg = await asyncio.wait_for(
                            client.wait_for(
                                "message",
                                check=lambda m: "I WILL BE BACK IN"
                                in m.content,
                            ),
                            timeout=60,
                        )
            time_str = re.search(r'(\d+)M', huntbot_msg.content)
            minutes = int(time_str.group(1)) + 2
            seconds = minutes * 60
            sendhook(hook_url=huntbot_hook_url, content="HuntBot Alert!!", description=f"Huntbot Started!!\n[Jump to Message]({huntbot_msg.jump_url})", image_url="https://images-ext-1.discordapp.[...]
            update_entry(new_nexthuntbot=time.time() + seconds)
            await asyncio.sleep(seconds) 
        else:
            await asyncio.sleep(180) 



@tasks.loop(seconds=random.randrange(35, 120))
async def autorandomcommand():
    channel = client.get_channel(owochannel)
    await channel.typing()
    msg = random.choice(config['settings']['random_commands'])
    await channel.send(f"owo {msg}")
    await asyncio.sleep(3)

@tasks.loop(minutes=2)
async def balanace_alerts():
    hbal = fetch_hcaptcha_balance()
    txtbal = fetch_texttoimage_balance()
   
    if hbal and txtbal < 0:
        sendhook(description="Keys Ran Out Of Funds Please Refill ANd then Restart Bot", hook_url=funds_hook_url, content="@everyone Bot Stopped!!", image_url="https://media.discordapp.net/attach[...]
        sys.exit()
    else:
        return


@tasks.loop(minutes=random.choice(change_channel_after))
async def auto_channelchange():
    change_channel()

# New Commands for Spam Farming

class ChannelSelect(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = []
        for guild in client.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    options.append(
                        discord.SelectOption(
                            label=f"{channel.name} ({guild.name})",
                            value=str(channel.id)
                        )
                    )
        super().__init__(
            placeholder="Select a channel to send messages",
            options=options[:25]
        )

    async def callback(self, interaction: discord.Interaction):
        global target_channel
        target_channel = int(self.values[0])
        await interaction.response.defer()


class SetupView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.add_item(ChannelSelect(ctx))

    @discord.ui.button(label="Start Farming", style=discord.ButtonStyle.green)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global farming_active, farming_task, user_token, target_channel
        
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Only the command user can use this!", ephemeral=True)
            return
        
        if target_channel is None:
            await interaction.response.send_message("Please select a channel first!", ephemeral=True)
            return
        
        await interaction.response.send_message("Enter your user token (in next 30 seconds):", ephemeral=True)
        
        try:
            msg = await client.wait_for('message', timeout=30, check=lambda m: m.author == interaction.user)
            user_token = msg.content.strip()
            await msg.delete()
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout! Setup cancelled.", ephemeral=True)
            return
        
        farming_active = True
        farming_task = asyncio.create_task(spam_loop())
        await interaction.followup.send(f"Farming started! Sending messages to <#{target_channel}>", ephemeral=True)

    @discord.ui.button(label="Stop Farming", style=discord.ButtonStyle.red)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global farming_active, farming_task
        
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Only the command user can use this!", ephemeral=True)
            return
        
        farming_active = False
        if farming_task:
            farming_task.cancel()
        await interaction.response.send_message("Farming stopped!", ephemeral=True)


async def spam_loop():
    global farming_active, user_token, target_channel
    
    headers = {"Authorization": user_token}
    
    while farming_active:
        try:
            payload = {"content": message_to_send}
            response = requests.post(
                f"https://discord.com/api/v9/channels/{target_channel}/messages",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[Farming] Message sent successfully!{Fore.RESET}")
            elif response.status_code == 429:
                print(f"{Fore.YELLOW}[Farming] Rate limited, waiting...{Fore.RESET}")
                await asyncio.sleep(5)
            else:
                print(f"{Fore.RED}[Farming] Error: {response.status_code} - {response.text}{Fore.RESET}")
                farming_active = False
                break
            
            await asyncio.sleep(interval)
        except Exception as e:
            print(f"{Fore.RED}[Farming] Error: {e}{Fore.RESET}")
            farming_active = False
            break


@client.command()
async def setup(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Only administrators can use this command!")
        return
    
    await ctx.send("Setup Panel", view=SetupView(ctx))


@client.command()
async def help(ctx):
    msg = f'''
    ```ini
    [Made By @TheAxes]
      [Help Command]
⁙ {prefix}autoowo - Starts Farming OwO Automatically
⁙ {prefix}stopautoowo - stops Farming OwO
⁙ {prefix}setup - Opens setup panel for custom farming (Admin Only)
⁙ {prefix}chhservicekey (new key) - changes hcaptcha service key
⁙ {prefix}chtexttoimagekey (new key) - changes texttoimage service key
⁙ {prefix}balance - returns each service balances
⁙ {prefix}info - returns the instance info along other details
    ```
        [Github.com/TheAxes]
'''
    await ctx.send(f"{msg}")


@client.command()
async def autoowo(ctx):
    wait =random.randrange(3, 8)
    await ctx.send("> Started Auto OwO")
    change_channel()
    try:
        for task in all_tasks:
            task.start()
            await asyncio.sleep(wait)
    except RuntimeError:
        return


@client.command()
async def stopautoowo(ctx):
    await ctx.send("> Stopped Auto OwO")
    try:
        for task in all_tasks_stop:
            task.cancel()
    except RuntimeError:
        return
    
def update_json(file_path, key_path, new_value):
    # Read the original file content
    with open(file_path, 'r') as file:
        original_content = file.read()
    
    # Parse the JSON data from the content
    data = json.loads(original_content)
    
    # Traverse the JSON object to update the specific value
    keys = key_path.split('.')
    temp_data = data
    for key in keys[:-1]:
        temp_data = temp_data[key]
    temp_data[keys[-1]] = new_value
    
    # Convert the updated JSON data to a formatted string
    updated_json_str = json.dumps(data, indent=2)
    
    # Use regex to replace the old value with the new value while keeping the original formatting intact
    def replace_value(match):
        return f'"{key_path}": "{new_value}"'
    
    # Find the value to replace in the original content
    pattern = re.compile(rf'"{key_path}":\s*".*?"')
    formatted_content = pattern.sub(replace_value, original_content)

    # Write the formatted content back to the file
    with open(file_path, 'w') as file:
        file.write(formatted_content)

@client.command()
async def chhservicekey(ctx, key=None):
    if key is None:
        await ctx.reply("`providing a hcaptcha_key key is must`")
    else:
        file_path = 'config.json'
        update_json(file_path=file_path, key_path='captcha.hcaptcha_key', new_value=key)
        await ctx.message.delete()
        await ctx.send("`Updated hcaptcha_key Key Successfully`")

@client.command()
async def chtexttoimagekey(ctx, key=None):
    if key is None:
        await ctx.reply("`providing a TextToImage_key key is must`")
    else:
        file_path = 'config.json'
        update_json(file_path=file_path, key_path='captcha.TextToImage_key', new_value=key)
        await ctx.message.delete()
        await ctx.send("`Updated TextToImage_key Key Successfully`")

@client.command()
async def balance(ctx):
    message = await ctx.send('`Fetching balance...`')
    hbal = fetch_hcaptcha_balance()
    txtbal = fetch_texttoimage_balance()
    msg = f'''
```ini
    [Balance]

  Hcaptcha Balance: "{hbal}"    
  TextToImage Balance: "{txtbal}"   
```
'''
    await message.edit(content=msg)

@client.command()
async def info(ctx):
    message = await ctx.reply("`fetching details...`")
    ping = client.latency * 1000
    r = requests.get(
        "https://raw.githubusercontent.com/TheAxes/Advance-Auto-Owo/main/Current-version.txt"
    )
    ver = r.text.rstrip()
    msg = f'''```ini
    [ Adv Auto OwO | Information ]

User: "{globalname}"
Latency: "{ping}ms"
Version: "{ver}"
Hservice: "{config['captcha']['hcaptcha_service']}"
TextToImage Service: "{config['captcha']['TextToImage_service']}"
Current OwO Channel: "{owochannel}"
OwO Dm Channel: "{owodm}"
Src: "https://github.com/TheAxes/Advance-Auto-Owo.git"
Dev: "https://guns.lol/theaxes"
```
'''
    await message.edit(content=msg)

client.run(token)
