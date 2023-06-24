import telebot, os, requests
from datetime import datetime
from os import system

api_key = 'telegram api key here'
bot = telebot.TeleBot(api_key)


def extract_arg(arg):
  return arg.split()[1:]

# Create a list to store the user IDs
users = []

# Function to add a user ID to the list
def add_user(user_id):
    if user_id not in users:
        users.append(user_id)


'''API KEYS TO USE THE BOT'''


@bot.message_handler(commands=['keys'])
def keys(message):
  APIkeyss = (message.text).replace('/keys ', '')

  if len(APIkeyss) == 51:
    global APIkeys
    APIkeys = f'Bearer {APIkeyss}'
    bot.reply_to(
      message,
      'You can now use the bot. If you are having a problem you just need to message your apikeys again and enjoy the bot.'
    )
  else:
    print('try again')


@bot.message_handler(commands=['start'])
def start(message):
  user_id = message.chat.id
  # Add the user ID to the list when they start using the bot
  add_user(user_id)
  bot.reply_to(
    message, """Your message to the users""")


myList = []
while True:

  @bot.message_handler(commands=['help'])
  def help(message):
    bot.reply_to(
      message, """
Disclaimer:
This is just for educational purposes only.
The developer of this bot is not responsible for any unauthorized activity!

If you want to use this bot click /tutorial""")

  @bot.message_handler(commands=['tutorial'])
  def tutorial(message):
    bot.reply_to(
      message, """
Steps to use this bot.
Steps:
1. Create an account in OpenAI (If you have an account proceed to step 3)
2. Login to OpenAI
3. In the upper right of the website you will see the word *Personal* click that.
4. Click the *view API keys*
5. On the api keys click *create new secret keys*
6. Copy and save it for later.
7. Go to the bot
8. Type /keys *your apikeys here*
    example: /keys sk-njkfsancjksdalksdaldanjksda
9. Enjoy using the bot! DM me if you want to make a telegram or discord bot!
10. DM the developer @kyle_010 if you are in need of assistance
""")



  @bot.message_handler(func=lambda message: True)
  def chat(message):
    user_id = message.chat.id
    # Add the user ID to the list when they start using the bot
    add_user(user_id)
    try:
      messages = (message.text)
      ask = "".join(messages)
      print(ask)
      if ask == "":
        bot.reply_to(message, "ignore this error message and try again!")
      else:

        headers = {
          'Content-Type': 'application/json',
          'Authorization': f'{APIkeys}',
        }
        json_data = {
          'model': 'text-davinci-003',
          'prompt': ask,
          'max_tokens': 4000,
          'temperature': 0,
        }
        response = requests.post('https://api.openai.com/v1/completions',
                                 headers=headers,
                                 json=json_data)
        print(response.json())
        bot.reply_to(
          message, f"""{response.json()['choices'][0]['text']}
""")

        
        #check for errors
    except TypeError as e:
      bot.reply_to(message, "ignore this error message and try again!")
      print(e)
    except NameError as e:
      bot.reply_to(
        message,
        "You need to create an account in OpenAI and get the Api Keys to use this bot. Please click /help to know how to create an account."
      )
      

    except AttributeError as e:
      bot.reply_to(message,
                   "Press /help if you are having a problem using the bot.")
      print(e)

    except IndexError as w:
      bot.reply_to(message, "ignore this error message and try again!")
      print(w)

    except KeyError as e:
      bot.reply_to(
        message,
        "Your api key is exceeded the free trial or create another account")
      print(e)
    except TypeError as e:
      print(e)
    except NameError as e:
      print(e)

  if __name__ == "__main__":
    #keep_alive()
    bot.polling()
