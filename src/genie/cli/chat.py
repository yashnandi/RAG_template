from __future__ import annotations

from genie.rag.qa import RAGQA


def main() -> None:
    qa = RAGQA()
    print("Genie Chat — type 'exit' to quit.\n")

    while True:
        q = input("You: ").strip()
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            break

        try:
            ans = qa.answer(q, top_k=3)
        except Exception as e:
            print(f"\n[error] {e}\n")
            continue

        print(f"\nGenie: {ans}\n")


if __name__ == "__main__":
    main()
