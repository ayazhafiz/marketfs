import argparse
import dotenv
import fuse

import marketfs

parser = argparse.ArgumentParser(
    prog="marketfs",
    description="A filesystem for the stock market.",
)
parser.add_argument("mountpoint", help="Where to mount marketfs.")
parser.add_argument("--foreground", default=True, action=argparse.BooleanOptionalAction)
parser.add_argument("--debug", default=False, action=argparse.BooleanOptionalAction)

args = parser.parse_args()

dotenv.load_dotenv()

fs = marketfs.MarketFs()
fuse.FUSE(
    fs,
    args.mountpoint,
    foreground=args.foreground,
    debug=args.foreground,
)
