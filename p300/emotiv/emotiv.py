from p300.emotiv.cortex import Cortex


class Emotiv:
    def __init__(self, app_client_id, app_client_secret, license="", debug_mode=True):
        self.streams = ['eeg']
        self.c = Cortex(app_client_id, app_client_secret, license, debug_mode)
        self.c.bind(new_eeg_data=self.on_new_eeg_data)
        self.c.bind(inform_error=self.on_inform_error)

        self.data = []

    def open(self):
        self.c.open()

    def start(self):
        self.data = []
        self.c.sub_request(self.streams)

    def stop(self):
        self.c.unsub_request(self.streams)

    def get_data(self):
        return self.data

    # callbacks functions
    def on_new_eeg_data(self, *args, **kwargs):
        data = kwargs.get('data')
        self.data.append(data)

    def on_inform_error(self, *args, **kwargs):
        error_data = kwargs.get('error_data')
        print(error_data)
