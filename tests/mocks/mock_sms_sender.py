class MockSmsSender:
    def __init__(self):
        self.sent_sms = []

    def send(self, phone_number: str):
        self.sent_sms.append(phone_number)
