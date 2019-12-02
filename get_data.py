from bs4 import BeautifulSoup
from requests import get
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool

from constants import DATA_URL, DATA_DIR

def download_file(filename):
    with open(Path(DATA_DIR) / filename, 'wb') as f:
        f.write(get(DATA_URL + filename).content)

def get_data():

    index = get(DATA_URL)
    soup = BeautifulSoup(index.content)
    
    data_links = [link['href'] for link in soup.select('a') if link['href'].endswith('.tgz')]

    n_links = len(data_links)
    with Pool(16) as p:
        list(tqdm(p.imap_unordered(download_file, data_links), total=n_links))

if __name__ == '__main__':
    get_data()