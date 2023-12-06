class VideoGame:
    used_ids = set()

    headings = ['ID', 'Name', 'Company', 'Platform', 'Year', 'Price']
    fields = {
        '-ID-': 'Game ID:',
        '-Name-': 'Game Name:',
        '-Company-': 'Game Company:',
        '-Platform-': 'Game Platform:',
        '-Year-': 'Year:',
        '-Price-': 'Price'
    }

    def __init__(self, ID, name, company, platform, year, price):
        if ID in VideoGame.used_ids:
            raise ValueError("Duplicate ID detected. Please choose a unique ID.")
        self.ID = ID
        VideoGame.used_ids.add(ID)
        self.name = name
        self.company = company
        self.platform = platform
        self.year = year
        self.price = price
        self.erased = False

    def __eq__(self, other):
        return other.ID == self.ID

    def __str__(self):
        return f"{self.fields['-ID-']} {self.ID}, {self.fields['-Name-']} {self.name}, {self.fields['-Company-']} {self.company}, {self.fields['-Platform-']} {self.platform}, {self.fields['-Year-']} {self.year}, {self.fields['-Price-']} {self.price}, Erased: {self.erased}"

    def gameInPlatform(self, platform):
        return str(self.platform) == str(platform)

    def setGameInfo(self, name, company, platform, year, price):
        self.name = name
        self.company = company
        self.platform = platform
        self.year = year
        self.price = price

    def markAsErased(self):
        self.erased = True
        VideoGame.used_ids.remove(self.ID)

    def isSameID(self, other_id):
        return self.ID == other_id
