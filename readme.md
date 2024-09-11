# ProxyTelegram
ProxyTelegram is a Telegram bot that resends all received messages to a supergroup and vice versa.
It allows you to communicate with users through the bot like through a proxy

# Install
git clone https://github.com/osf4/proxytelegram

# Usage
1. Create ```config.yaml``` file
2. Put that lines into the file:
   
```yaml
# MongoDB settings
database:
  host: 'localhost'
  port: 27017
  name: 'test'

# Telegram bot settings
bot:
  token: 'token from @BotFather'
  username: 'bot username'
  supergroup_id: 'supergroup id'
  greeting_message: 'Hi!' # Not required
```

3. run ```python3 main.py```
