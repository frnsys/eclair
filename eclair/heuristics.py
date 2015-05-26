from __future__ import unicode_literals

import re
from itertools import product
from collections import Counter, defaultdict
from nytnlp.tokenize.keyword import keyword_tokenizes
from nytnlp.markup import markup_terms


def guess_signatures(emails):
    """
    This is a heuristic to pick up where `talon` fails at
    detecting signatures: look for end-of-email strings which
    repeat significantly for a given sender.
    """

    # Group emails by senders
    emails_by_sender = defaultdict(list)

    for em in emails:
        emails_by_sender[em.sender].append(em)

    for sender, ems in emails_by_sender.items():
        # For every pair of emails,
        # compute end-of-string overlap
        pairs = product(ems, ems)
        overlaps = []
        for e1, e2 in pairs:
            if e1 == e2:
                continue
            overlap = []
            i = -1
            e1b = e1.body.strip()
            e2b = e2.body.strip()
            le1b = len(e1b)
            le2b = len(e2b)
            while True:
                if abs(i) > le1b or \
                    abs(i) > le2b or \
                    e1b[i] != e2b[i]:
                    break
                overlap.append(e1b[i])
                i -= 1
            overlap = ''.join(reversed(overlap)).strip()

            # > 1 so we don't capture punctuation
            if overlap and len(overlap) > 1:
                overlaps.append(overlap)

        if not overlaps:
            continue

        # See if the top sig qualifies
        c = Counter(overlaps)
        sig, count = c.most_common(1)[0]

        if count/len(ems) > 0.8:
            # Set the sig and remove it from the cleaned body
            r = re.compile('{}\s*$'.format(re.escape(sig)))
            for em in ems:
                em.signature = sig if em.signature is None else '\n'.join([sig, em.signature])
                em.body = r.sub('', em.body).strip()


def guess_keywords(emails):
    docs = [e.body for e in emails]
    t_docs = keyword_tokenizes(docs)
    for i, t_doc in enumerate(t_docs):
        emails[i].keywords = t_doc

    for i, highlighted in enumerate(markup_terms(docs, t_docs)):
        emails[i].highlighted_body = highlighted
