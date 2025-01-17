"""
This file simply tests that bactax correctly identifies
whether a handful of bacteria are gram negative or positive.

The tests are:

- genus: Akkermansia --> gram negative
- species: Clostridioides difficile --> gram positive
- genus: fusobacterium --> gram negative
- species: morganella morganii --> gram negative
- genus: enterococcus --> gram positive
- genus: ruminococcus --> gram positive
- genus: clostridium --> gram positive
"""

import bactax


class BactaxGramTest:

    def __init__(self, input: dict[str, str], expected_output: str):
        self.input = input
        self.expected_output = expected_output

    def run(self):
        output = bactax.gram_stain(**self.input)
        if not output == self.expected_output:
            print(
                f"Test failed for {self.input}: output was {output} but expected {self.expected_output}"
            )
            return False
        return True


tests = [
    BactaxGramTest({"genus": "Akkermansia"}, bactax.Gram.NEGATIVE),
    BactaxGramTest({"species": "Clostridioides difficile"}, bactax.Gram.POSITIVE),
    BactaxGramTest({"genus": "fusobacterium"}, bactax.Gram.NEGATIVE),
    BactaxGramTest({"species": "morganella morganii"}, bactax.Gram.NEGATIVE),
    BactaxGramTest({"genus": "enterococcus"}, bactax.Gram.POSITIVE),
    BactaxGramTest({"genus": "ruminococcus"}, bactax.Gram.POSITIVE),
    BactaxGramTest({"genus": "clostridium"}, bactax.Gram.POSITIVE),
]

num_succeeded = 0
for test in tests:
    num_succeeded += int(test.run())

print(f"{num_succeeded}/{len(tests)} tests succeeded")
