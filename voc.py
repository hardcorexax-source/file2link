import telebot
import json

from deep_translator import GoogleTranslator

def transEn2Ru(word):
  return GoogleTranslator(source = 'en', target = 'ru').translate(word)

def transRu2En(word):
  return GoogleTranslator(source = 'ru', target = 'en').translate(word)



token="7823478766:AAF0lNvTSrJYY_bzCV6MZBN4janyxhLe9cE"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
  username = message.from_user.username or str(message.from_user.id)
  with open(f"{username}.json", "x") as file:
    file.write('{}')
  bot.send_message(message.chat.id, f"Словарь создан!")

@bot.message_handler(commands=['json'])
def my_words(message):
  username = message.from_user.username or str(message.from_user.id)
  bot.send_message(message.chat.id, f"Вот код JSON всех ваших слов")
  with open(f"{username}.json", "r", encoding="utf-8") as file:
    bot.send_message(message.chat.id, f"{file.read()}")



@bot.message_handler(commands=['my_words'])
def my_words(message):
  username = message.from_user.username or str(message.from_user.id)
  bot.send_message(message.chat.id, f"Полный список ваших слов")
  with open(f"{username}.json", "r", encoding="utf-8") as file:
    wordsListEn = ''
    wordsDict = json.loads(file.read())
    for i in wordsDict:
        allRu = ''
        if len(wordsDict[i]) == 1:
            allRu = wordsDict[i][0]
        else:
            for j in range(len(wordsDict[i])-1):
                allRu += wordsDict[i][j]+","
            allRu += wordsDict[i][-1]

        wordsListEn += i+" - "+allRu+'\n\n'


    bot.send_message(message.chat.id, f"{wordsListEn}")


@bot.message_handler(commands=['delete_list'])
def delete_vocabulary(message):
  username = message.from_user.username or str(message.from_user.id)
  bot.send_message(message.chat.id, f"Полный список ваших слов (Если забыли сохранить)")
  with open(f"{username}.json", "r", encoding="utf-8") as file:
    wordsListEn = ''
    wordsDict = json.loads(file.read())
    for i in wordsDict:
        wordsListEn += i+'\n'
    bot.send_message(message.chat.id, f"{wordsListEn}")
  with open(f"{username}.json", "w", encoding="utf-8") as file:
    file.write('{}')
  bot.send_message(message.chat.id, f"Список успешно удален!")


######################################################################

def messageToArr(message):
    message = message.lower()
    newWord = ''
    wordsArr = []
    for i in message:
      if (ord('а') <= ord(i) <= ord('я')) or (ord('a') <= ord(i) <= ord('z')):
        newWord += i
      elif (newWord != ''):
        wordsArr.append(newWord)
        newWord = ''

    if (newWord != ''):
      wordsArr.append(newWord)
      newWord = ''
    return wordsArr


@bot.message_handler()
def no_command_message(message):
  username = message.from_user.username or str(message.from_user.id)
  wordsArr = []
  fileJson = None
  with open(f"{username}.json", "r", encoding="utf-8") as file:
    fileJson = json.loads(file.read())
    wordsArr = messageToArr(message.text)
    for i in wordsArr:
        i.lower()
        if (ord('а') <= ord(i[0]) <= ord('я')):
            engKey = transRu2En(i).lower()
            if engKey not in fileJson:
                fileJson[engKey] = []
            fileJson[engKey].append(i)
        else:
            if i not in fileJson:
                fileJson[i] = []
            fileJson[i].append(transEn2Ru(i))




  with open(f"{username}.json", "w", encoding="utf-8") as file:
    json.dump(fileJson, file, indent = 4)

  length = len(wordsArr)
  secondPart = ''
  if (int(str(length)[-1]) == 1):
    if (len(str(length)) > 1):
      if (int(str(length)[-2]) != 1):
        secondPart = "новое слово"
    else:
      secondPart = "новое слово"
  elif (2 <= int(str(length)[-1]) <= 4):
    if (len(str(length)) > 1):
      if (int(str(length)[-2]) != 1):
        secondPart = "новых слова"
      else:
        secondPart = "новых слов"
    else:
      secondPart = "новых слова"
  else:
    secondPart = "новых слов"

  bot.send_message(message.chat.id, f"Добавлено {len(wordsArr)} {secondPart}")


bot.infinity_polling(none_stop=True)