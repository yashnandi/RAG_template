from __future__ import annotations

import sys

from genie.rag.qa import RAGQA


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m genie.cli.ask \"<your question>\"")
        raise SystemExit(1)

    question = " ".join(sys.argv[1:])
    qa = RAGQA()
    ans = qa.answer(question, top_k=3)
    print("\n" + ans + "\n")


if __name__ == "__main__":
    main()
