import argparse
from sys import exit, stderr
from reg import app

def parse_args():
    parsing = argparse.ArgumentParser(
        description="Tiger Clubs")

    parsing.add_argument(
        "port", type=int,
        help="the port at which the server should listen")

    parsed = parsing.parse_args()

    port = parsed.port
    return port


def main():

    port = parse_args()

    try:
        app.run(host="0.0.0.0", port=port, debug=True)
    except Exception as ex:
        # print(ex, file=stderr)
        exit(1)

if __name__ == "__main__":
    main()
