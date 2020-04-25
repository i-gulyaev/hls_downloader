#!/usr/bin/env python3

import argparse
import itertools
import multiprocessing
import pathlib
import requests


def get_urls(input_file):
    with open(input_file) as ifile:
        for line in ifile:
            line = line.strip()
            if line and (not line.startswith('#')):
                yield line


def compose_output_filename(input_file, output_path):
    return pathlib.PurePosixPath(output_path).joinpath(
        pathlib.Path(input_file).stem + ".ts")


def download_job(url):
    print("Downloading chunk: " + url)
    chunk = requests.get(url)
    return chunk


def download_mt(input_file, output_file, limit):

    num_processes = 16
    with multiprocessing.Pool(num_processes) as pool:
        result = pool.imap(download_job,
                           itertools.islice(
                               get_urls(input_file), 0, limit))

        with open(output_file, 'wb') as ofile:
            for chunk in result:
                ofile.write(chunk.content)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_files', nargs='+', type=str, required=True)
    parser.add_argument('-o', '--output_path', type=str,  required=True)
    parser.add_argument('-l', '--chunk_limit', type=int, default=1000000)

    args = parser.parse_args()

    for ifile in args.input_files:
        ofile = compose_output_filename(ifile, args.output_path)
        download_mt(ifile, ofile, args.chunk_limit)
        print("File '{}' successfully written!".format(ofile))
