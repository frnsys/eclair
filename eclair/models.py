import talon

# Initialize talon's classifiers
talon.init()

from flanker import mime
from flanker.addresslib import address
from talon import signature, quotations
from talon.signature.bruteforce import extract_signature
from dateutil.parser import parse


class Email():
    def __init__(self, email_string):
        """
        Takes a raw email string and processes it into something useful
        """
        self.str = email_string
        self.raw = mime.from_string(self.str)

        to = self.raw.headers['To']
        if to is None:
            self.recipients = []
        else:
            to = to.lower()
            self.recipients = address.parse_list(to) if ',' in to else [address.parse(to)]

        # It's possible a recipient is None if it is something like
        # 'Undisclosed recipients:;'
        self.recipients = [r for r in self.recipients if r is not None]
        self.sender = address.parse(self.raw.headers['From'].lower())

        self.subject = self.raw.subject
        self.id = self.raw.message_id
        self.date = parse(self.raw.headers['Date'])
        self.content_encoding = self.raw.content_encoding[0]

        # Extract plaintext body
        if self.raw.content_type.is_singlepart():
            self.full_body = self.raw.body
        elif self.raw.content_type.is_multipart():
            for p in self.raw.parts:
                if p.content_type == 'text/plain':
                    self.full_body = p.body
                    break

        # Try to get signature
        self.body, self.signature = extract_signature(self.full_body)

        # Try ML approach if necessary
        if self.signature is None:
            self.body, self.signature = signature.extract(self.full_body, sender=self.sender)

        # Get replies only, not the quotes
        self.body = quotations.extract_from(self.body, 'text/plain')

    def to_json(self):
        return {
            'recipients': [r.address for r in self.recipients],
            'sender': self.sender.address,
            'subject': self.subject,
            'date': self.date,
            'body': self.body,
            'signature': self.signature
        }
