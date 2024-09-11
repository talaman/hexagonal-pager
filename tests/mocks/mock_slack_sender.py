class MockSlackSender:
    def __init__(self):
        self.sent_slack = []

    def send(self, channel: str):
        self.sent_slack.append(channel)
