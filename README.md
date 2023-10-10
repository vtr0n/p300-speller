## P300 speller
Simple p300 speller using Emotiv Epoc X

![image](https://user-images.githubusercontent.com/18473198/204102355-c35363bf-cc59-45a4-b1cf-f6352638a81d.png)

### Installation
You need get access to [Emotiv Cortex API](https://emotiv.gitbook.io/cortex-api/)
```
cd p300 && pipenv install  
cp .env.sample .env

# put Cortex tokens in .env
vim .env

python main.py
```

### Controls
* Start training: `t`
* Start prediction: `p`
* Stop : `s`


Я провел небольшое исследование.
Я поймал данные с usb dongle через wireshark и параллельно записывал данные с emotiv pro.
Затем все прогнал в графики и вот что получилось. (1.png - emotiv.pro, 2.png - wireshark).
Данные пользостью совпали!

Когда я парсил данные с wireshark, я видел некоторые пакеты, по 80 и 246792 байта (70 - дефолтный входищий пакет)
Также я наткнулся на данные по 32 байта, где странные на вид данные(каждый десятый пакет)
Вот они(предпологаю, что это данные гироскопа):
14 32 213 4 7 240 252 247 252 24 223 224 2 28 0 240 254 80 1 236 0 0 0 0 0 0 0 0 0 0 0 0 12
15 32 213 4 7 240 252 248 252 128 223 168 2 0 0 236 254 67 1 246 0 0 0 0 0 0 0 0 0 0 0 0 22
16 32 213 3 7 239 252 247 252 72 223 164 2 152 0 243 254 80 1 241 0 0 0 0 0 0 0 0 0 0 0 0 32
17 32 213 3 7 239 252 247 252 16 223 144 2 104 0 244 254 86 1 240 0 0 0 0 0 0 0 0 0 0 0 0 42
18 32 213 4 7 240 252 246 252 148 223 148 2 132 0 237 254 83 1 247 0 0 0 0 0 0 0 0 0 0 0 0 52