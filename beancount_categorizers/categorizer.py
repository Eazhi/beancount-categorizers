import re
from beancount.core import data
from smart_importer.hooks import ImporterHook

import logging

class PayeeCategorizer(ImporterHook):
    def __init__(self, categories):
        self.account_to_payees = categories
        self.payee_to_account = {}
        self.regexes = {}

        for account, payees in self.account_to_payees.items():
            for payee in payees:
                if payee in self.payee_to_account:
                    logging.warning(f"{payee} in multiple accounts")
                    self.payee_to_account[payee] = None
                else:
                    self.payee_to_account[payee] = account

        for payee, account in self.payee_to_account.items():
            if not account:
                continue  # Account conflict
            self.regexes[payee] = re.compile(payee, flags=re.IGNORECASE)

    def __call__(self, importer, file, imported_entries, existing_entries):
        return [
            self._process(entry) or entry for entry in imported_entries
        ]

    def _process(self, entry):
        if type(entry) != data.Transaction or len(entry.postings) != 1 or entry.flag != "*":
            return

        match = set()
        payee_matches = set()
        for payee, prog in self.regexes.items():
            if prog.match(entry.payee) or prog.match(entry.narration):
                match.add(self.payee_to_account[payee])
                payee_matches.add(payee)

        if len(match) == 1:
            entry.postings.append(data.Posting(
                list(match)[0],
                None,
                None,
                None,
                None,
                None,
            ))
        elif len(match) > 1:
            logging.warning(f"{len(match)} matches: {match} for {entry}")

        return entry
