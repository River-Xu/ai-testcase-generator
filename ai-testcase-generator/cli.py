from __future__ import annotations
import argparse
from pathlib import Path

from aitestgen import generate_testcases, export_testcases

def main():
    parser = argparse.ArgumentParser(description="AI Testcase Generator")
    parser.add_argument("--input", type=str, help="Path to requirement text/markdown file")
    parser.add_argument("--text", type=str, help="Requirement text (inline)")
    parser.add_argument("--out", type=str, required=True, help="Output file path (.json/.csv/.xlsx)")
    args = parser.parse_args()

    if not args.input and not args.text:
        raise SystemExit("Provide --input or --text")

    if args.input:
        requirement = Path(args.input).read_text(encoding="utf-8")
    else:
        requirement = args.text or ""

    suite = generate_testcases(requirement)
    out = export_testcases(suite, args.out)
    print(f"Saved: {out}")

if __name__ == "__main__":
    main()
