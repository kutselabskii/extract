import argparse
from pathlib import Path
from shutil import copy2
import codecs

DESCRIPTION = """
    Copies files mentioned in filenames.txt from one directory to another using settings from settings.txt file.

    settings.txt:
        Consists of three text lines
        1) Absolute path to directory FROM which files should be copied
        2) Absolute path to directory TO which files should be copied
        3) Name template. Each file name will be constructed using that template.
            It should look like this:
                [some data]*[more data].[file extension]
            For example:
                Photo*_111.raw

    filenames.txt:
        Put file names one after one. They should be separated with line endings
        Example:
            file
            another file
            photo3

    Resulting filenames, using data from examples above, will look like this:
        Photofile_111.raw
        Photoanother file_111.raw
        Photophoto3_111.raw
    """

settings = open(Path(__file__).absolute().parent.joinpath('settings.txt')).read()


def main():
    parser = argparse.ArgumentParser(description = DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args()

    startDirectory, endDirectory, template = open(Path(__file__).absolute().parent.joinpath('settings.txt'), 'r').read().splitlines()
    files = codecs.open(Path(__file__).absolute().parent.joinpath('filenames.txt'), 'r', 'utf-8').read().replace(',', ' ').split()

    for file in files:
        path = Path(startDirectory).joinpath(template.replace('*', file))
        copy2(path, endDirectory)
    
    input('Write anything and press Enter\n')


if __name__ == "__main__":
    main()
