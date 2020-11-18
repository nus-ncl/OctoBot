#!/usr/bin/python3


def read_file(filename):
    """
    Returns content of file provided
    :param filename: filename to read
    :return: content of the file
    """

    with open(filename) as f:
        content = f.readlines()
        f.close()

    return ''.join([l.strip() for l in content])
