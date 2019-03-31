from InstagramAPI import InstagramAPI
import Config

IG = InstagramAPI(Config.IG_Username, Config.IG_Password)
IG.login()

# Upload Method :: Uploads the meme with the caption to Instagram
def Upload (_Caption):
    IG.uploadPhoto ('Data/meme.jpg', caption = _Caption)
    print ('Uploaded the meme, with the caption: ' + _Caption)
