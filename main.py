import os

from p300.music.music import Music
from p300.speller.speller import Speller
from p300.visual.visual import Visual
from dotenv import load_dotenv


def main():
    load_dotenv()

    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    license = os.environ['LICENSE']

    # app = Music(client_id, client_secret, license)
    app = Speller(client_id, client_secret, license)
    #app = Visual(client_id, client_secret, license)
    app.start()

if __name__ == "__main__":
    main()
