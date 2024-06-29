"""
About:
------

The sina_download_files tool is a command-line interface for downloading various NLP resources from pre-specified URLs. It is a part of the sinatools package and provides options to choose which files to download and to specify a download directory. The tool automatically handles file extraction for zip and tar.gz files.

Usage:
------

Below is the usage information that can be generated by running sina_download_files --help.

.. code-block:: none

    Usage:
     sina_download_files [OPTIONS]

.. code-block:: none

        Options:
        -f, --files FILES
            Names of the files to download. Available files are: ner, morph, salma_model, salma_tokenizer, glosses_dic, lemma_dic, five_grams, four_grams, three_grams, two_grams. 
            If no file is specified, all files will be downloaded.

Examples:
---------

.. code-block:: none

    sina_download_files -f morph ner 
    This command will download only the `morph` and `ner` files to the default directory.

Note:
-----

.. code-block:: none

    - The script automatically handles the extraction of zip and tar.gz files after downloading.
    - Ensure you have the necessary permissions to write to the specified directory.
    - The default download directory is based on the operating system and can be obtained using the `get_appdatadir` function.


"""

import argparse
from sinatools.DataDownload.downloader import download_file
from sinatools.DataDownload.downloader import download_files
from sinatools.DataDownload.downloader import get_appdatadir
from sinatools.DataDownload.downloader import urls


def main():
    parser = argparse.ArgumentParser(description="Download files from specified URLs.")
    parser.add_argument('-f', '--files', nargs="*", choices=urls.keys(),
                        help="Names of the files to download. Available files are: "
                             f"{', '.join(urls.keys())}. If no file is specified, all files will be downloaded.")
    
    get_appdatadir()

    args = parser.parse_args()

    if args.files:
        for file in args.files:
            url = urls[file]
            download_file(url)
    else:
        download_files()

if __name__ == '__main__':
    main()

#sina_download_files -f morph ner