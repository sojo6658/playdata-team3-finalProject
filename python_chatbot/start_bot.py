import morpheme
import mysql
import model

import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle, Interaction

#CONST_GUILD = "your GUILD id"
CONST_TOKEN = "your bot TOKEN"

bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("Bot Is Ready And Online!")
    MY_channel = bot.get_channel("your channel id")
    await MY_channel.send("""온라인 강의를 추천해주는 봇입니다.! \n DM으로 원하는시는 강의를 추천해달라고 해보세요!""")
    
    

@bot.event
async def on_message(message):
    if message.author == bot.user:    #봇이 보낸 메시지면 막기
        return
    else : 
        author = message.author
        author_id = message.author.id
        author_name = message.author.name
        message_contents = message.content
        print("author : ", author)
        print("author_id : ", author_id)
        print("author_name : ", author_name)
        print("message_contents : ", message_contents)
        print("message : ", message)
    if not isinstance(message.channel, discord.DMChannel):
        await message.author.send('''"파이썬 기본 강의 예약해줘" 키워드로 예약하신 강의가 업로드 되었습니다. \n https://www.inflearn.com/course/python-data-security \n https://www.inflearn.com/course/소프트캠퍼스-판다스-데이터분석 \n https://www.inflearn.com/course/자판기-프로그램''')
        return
    if ("추천") in message.content:    #추천기능 -- 구현 
        await message.author.send("알맞는 강의를 찾고 있습니다. 잠시만 기다려 주세요~!")
        #print(morpheme.start_morpheme(message.content))
        keysword = morpheme.filter_my_dictionary(message.content)
        URLs = ''
        for url in model.recommendation(keysword):
            URLs += url + '\n'
        await message.author.send(URLs)
        await message.author.send('위 5개의 강의를 추천합니다.')
        mysql.insert_log(author_id, author, author_name, message_contents, keysword, 2, URLs.replace('\n', '\t')) #메세지 보낸사람및 메세지 저장기능
        #추천 되었을경우 사용자입력코드는 2    
    elif ("예약") in message.content:    #예약기능 -- 미구현
        if ("확인") in message.content or ("취소") in message.content :
            await message.author.send('번호\t예약메세지')
            view = View()
            for output in mysql.select_reservation(author_id):
                await message.author.send(str(output[0])+'번'+'\t'+output[1])
                button1 = Button(label=str(output[0])+' 번', style=ButtonStyle.primary, custom_id=str(output[0]))
                async def button1_callback(interaction: Interaction):
                    print(interaction.data.get('custom_id'))
                    mysql.update_reservation(int(interaction.data.get('custom_id')))
                    await interaction.response.send_message("삭제완료.")
                    await msg.delete()
                button1.callback = button1_callback
                view.add_item(button1)
            await message.author.send("예약확인완료!")
            msg = await message.author.send("삭제할 번호의 버튼을 선택해주세요.", view=view)
        else:
            keysword = morpheme.filter_my_dictionary(message.content)
            mysql.insert_log(author_id, author, author_name, message_contents, keysword, 1, ' ') #메세지 보낸사람및 메세지 저장기능
            await message.author.send("예약완료!")
        #예약 되었을경우 사용자입력코드는 1
    else: #위 키워드가 없을경우 오류 메시지
        await message.author.send("""'예약' 및 '추천' 키워드를 넣어 다시 메세지해주세요""")
        mysql.insert_log(author_id, author, author_name, message_contents, ' ', 0, ' ') #메세지 보낸사람및 메세지 저장기능
        #키워드가 없을경우 사용자입력코드는 0
bot.run(CONST_TOKEN)


