import discord
import os
TOKEN = os.getenv("DISCORD_TOKEN")

# Enable intents so bot can read messages
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
messages = []

@client.event
async def on_message(message):
    if not message.author.bot:
        messages.append({
            "platform": "discord",
            "user": str(message.author),
            "timestamp": str(message.created_at),
            "text": message.content,
            "url": f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        })

# Run the bot
client.run(TOKEN)
