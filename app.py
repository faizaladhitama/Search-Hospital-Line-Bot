# encoding: utf-8
import requests
import os
import json
import jsonpickle

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

#Your Channel Access Token
line_bot_api = LineBotApi("vfKILEFUN3oaz79OgC4XOrPQ9jXbgBrKMdjkuFpEf/Fu9mjOKrR5+ZHEKHW1Qv+ha/vkMjZO2Y5eNcyTmtT7fhdgPhQ6ctgoTL2WeyrZzyUvVaYwduEdAXZ2kH06tHOGjNo7eRezf0puW+tyXc20LgdB04t89/1O/w1cDnyilFU=") 
#Your Channel Secret
handler = WebhookHandler("fb698ed6c00c04a7ced40856bddd6890")

#User send location
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    #source_type = event.source.type
    #state = db[event.source.userId]    
    
    location_obj = event.message
    longitude = location_obj.longitude
    latitude = location_obj.latitude
    address = location_obj.address     
 
    src = event.source
    json_data = jsonpickle.encode(src)    
    print(json_data)    
    data = json.loads(json_data)
    print(data)    
    print(data['user_id'])
    
    try:
        db[str(data['user_id'])] = "{} , {}".format(latitude,longitude)
    except:
        db[str(data['user_id'])] = "{} , {}".format(latitude,longitude)

    reply = "Address : {}\nLongitude : {}\nLatitude : {}\nDatabase : {}".format(address,longitude,latitude,db[str(data['user_id'])])
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply)) #reply the same message from user

#User send text
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user
    reply = text
    if text == "/about":
        reply = "Faizal Adhitama Prabowo\nfaizaladhitamaprabowo@gmail.com"    
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)) #reply the same message from user
    elif text == "/hospital":
        #try:
            reply = "Pengurutan Rumah Sakit dengan jarak terdekat :\n"
            src = event.source
            json_data = jsonpickle.encode(src)    
            print(json_data)    
            data = json.loads(json_data)
            print(data)    
            print(data['user_id'])
            
            LOCATION = db[str(data['user_id'])]
            API_KEY = "AIzaSyDrnC_K1xWhzPFbTe8RXPQgerRTfs2cftg"
            RADIUS_DEFAULT = "1000"
            TYPE = "hospital"
            KEYWORD = "Rumah Sakit"
            LINK = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

            newResult = []
            banned_word = ['pkbi', 'akademi', 'instalasi', 'gedung', 'klinik', 'bedah', 'penyakit', 'clinichek', 'spesialis', 'poli', 'dms', 'sehat', 'apotik', 'anasthesi', 'check', 'terapi', 'jenazah', 'simulasi', 'respirasi', 'kantin', 'mesjid', 'direksi', 'bc', 'uber', 'clinic', 'health', 'care']
            banned_sentence = ['rumah sakit', 'rs', 'kusuma putra']
            
            RADIUS = int(RADIUS_DEFAULT)
            url = LINK + 'location={}&radius={}&type={}&keyword={}&key={}'.format(
                LOCATION, str(RADIUS), TYPE, KEYWORD, API_KEY)
            response = requests.get(url)
            results = response.json()['results']

            for result in results:
                clear = True
                words = result['name'].split(" ")
                for word in words:
                    if word.lower() in banned_word:
                        clear = False
                        break
                name = result['name']
                if clear and name.lower() not in banned_sentence and name not in newResult:
                    newResult.append(name)
            for result in newResult:
                reply += result + "\n"
            print(reply)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply),timeout=10) #reply the same message from user
        #except:            
        #    reply = "Please send your location first"
        #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply)) #reply the same message from user
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
