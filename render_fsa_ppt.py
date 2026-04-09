#!/usr/bin/env python3
"""
One-click renderer for the FSA paper slide plans.

This script wraps `generate_ppt.py` so users can easily render either
report or teaching edition PPT images with a single command.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLAN_REPORT = ROOT / "slides_plan_prestack_fsa.json"
PLAN_TEACHING = ROOT / "slides_plan_prestack_fsa_teaching.json"
DEFAULT_STYLE = ROOT / "styles" / "gradient-glass.md"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render FSA PPT images (report/teaching) via generate_ppt.py"
    )
    parser.add_argument(
        "--edition",
        choices=["report", "teaching"],
        default="teaching",
        help="Choose slide plan edition (default: teaching)",
    )
    parser.add_argument(
        "--style",
        default=str(DEFAULT_STYLE),
        help="Path to style file (default: styles/gradient-glass.md)",
    )
    parser.add_argument(
        "--resolution",
        choices=["2K", "4K"],
        default="2K",
        help="Output resolution (default: 2K)",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Output folder (default: auto by generate_ppt.py)",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Optional Gemini API key. If omitted, use GEMINI_API_KEY env var.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    plan = PLAN_TEACHING if args.edition == "teaching" else PLAN_REPORT
    if not plan.exists():
        print(f"Error: plan file not found: {plan}")
        sys.exit(1)

    env = os.environ.copy()
    api_key = args.api_key or env.get("GEMINI_API_KEY", "")
    if not api_key:
        print("Error: GEMINI_API_KEY is required.")
        print("Use --api-key 'YOUR_KEY' or export GEMINI_API_KEY first.")
        sys.exit(1)
    env["GEMINI_API_KEY"] = api_key

    cmd = [
        sys.executable,
        str(ROOT / "generate_ppt.py"),
        "--plan",
        str(plan),
        "--style",
        args.style,
        "--resolution",
        args.resolution,
    ]
    if args.output:
        cmd.extend(["--output", args.output])

    print("Running command:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True, env=env)


if __name__ == "__main__":
    main()
