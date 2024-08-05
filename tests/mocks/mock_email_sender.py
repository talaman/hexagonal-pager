class MockEmailSender:
    def __init__(self):
        self.sent_emails = []

    def send(self, address: str):
        self.sent_emails.append(address)
