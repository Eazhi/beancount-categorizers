import logging
import re

from beancount.core import data

from beancount_categorizers.hooks import ImporterHook


class FlagTxn(ImporterHook):
    def __init__(self, payees: list):
        self.payees = payees

    def __call__(self, importer, file, imported_entries, existing_entries):
        return [self._process(entry) or entry for entry in imported_entries]

    def _process(self, entry):
        if not isinstance(entry, data.Transaction) or len(entry.postings) != 1:
            logging.info(f"Did not flag entry {entry}")
            return entry

        for payee in self.payees:
            if re.match(payee, (entry.payee or entry.narration)):
                return data.Transaction(
                    entry.meta,
                    entry.date,
                    "!",
                    entry.payee,
                    entry.narration,
                    entry.tags,
                    entry.links,
                    entry.postings,
                )

        return entry
