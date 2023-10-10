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
