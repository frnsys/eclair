from glob import glob
from eclair.models import Email
from eclair.heuristics import guess_signatures
from flanker.mime.message.errors import DecodingError

files = glob('data/rubio_emails/*.eml')

emails = []
for file in files:
    with open(file, 'r') as f:
        data = f.read()

    try:
        e = Email(data)
        emails.append(e)

    # Malformed email
    except DecodingError:
        continue

guess_signatures(emails)



print('done')


