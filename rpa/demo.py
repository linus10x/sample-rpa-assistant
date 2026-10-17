"""File one synthetic intake. The assistant clears the notice, then types and submits."""

from rpa.app import Desk
from rpa.assistant import run


def main() -> int:
    result = run(
        Desk(),
        "file_intake",
        {"applicant": "Sample Person", "case_id": "C-1001"},
    )
    print("submitted", result["submitted"])
    print("log", " ".join(result["log"]))
    return 0 if result["submitted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
