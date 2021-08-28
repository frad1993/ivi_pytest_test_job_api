import string, random


ivi_user = 'hfweioweo'

def get_random_str(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_random_int():
    return random.randrange(100, 200, 3)

