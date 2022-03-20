import urllib, hashlib

def avatar(usermail):

    #hashing the url
    hash = hashlib.md5(usermail.encode('utf-8')).hexdigest()

    #output image
    gravatar_image = "https://www.gravatar.com/avatar/" + hash + "?"

    return gravatar_image