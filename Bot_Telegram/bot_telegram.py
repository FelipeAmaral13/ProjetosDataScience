#####################################################
#                                                   #
#                   Passo a passo                   #
#                                                   #
#####################################################

# 1. Criar o Bot no BotFather
# 2. Obter o Token criado 
# 3. Criar um grupo
# 4. Add o Bot no grupo
# 5. Tornar o Bot admin do grupo
# 6. Acessar o link: https://api.telegram.org/bot<TOKEN_BOT>/getUpdates e obter o chat_id (é um numero que começa com "-") do grupo que o Bot esta inserido. 


import requests

# Robo Telegram
class Bot():

    def __init__(self, token, chat_id=None):
        self.token = token 
        self.chat_id = chat_id  
        self.url = "https://api.telegram.org/bot{}".format(token)
        
    def send_message(self, msg, 
                     disable_web_page_preview=False, 
                     disable_notification=False, 
                     parse_mode=['HTML', 'Markdown']):
        try:
            assert self.chat_id is not None, "ERRO: chat_id is None, please set a chat_id"
            data = {"chat_id": self.chat_id, "text": msg, 'disable_web_page_preview': disable_web_page_preview,
                    'disable_notification': disable_notification, 'parse_mode': parse_mode[0]}
            url = self.url + '/sendMessage'
            response = requests.post(url, data)
            return response
        except Exception as e:
            print('ERRO send_message: request Não Enviada: {}'.format(url))
            print(e)
            raise e
    
    def setChatId(self, chat_id):
        self.chat_id = chat_id


#token = '1733127358:AAGFj2Yk3_1Pd6de_JW7FWLA7KYVf82RHLU'
#chat_id = -472930056

#masterclassdsbot = Bot(token=token)
#masterclassdsbot.setChatId(chat_id)
#masterclassdsbot.send_message(msg='Olá mundo')


