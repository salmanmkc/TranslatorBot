import discord
import json
import TranslatorApi
import supported_languages
import os

bot_token = os.environ["bot_token"]

client = discord.Client()

requesting_user = ""

def get_help_message(language):                   
    #help_message_en is being used as a placeholder. they should be pulled from json and set to help_message_LANGUAGE.CODE.
    if language == "English":
        #these should be pulled in from json or similar files. json is already a dependency so best to stick with it.
        help_message = "All commands can be used by mentioning this bot." \
                   "To view this message you can mention this bot with the message '-h English' or 'help English'" \
                   "To translate a previously sent message, simply react to it with a flag emoji. " \
                   "Below is a list of supported languages and their flags: \n"\
                   ":flag_us: English | US\n"\
                   ":flag_in: Hindi | IN\n"\
                   ":flag_es: Spanish | ES\n"\
                   ":flag_de: German | DE\n"\
                   ":flag_mf: French | MF\n"\
                   ":flag_pt: Portuguese | PT\n"\
                   ":flag_ru: Russian | RU\n"\
                   ":flag_jp: Japanese | JP\n"\
                   "More languages will be supported in future releases."
        return help_message
    elif language == "Hindi" or lanuage == "हिन्दी":
        help_message = "Support for this language has not been implemented yet." #import message from json
        return help_message
    elif language == "Spanish" or lanuage == "Español":
        help_message = "Support for this language has not been implemented yet." #import message from json
        return help_message
    elif language == "German" or lanuage == "Deutsche":
        help_message = "Support for this language has not been implemented yet." #import message from json
        return help_message
    elif language == "French" or lanuage == "français":
        help_message = "Support for this language has not been implemented yet." #import message from json
        return help_message
    elif language == "Portuguese" or lanuage == "Português":
        help_message = "Support for this language has not been implemented yet." #import message from json
        return help_message
    elif language == "Russian" or lanuage == "русский":
        help_message = "Support for this language has not been implemented yet." #import message from json
        return help_message
    elif language == "Japanese" or lanuage == "日本語":
        help_message = "Support for this language has not been implemented yet." #import message from json
        return help_message
        

def get_country(flag):
    with open("required_data.json", "r") as datafile:
        jsondata = json.loads(datafile.read())

    for every in jsondata:
        if every["flag"] == flag:
            return every


@client.event
async def on_reaction_add(reaction, user):
    print("You added a reaction"+reaction.emoji)

    received_emoji = reaction.emoji
    country_name = get_country(received_emoji)
    print(country_name)
    if country_name is not None:
        languages = supported_languages.SupportedLanguages
        if country_name["name"]["common"] == "France":
            language = languages.French
        elif country_name["name"]["common"] == "Germany":
            language = languages.German
        elif country_name["name"]["common"] == "India":
            language = languages.Hindi
        elif country_name["name"]["common"] == "United States":
            language = languages.English
        elif country_name["name"]["common"] == "Spain":
            language = languages.Spanish
        elif country_name["name"]["common"] == "Russia":
            language = languages.Russian
        elif country_name["name"]["common"] == "Portugal":
            language = languages.Portuguese
        elif country_name["name"]["common"] == "Japan":
            language = languages.Japanese
        else:
            language = None

        if language is not None:
            api = TranslatorApi.TranslatorApi()
            text = [{"text": reaction.message.content}]
            translation = api.translate(text, language)
            response = translation.text
            response = json.loads(response)
            if response[0]["detectedLanguage"] is not None:
                if response[0]["translations"] is not None:
                    translated_text = response[0]["translations"][0]["text"]
                    if user.dm_channel is None:
                        await user.create_dm()
                    await user.dm_channel.send(translated_text)
                    # await reaction.message.channel.send(translated_text)
                else:
                    print(response)
                    await reaction.message.channel.send("Translation Failed")
            else:
                print(response)
                await reaction.message.channel.send("We were not able to detect input language")

        else:
            await reaction.message.channel.send("Languages of {} are currently not supported".format(country_name["name"]["common"]))
    else:
        print("Normal emoji found exiting")
    return

@client.event
async def on_message(message):
    content = message.content
    list_content = str(content).split()
    if list_content[1] == "help" or list_content[1] == "-h":
        if len(list_content) == 3:
            mentions = message.raw_mentions
            if mentions is not None:
                for mention in mentions:
                    if mention == client.user.id:
                        if message.author.dm_channel is None:
                            await message.author.create_dm()
                        await message.author.dm_channel.send(get_help_message(list_content[3]))
    return


client.run(bot_token)
