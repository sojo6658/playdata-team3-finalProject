import morpheme
#import callmodel
import discord
import mysql
from discord.ext import commands
import model
#CONST_GUILD = "1055420078289588254"
CONST_TOKEN = "MTA1NTQyMTc2NDkxNTY5MTU0MQ.GlF08N.zqk9sKOjWm0SiYed4hNj6oonipOi2mLvFFTSaI"

bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("Bot Is Ready And Online!")

@bot.event
async def on_message(message):
    if message.author == bot.user:    #봇이 보낸 메시지면 막기
        return
    
    else : 
        author = message.author
        author_id = message.author.id
        author_name = message.author.name
        message_contents = message.content
        # print("author : ", author)
        # print("author_id : ", author_id)
        # print("author_name : ", author_name)
        # print("message_contents : ", message_contents)
        
    if ("추천") in message.content:    #추천기능 -- 구현 
        #print(morpheme.start_morpheme(message.content))
        keysword = morpheme.get_nouns_text(message.content)
        URLs = ''
        # for url in callmodel.get_URL(keysword):
        #     URLs += url + '\n'
        for url in model.recommendation(keysword):
            URLs += url + '\n'
        await message.channel.send(URLs)
        mysql.insert_log(author_id, author, author_name, message_contents, keysword, 2, URLs.replace('\n', '\t')) #메세지 보낸사람및 메세지 저장기능
        #추천 되었을경우 사용자입력코드는 2    
    elif ("예약") in message.content:    #예약기능 -- 미구현
        await message.channel.send("예약완료!")
        #예약 되었을경우 사용자입력코드는 1
    else: #위 키워드가 없을경우 오류 메시지
        await message.channel.send("""'예약' 및 '추천' 키워드를 넣어 다시 메세지해주세요""")
        #키워드가 없을경우 사용자입력코드는 0
        
bot.run(CONST_TOKEN)