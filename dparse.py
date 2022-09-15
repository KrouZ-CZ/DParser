import requests
from PyQt5 import QtCore

class DParse(QtCore.QObject):
    mysignal = QtCore.pyqtSignal(dict)

    def __init__(self, token: str, chat_id: str, tab: int, parent=None) -> None:
        QtCore.QThread.__init__(self, parent)
        self.token = token
        self.chat_id = chat_id
        self.tab = tab

    def get_msg(self):
        url = f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=50'
        headers = {
            'authorization': self.token,
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9006 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"
            }
        alls = {'icons': {}, 'messages': []}

        for _ in range(self.tab):
            req = requests.get(url=url, headers=headers).json()
            if (type(req) == dict) and ((req.get('message') == 'Unknown Channel') or (req.get('message') == '401: Unauthorized')): 
                self.mysignal.emit({'icons': {}, 'messages': []})
                return 
            if len(req) == 0: break
            before = req[len(req) - 1]['id']
            for item in req:
                if item['type'] != 0: continue
                if not item['author']['avatar'] in alls['icons']:
                    alls['icons'][item['author']['avatar']] = requests.get(f"https://cdn.discordapp.com/avatars/{item['author']['id']}/{item['author']['avatar']}.webp?size=128")._content
                alls['messages'].insert(0, {'username': item['author']['username'], 'text': item['content'], 'timestamp': item['timestamp'], 'icon': item['author']['avatar']})
            url = f'https://discord.com/api/v9/channels/{self.chat_id}/messages?before={before}&limit=50'
        self.mysignal.emit(alls)