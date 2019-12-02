import tarfile

from pathlib import Path

from constants import DATA_DIR

def extract_data():
    for data_path in Path(DATA_DIR).rglob('*.tgz'):
        with tarfile.open(data_path, 'r:gz') as tf:
            tf.extractall(DATA_DIR)

if __name__ == '__main__':
    extract_data()