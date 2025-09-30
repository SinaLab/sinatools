import os
import sys
from pathlib import Path
import requests  
import zipfile
from tqdm import tqdm
import tarfile
urls = {
    'morph': 'https://sina.birzeit.edu/lemmas_dic.pickle',
    'ner': 'https://sina.birzeit.edu/Wj27012000.tar.gz',
    # 'wsd_model': 'https://sina.birzeit.edu/bert-base-arabertv02_22_May_2021_00h_allglosses_unused01.zip',
    # 'wsd_tokenizer': 'https://sina.birzeit.edu/bert-base-arabertv02.zip',
    'one_gram': 'https://sina.birzeit.edu/one_gram.pickle',
    'five_grams': 'https://sina.birzeit.edu/five_grams.pickle',
    'four_grams':'https://sina.birzeit.edu/four_grams.pickle',
    'three_grams':'https://sina.birzeit.edu/three_grams.pickle',
    'two_grams':'https://sina.birzeit.edu/two_grams.pickle',
    'graph_l2':'https://sina.birzeit.edu/graph_l2.pkl',
    'graph_l3':'https://sina.birzeit.edu/graph_l3.pkl',
    'relation':'https://sina.birzeit.edu/relation_model.zip'
}

def get_appdatadir():
    """
    This method checks if the directory exists and creates if it doesn't. And returns the path to the directory where the application data is stored.
   
    Returns:
    --------
    Path: A pathlib.Path object representing the path to the application data directory.

    Raises:
    -------
    None.

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from sinatools.DataDownload import downloader

        path = downloader.get_appdatadir()

        Windows: 'C:/Users/<Username>/AppData/Roaming/sinatools'
        MacOS: '/Users/<Username>/Library/Application Support/sinatools'
        Linux: '/home/<Username>/.sinatools'
        Google Colab: '/content/sinatools'

    """
    home = str(Path.home())
    if 'google.colab' in sys.modules:
        path = Path('/content/sinatools')
    elif sys.platform == 'win32':
        path = Path(home, 'AppData/Roaming/sinatools')
    elif sys.platform == 'darwin':
        path = Path(home, 'Library/Application Support/sinatools')
    else:
        path = Path(home, '.sinatools')

    if not os.path.exists(path):
        os.makedirs(path)

    return path

def download_file(url, dest_path=get_appdatadir()):
    """
    Downloads a file from the specified URL and saves it to the specified destination path.

    Args:
        url (:obj:`str`): The URL of the file to be downloaded.
        dest_path (:obj:`str`): The destination path to save the downloaded file to. Defaults
            to the user's application data directory.


    Returns:
        :obj:`str`: The absolute path of the downloaded file.

    Raises:
        requests.exceptions.HTTPError: If there was an HTTP error during the request.

    Note:
        This method uses the `requests` and `tqdm` libraries. It also checks if the
        compressed downloaded file type and extracts it.

    **Example:**

    .. highlight:: python
    .. code-block:: python

          download_file(url='https://example.com/data.zip', dest_path='data/')

    """
    filename = os.path.basename(url)
    file_path = os.path.join(dest_path, filename)

    print(filename)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                total_size = int(r.headers.get('content-length', 0))
                block_size = 8192
                progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
                for chunk in r.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
                progress_bar.close()

        # Check the file type and extract accordingly
        file_extension = os.path.splitext(file_path)[1]
        extracted_folder_name = os.path.splitext(file_path)[0]
        
        if file_extension == '.zip':
            extract_zip(file_path, extracted_folder_name)
        elif file_extension == '.gz':

            extract_tar(file_path, extracted_folder_name)
        elif file_extension =='.pickle':
            print(f'Done: {file_extension}')

        else:
            print(f'Unsupported file type for extraction: {file_extension}')

        return file_path

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f'Error 403: Forbidden. The requested file URL {url} could not be downloaded due to insufficient permissions. Please check the URL and try again.')
        else:
            print('An error occurred while downloading the file:', e)

def extract_zip(file_path, extracted_folder_name):
    """
    Extracts the contents of a ZIP file to the specified folder.

    Args:
        file_path (str): The path to the ZIP file.
        extracted_folder_name (str): The name of the folder where the contents will be extracted.

    Returns:
        None
    """
    with zipfile.ZipFile(file_path, 'r') as zip_file:
        zip_file.extractall(extracted_folder_name)


def extract_tar(file_path, dest_path):
    """
    Extracts the contents of a tar.gz file to the specified destination path.

    Args:
        file_path (str): The path to the tar.gz file.
        dest_path (str): The destination path where the contents will be extracted.

    Returns:
        str: The path to the extracted folder if successful, or None if extraction failed.
    """
    try:
        with tarfile.open(file_path, 'r:gz') as tar:
            # Remove the extension from the file name
            extracted_folder_name = os.path.splitext(os.path.basename(file_path))[0]
            extracted_folder_path = os.path.join(dest_path, extracted_folder_name)

            # Extract the contents to the destination path
            tar.extractall(dest_path)
        
        # Remove the compressed file
        os.remove(file_path)
        
        return extracted_folder_path

    except tarfile.ReadError:
        print(f'Failed to extract the file: {file_path}')
        return None


def download_files():
    """
    Downloads multiple files from a dictionary of URLs using the download_file() function.
    Returns:
        None
    """
    for url in urls.values():
        download_file(url)
        download_folder_from_hf("SinaLab/ArabGlossBERT", "bert-base-arabertv02_22_May_2021_00h_allglosses_unused01")
        download_folder_from_hf("SinaLab/ArabGlossBERT", "bert-base-arabertv02")    


def download_folder_from_hf(repo_url, folder_name):
    
    # Hugging Face API to fetch files from the repository
    api_url = f"https://huggingface.co/api/models/{repo_url}/tree/main/{folder_name}"

    # Make the request to get the folder structure
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to fetch folder contents. Status code: {response.status_code}")
        return
    
    folder_content = response.json()
    
    # Download each file in the folder
    for file_info in folder_content:
        file_name = file_info["path"]
        file_url = f"https://huggingface.co/{repo_url}/resolve/main/{file_name}"
        
        # Download the file and save it to the output directory
        file_response = requests.get(file_url)
        if file_response.status_code == 200:
            # Create any necessary directories
            output_file_path = os.path.join(get_appdatadir(), file_name)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file_path, 'wb') as f:
                f.write(file_response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download {file_name}. Status code: {file_response.status_code}")
