from p300.audio.audio import Audio
from p300.speller.speller import Speller
from p300.speller_random.speller import SpellerRandom
from dotenv import load_dotenv


def main():

    #app = Audio()
    app = Speller()
    app.start()

if __name__ == "__main__":
    main()
