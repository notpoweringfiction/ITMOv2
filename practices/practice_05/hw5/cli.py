#!/usr/bin/env python3
import argparse
import os
import sys

from service_ext import (
    load_state,
    save_state,
    add_subscriber,
    list_subscribers,
    export_subscribers,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="hw5-cli", description="Manage subscribers")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_sub = sub.add_parser("subscribe", help="Add subscriber")
    p_sub.add_argument("name", help="Subscriber name")

    p_list = sub.add_parser("list", help="List subscribers")
    p_list.add_argument("--prefix", default="", help="Case-insensitive prefix filter")

    p_exp = sub.add_parser("export", help="Export visible list to file")
    p_exp.add_argument("--prefix", default="", help="Case-insensitive prefix filter")
    p_exp.add_argument("--out", required=True, help="Output file path")

    args = parser.parse_args(argv)

    try:
        load_state()
        if args.cmd == "subscribe":
            res = add_subscriber(args.name)
            save_state()
            print(f"subscribed: {str(res.get('subscribed', False)).lower()}")
        elif args.cmd == "list":
            items = list_subscribers(args.prefix)
            for x in items:
                print(x)
        elif args.cmd == "export":
            export_subscribers(args.prefix, args.out)
            print(f"exported: {args.out}")
        else:
            parser.print_help()
            return 2
        return 0
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
