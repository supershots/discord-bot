import discord
import anthropic
import os

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
ai_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """
あなたは就労継続支援の作業をサポートするアシスタントです。
利用者の方が作業中に困ったことを質問するので、
わかりやすく、やさしい言葉で答えてください。
"""

@client.event
async def on_ready():
    print(f"Botが起動しました: {client.user}")

@client.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author == client.user:
        return

    # 特定チャンネルのみ反応させる場合（チャンネル名で絞り込み）
    if message.channel.name != "作業の質問":
        return

    # 「考え中...」と先に返信
    thinking_msg = await message.reply("考え中です...少し待ってね🤔")

    try:
        response = ai_client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message.content}]
        )
        answer = response.content[0].text
        await thinking_msg.edit(content=answer)
    except Exception as e:
        await thinking_msg.edit(content=f"エラー：{e}")

client.run(DISCORD_TOKEN)