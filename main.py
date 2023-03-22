import vk_api
import sqlite3
from time import sleep, asctime

class VkSearch:

    def __init__(self, *user_ids):
        self.user_ids = user_ids
        self.auth()
        self.get_data()
        self.show()

    def auth(self):
        vk_session = vk_api.VkApi('+79208920891', 'A448844a!_#E')
        vk_session.auth()
        self.vk = vk_session.get_api()

    def get_data(self):
        self.res = self.vk.users.get(user_ids=self.user_ids, fields='last_seen, online, timezone, has_mobile, city' )

    def show(self):
        for item in self.res:
            self.name = item['first_name']
            self.online = item['online']
            self.device = item['last_seen']['platform']
            self.last_seen = item['last_seen']['time']
            Table(self.name, self.online, self.device, self.last_seen)
            print(f'{self.name}\n\nВ сети ===> {self.online}\nУстройство ===> {self.device}\nКрайнее появление в сети ===> {self.last_seen}')

class Table:
    def __init__(self, name, online, device, last_seen):
        self.conn = sqlite3.connect('vksearch.db')
        self.c = self.conn.cursor()
        self.time = asctime()
        self.name = name
        self.online = online
        self.device = device
        self.last_seen = last_seen
        self.make_table()
        self.put_data()
        self.conn.commit()
        self.conn.close()

    def make_table(self):
        self.c.execute(f'CREATE TABLE IF NOT EXISTS {self.name} ("time", "online", "device", "last_seen")')

    def put_data(self):
        self.c.execute(f"INSERT INTO {self.name} VALUES (?, ?, ?, ?)", (self.time, self.online, self.device, self.last_seen))

def main():
    while True:
        sleep(10)
        users = ['1046428', '18658655', '25954547']
        print(', '.join(users))
        VkSearch(', '.join(users))

    

if __name__ == '__main__':
    main()
