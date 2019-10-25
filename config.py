DEBUG = True

DATABASE = './db/thesis.db'

SECRET_KEY = b'W\xeb\xa7\xc4\x91\xb3\x89\x1e\xb3\xbe'

REGISTRATION_KEY = 'secret'

EMAIL_FORMAT = '^z[0-9]{7}@unsw.edu.au$'
EMAIL_FORMAT_ERROR = \
    'Expected z5555555@unsw.edu.au<br>where z5555555 is your zID.'

TOPIC_REQUEST_TEXT = 'Dear HEADER\n\n' + \
    'I am a student about to start final year Thesis next semester.\n' + \
    'I would like to express my interest in conducting my thesis ' + \
    'project with you. I have a research interest in ...\n\n' + \
    'The list below outlines the courses I have completed ' + \
    'and experience/skills:\n\nI would like to book a time ' + \
    'for a face-to-face discussion about the project that you ' + \
    'may offer. I am available at the following time...\n\n' + \
    'Kind Regards\nFOOTER'
