# Beancount Categorizers

`beancount-categorizers` aims to provide simple categorizers to simplify your
transactions import pipeline.

## Installation

```sh
$ pip install beancount-categorizers
```

## Usage

```python
from beancount_bank import BankImporter  # Change with your bank's custom importer
from beancount_categorizers import PayeeCategorizer, FlagTxn

from smart_importer import apply_hooks

flagger = FlagTxn([])

categorizer = PayeeCategorizer({
    "Income:Employer": ["Employer"],
    "Expenses:Food:Groceries": ["Grocery stores.*", "Another grocery store"],
})

CONFIG = [
    apply_hooks(
        BankImporter("Assets:Bank:Checking"),
        [flagger, categorizer],
    )
]
```

## Categorizers

### Regex categorizer

The config takes a simple dict["account name", list["payee"]]
Where:
- account names are the accounts where transaction should be categorized
- "payee" are regex patterns that should match either the payee or the transaction's narration

### Flag Transaction

Given a list of payee, "flags" transaction with the "!" flag to automatically mark them as to be checked.