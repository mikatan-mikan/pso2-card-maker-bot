from collections import deque
import discord
from PIL import Image,ImageDraw,ImageFont
import requests
from copy import deepcopy

card_image = Image.open("./assets/make_card/main.png")
make_card_list = ["所在SHIP","メインキャラ名","プレイスタイル","好きなキャラ","PSOで好きな事"]
client = discord.Client()

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)


@client.event
async def on_message(msg):
    if msg.author.bot:
        return


    non_space_msg = msg.content.replace(" ","")

    record_space = non_space_msg.split(" ")

    enter_to_space_msg = non_space_msg.replace("\n"," ")
    enter_to_space_msg = enter_to_space_msg.split(" ")
    delete_list = []
    for i in range(len(enter_to_space_msg)):
        enter_to_space_msg[i].replace(" ","")
        if enter_to_space_msg[i] == "":
            delete_list.append(i)
    delete_list.reverse()
    for i in delete_list:
        del enter_to_space_msg[i]
    record_enter = enter_to_space_msg
    if msg.content.startswith('/make_card'):
        for i in range(len(record_enter)):
            record_enter[i] = record_enter[i].split(":")
        tmp = deepcopy(card_image)
        font_size = 56
        font_path = 'C:\Windows\Fonts\meiryo.ttc'
        font = ImageFont.truetype(font_path,font_size)
        p_wid , p_hei = tmp.width , tmp.height
        text_image = Image.new(mode="RGBA",size=(p_wid,p_hei),color=(0,0,0,0))
        draw_pic = ImageDraw.Draw(text_image)
        try:
            record_enter[-1][1]
            minus_len = 0
        except:
            minus_len = 1
        for i in range(1 , min(len(record_enter) - minus_len , 8)):
            if i <= 5:
                if record_enter[i][0] != make_card_list[i - 1]:
                    await msg.channel.send("項目5までは固定の項目です。\nもう一度コマンドを打ちなおしてください")
                    return
            t_wid , t_hei = draw_pic.textsize(record_enter[i][1],font)
            draw_pic.text((400,136 + 104 * i),record_enter[i][0],fill=(255,255,255,255),font=font)
            draw_pic.text((p_wid - t_wid - 360,136 + 104 * i),record_enter[i][1],fill=(255,255,255,255),font=font)
            #text_image.show()
        put_intro = ""
        if minus_len == 1:
            #for i in range(len(record_enter[-1][0])):
            while True:
                t_wid , t_hei = draw_pic.textsize(record_enter[-1][0][:i],font)
                if t_wid > 1200:
                    put_intro += record_enter[-1][0][:i] + "\n"
                    #print(put_intro)
                    record_enter[-1][0] = record_enter[-1][0][i:]
                    i = 0
                i += 1
                if i - 1 == len(record_enter[-1][0]):
                    put_intro += record_enter[-1][0]
                    break
            draw_pic.text((1320,1040),put_intro,fill=(255,255,255,255),font=font)
        #tmp.show()
        #try:
        try:
            url = msg.attachments[0].url
            download_img(url,"./assets/make_card/dl_im.png")
            up_im = Image.open("./assets/make_card/dl_im.png")
            if up_im.width * 79 < up_im.height * 184:
                up_im = up_im.resize((int(up_im.width * (361 / up_im.height)),361))
            else:
                up_im = up_im.resize((736,int(up_im.height * (736 / up_im.width))))
            #up_im = up_im.resize((736,356))
            tmp.paste(up_im,(408 + int((736 - up_im.width) / 2),1132 + int((356 - up_im.height) / 2)))
                #102-286 283 - 374
        except:pass
        tmp = Image.alpha_composite(tmp,text_image)# tmp.paste(text_image)#tmpに入力された文字を入れていく
        #tmp.show()
        tmp.save("./assets/make_card/out.png")
        await msg.channel.send(file = discord.File("./assets/make_card/out.png"))
    if msg.content.startswith('/help'):
        if msg.content != "/help":
            await msg.channel.send("不必要な文字が付加されています")
            return
        await msg.channel.send("/make_card\n```自己紹介をアークスカード風に作成します。\n/makecard\n<[必須]自己紹介テンプレを書く(/intr_temで内容確認)>\n<追加の紹介を 題:内容 でふたつ（二行）まで>\n<自由にどうぞ(4行に収まらないと悲惨かも(？))>\n<画像を添付>```\n/intr_tem\n```自己紹介テンプレートを表示します```")
    if msg.content.startswith('/intr_tem'):
        if msg.content != "/intr_tem":
            await msg.channel.send("不必要な文字が付加されています")
            return
        await msg.channel.send("所在SHIP:<内容>\nメインキャラ名:<内容>\nプレイスタイル:<内容>\n好きなキャラ:<内容>\nPSOで好きな事:<内容>")

client.run(token)
