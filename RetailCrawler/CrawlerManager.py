class CrawlerManager:
    search_request_string = ''
    item_requested = ''

    def __init__(self, test):
        self.search_request_string = test

    def gimmethatstringback(self):
        return self.search_request_string

    def gimmetheactualitem(self):
        # Extract the first item in the Request Dictionary Object
        self.item_requested = self.search_request_string['Records'][0]['dynamodb']["NewImage"]["item"]["S"]

        return self.item_requested
