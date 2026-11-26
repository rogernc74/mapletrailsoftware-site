"""Generate the Acadie+ browser configuration for the static-site build."""

from argparse import ArgumentParser
import json
import os
from pathlib import Path
import re


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Path to the generated JavaScript module.")
    args = parser.parse_args()

    key = os.environ.get("ACADIE_FIREBASE_WEB_API_KEY", "")
    if not re.fullmatch(r"AIza[A-Za-z0-9_-]{35}", key):
        raise SystemExit("Set ACADIE_FIREBASE_WEB_API_KEY to the Acadie Firebase browser key.")

    scripts = Path(__file__).resolve().parent
    config = json.loads((scripts / "acadie-billing-config.json").read_text(encoding="utf-8"))
    config["firebase"]["apiKey"] = key
    config["giftEnabled"] = os.environ.get("ACADIE_GIFT_WEBSITE_ENABLED") == "true"
    module = f"export const billingConfig = Object.freeze({json.dumps(config, indent=2)});\n"
    args.output.write_text(module, encoding="utf-8")


if __name__ == "__main__":
    main()
