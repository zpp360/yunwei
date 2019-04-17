# coding = utf-8
class region:

    def __init__(self):
        self.code = ''
        self.name = ''
        self.url = ''
        self.parent_name = ''
        self.parent_code = ''

    def __str__(self):
        return self.code + ":" +self.name + ":" +self.url + ":" + self.parent_code + ":" + self.parent_name



