import praw
import random
import urllib.request
from PIL import Image
import time

import Config
import SendMeme

# Setup Method :: Returns all the data needed
def Setup ():
    Reddit = praw.Reddit (client_id = Config.ID, client_secret = Config.Secret, password = Config.Password, user_agent = Config.Agent, username = Config.Username)
    Memes = Reddit.subreddit ('DarkMemes')

    with open ('Data/lastmeme.txt', 'r') as file:
        LastID = str (file.readlines ()[0].replace ('\n', ''))

    with open ('Data/captions.txt', 'r', encoding = 'utf-8') as file:
        Captions = file.readlines ()

    with open ('Data/lastcaptions.txt', 'r', encoding = 'utf-8') as file:
        LastCaptions = file.readlines ()

    return Memes, LastID, Captions, LastCaptions

# GetImage Method :: Does all the processing
def GetImage (_Memes, _ID, _Captions, _LCaps):
    Memes = []

    if _ID is not None:
        for meme in _Memes.new (limit = 15):
            if not str (meme.id) == str (_ID):
                Memes.append (meme)
            else:
                break

    if Memes == []:
        print ('No new meme..')
        return

    Meme = CheckMeme (Memes[len (Memes) - 1])

    if Meme is None:
        print ('Meme image is not valid!')
        return

    try:
        urllib.request.urlretrieve (Meme.url, 'Data/meme.jpg')
    except:
        print ('This meme must be a video..')
        return

    Img = Image.open ('Data/meme.jpg').convert ('RGB')
    Img.resize (Config.Size, Image.ANTIALIAS)
    Img.save ('Data/meme.jpg')

    Caption = GetCaption (_Captions, _LCaps)

    with open ('Data/lastmeme.txt', 'w') as file:
        file.write (str (Meme.id))

    SendMeme.Upload (Caption)
    print (Meme.id)

# CheckMeme Method :: Checks if the URL is a valid reddit url
def CheckMeme (_Meme):
    if 'redd' in _Meme.url:
        return _Meme
    else:
        return None

# GetCaption Method :: Finds a caption for the post
def GetCaption (_Captions, _LastCaptions):
    for Caption in _Captions:
        if not Caption in _LastCaptions:
            with open ('Data/lastcaptions.txt', 'r', encoding = 'utf-8') as file:
                Lasts = file.readlines ()

            Lasts[0] = Lasts[1]
            Lasts[1] = str (Caption)

            with open ('Data/lastcaptions.txt', 'w', encoding = 'utf-8') as file:
                file.writelines (Lasts)

            return Caption

if __name__ == '__main__':
    while True:
        Data = Setup ()

        GetImage (Data[0], Data[1], Data[2], Data[3])

        print ('Started again..')

        time.sleep (Config.Interval)
