import sys
from httpy import httpy


def main():
    url = sys.argv[1]
    response = httpy.get(url, validate=True)

    print response.body


if __name__ == '__main__':
    main()