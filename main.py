import os

from p300.speller import Speller
from dotenv import load_dotenv


def main():
    load_dotenv()

    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    license = os.environ['LICENSE']

    app = Speller(client_id, client_secret, license)
    app.start()


if __name__ == "__main__":
    main()
