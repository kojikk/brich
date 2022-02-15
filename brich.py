import speech_recognition as sr
import pyttsx3
import os
import fuzzywuzzy as fuzz
from fuzzywuzzy import fuzz
import time

name = {
    "brich": ('брич', 'бритч', 'кирпич', 'бреч', 'бирч', 'биртч', 'бреач', 'беарч', 'bridge', 'breach', 'бридж'),
}

#функции
def speak(what):
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

def getConfig(file):
    arr1 = []
    arr2 = []

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines() 

    for line in lines:
        s = line.split(':',1)
        arr1.append(s[0].strip())
        arr2.append(s[1].strip())

    f.close()

    key = []
    val = []

    for i in arr1:
        s = i.split("(")
        s[1] = s[1].replace(')', '')
        key.append(s[0])
        s[1] = tuple(s[1].split(', '))
        val.append(s[1])
    
    cmds_dict = dict()

    for i in range(len(arr1)):
        x = {key[i]:(val[i])}
        cmds_dict.update(x)

    arr1 = cmds_dict

    return(arr1, arr2)

cmds = getConfig('config.txt')[0]

def record_volume():
    r = sr.Recognizer()
    with sr.Microphone(device_index = 1) as source:
        r.adjust_for_ambient_noise(source, duration=0.5) #настройка посторонних шумов
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language = 'ru-RU')
        text = query.lower()
        return text
    except:
        pass

def check_for_name():
    cmd = str(record_volume())    
    if cmd.startswith(name['brich']):
        for x in name['brich']:
                cmd = cmd.replace(x, "").strip()
        print(cmd)
        cmd = recognize_cmd(cmd)
        print(cmd)
        execute_cmd(cmd['rec_cmd'], cmd['percent'])

def recognize_cmd(cmd):
    RC = {'rec_cmd': '', 'percent': 50}
    for c,v in cmds.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['rec_cmd'] = c
                RC['percent'] = vrt
    cmd = RC
    return cmd

def execute_cmd(cmd, percent):
    if cmd == 'time' and percent >= 70:
        clock()
    else:
        try: 
            Arr = list(cmds.keys())
            index = Arr.index(cmd)
            os.startfile(getConfig('config.txt')[1][index])
        except:
            pass
    
#настройки спикера
speak_engine = pyttsx3.init()

##голос
def voice_changer(id):
    voice = ['HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Aleksandr-hq',
             'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Artemiy',
             'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
            ]
    speak_engine.setProperty('voice', voice[id])
voice_changer(1)

##скорость
rate = speak_engine.getProperty('rate')
speak_engine.setProperty('rate', rate-40)

##громкость
volume = speak_engine.getProperty('volume')
speak_engine.setProperty('volume', volume+0.9)

#команды
def clock():
    local_time = time.localtime()
    t = 'время',local_time.tm_hour, 'часов', local_time.tm_min,'минут'
    speak(str(t))

speak('Брич запущен')
print('Брич запущен')

while True:
    check_for_name()