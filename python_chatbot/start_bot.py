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
async def on_ready(): #봇 준비 완료시 실행되는 코드
    print("Bot Is Ready And Online!")
    MY_channel = bot.get_channel("your channel id")
    await MY_channel.send("""온라인 강의를 추천해주는 봇입니다.! \n DM으로 원하는시는 강의를 추천해달라고 해보세요!""")
    
    

@bot.event
async def on_message(message): # 봇이 메시지를 있는 모든 곳에서 메시지가 발생했을경우 실행되는 코드
    if message.author == bot.user:    #봇이 보낸 메시지면 막기
        return
    else : #봇이 아닐경우 기본정도 잠시저장
        author = message.author
        author_id = message.author.id
        author_name = message.author.name
        message_contents = message.content
        print("author : ", author)
        print("author_id : ", author_id)
        print("author_name : ", author_name)
        print("message_contents : ", message_contents)
    if not isinstance(message.channel, discord.DMChannel) # 메시지가 DM이 아니리면 막기
        return
    if ("추천") in message.content:    #추천기능 -- 구현 
        await message.author.send("알맞는 강의를 찾고 있습니다. 잠시만 기다려 주세요~!") # 해당기능이 시간이 걸리기때문에 추가
        keysword = morpheme.filter_my_dictionary(message.content) # 코모란에 사용자사전을 이용하여 추출한 키워드를 자체사전과 비교하여 필요한 키워드만 추출
        URLs = ''
        for url in model.recommendation(keysword): # 모델을 이용하여 랭킹을 매겨 상위5개의 URL을 추출
            URLs += url + '\n'
        await message.author.send(URLs)
        await message.author.send('위 5개의 강의를 추천합니다.')
        mysql.insert_log(author_id, author, author_name, message_contents, keysword, 2, URLs.replace('\n', '\t')) #메세지 보낸사람 및 메세지 저장기능
        #추천 되었을경우 사용자입력코드는 2    
    elif ("예약") in message.content:    
        if ("확인") in message.content or ("취소") in message.content : # 예약확인 및 취소 기능
            await message.author.send('번호\t예약메세지')
            view = View()
            for output in mysql.select_reservation(author_id): # 예약한 강의를 DB에서 가져오기
                await message.author.send(str(output[0])+'번'+'\t'+output[1]) # 강의 보여주기
                button1 = Button(label=str(output[0])+' 번', style=ButtonStyle.primary, custom_id=str(output[0]))
                async def button1_callback(interaction: Interaction): #버튼을 눌렀을 경우 해당하는 강의예약 캔슬
                    print(interaction.data.get('custom_id'))
                    mysql.update_reservation(int(interaction.data.get('custom_id')))
                    await interaction.response.send_message("삭제완료.")
                    await msg.delete() #해당 버튼 메시지 삭제
                button1.callback = button1_callback
                view.add_item(button1) 
            await message.author.send("예약확인완료!")
            msg = await message.author.send("삭제할 번호의 버튼을 선택해주세요.", view=view) 
        else: #예약기능
            keysword = morpheme.filter_my_dictionary(message.content) 
            mysql.insert_log(author_id, author, author_name, message_contents, keysword, 1, ' ') #메세지 보낸사람및 메세지 저장기능
            await message.author.send("예약완료!")
        #예약 되었을경우 사용자입력코드는 1
    else: #위 키워드가 없을경우 오류 메시지
        await message.author.send("""'예약' 및 '추천' 키워드를 넣어 다시 메세지해주세요""")
        mysql.insert_log(author_id, author, author_name, message_contents, ' ', 0, ' ') #메세지 보낸사람및 메세지 저장기능
        #키워드가 없을경우 사용자입력코드는 0
bot.run(CONST_TOKEN) # 봇 동작 시작
def scheduler(): # 예약한 키워드에 새로운 강의가 추가되면 보내주는 스케쥴러 향후추가
    pass


