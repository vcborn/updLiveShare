import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import discord
from discord.ext import commands
import sys

# Firestoreの処理
# 認証鍵漏れやトークン漏れはセキュリティ的にまずいので[REDACTED]（編集済み）にしてあります。
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "vcborn-member",
  "private_key_id": "[REDACTED]",
  "private_key": "[REDACTED]",
  "client_email": "firebase-adminsdk-mrsd8@vcborn-member.iam.gserviceaccount.com",
  "client_id": "[REDACTED]",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-mrsd8%40vcborn-member.iam.gserviceaccount.com"
})
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection(u'accounts').document(u'liveshare')

# Discord側の処理

TOKEN = "[REDACTED]"
update_date = "2021/10/02"
author = "wamo"
version = "1.0"

bot = commands.Bot(command_prefix=commands.when_mentioned_or('::'))
bot.remove_command("help")
bot.remove_command("exit")

async def on_ready():
    print("ログインしました")
    await bot.change_presence(activity=discord.Game(name='::help | 稼働中'))

@bot.command()
async def get(ctx):
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        embed = discord.Embed(title="完了",description="現在のURLはこちらです。\n" + data["url"],color=0x0076ff)
        embed.set_thumbnail(url="https://dl.wmsci.com/image/40px-info.png")
    else:
        embed = discord.Embed(title="注意",description="ドキュメントがありません！",color=0xffcd30)
        embed.set_thumbnail(url="https://dl.wmsci.com/image/40px-warn.png")
    await ctx.send(embed = embed)

@bot.command()
async def upd(ctx, url=None):
    if not (url):
        embed = discord.Embed(title="注意",description="URLがありません！",color=0xffcd30)
        embed.set_thumbnail(url="https://dl.wmsci.com/image/40px-warn.png")
    else:
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            if not data["url"] == url:
                new = {
                    u'url': url
                }
                db.collection(u'accounts').document(u'liveshare').set(new)
                embed = discord.Embed(title="完了",description="新しいURLに更新しました。",color=0x0076ff)
                embed.set_thumbnail(url="https://dl.wmsci.com/image/40px-info.png")
            else:
                embed = discord.Embed(title="注意",description="そのURLはすでに登録されています。",color=0xffcd30)
                embed.set_thumbnail(url="https://dl.wmsci.com/image/40px-warn.png")
        else:
            embed = discord.Embed(title="注意",description="ドキュメントがありません！",color=0xffcd30)
            embed.set_thumbnail(url="https://dl.wmsci.com/image/40px-warn.png")
    await ctx.send(embed = embed)

@bot.command()
async def about(ctx):
    embed = discord.Embed(title="このBotについて",description='FireStoreのLiveShare URLを更新します。\n\n製作者：' + author + '\nバージョン：v' + version + '\n最終更新日：' + str(update_date),color=0x0076ff)
    embed.set_thumbnail(url="https://dl.wmsci.com/image/40px-info.png")
    await ctx.send(embed = embed)

@commands.command()
async def help(ctx):
    embed = discord.Embed(title="使い方",color=0x0076ff)
    embed.add_field(name="::upd url",value="FireStoreのLiveShare URLを更新します。",inline=False)
    embed.add_field(name="::help",value="このページ",inline=False)
    embed.add_field(name="::about",value="このプログラムについて",inline=False)
    embed.add_field(name="::exit",value="終了",inline=False)
    embed.set_thumbnail(url="https://dl.wmsci.com/image/40px-info.png")
    await ctx.send(embed = embed)
bot.add_command(help)

@commands.command()
async def exit(ctx):
    await bot.logout()
    await sys.exit()
bot.add_command(exit)
    
bot.add_listener(on_ready)

bot.run(TOKEN)