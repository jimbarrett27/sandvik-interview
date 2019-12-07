import json
import numpy as np

from scipy.io import wavfile
from scipy.signal import welch
from pathlib import Path

from tqdm import tqdm
from multiprocessing import Pool

from typing import Dict, Tuple


def extract_features(time_series: np.ndarray) -> np.ndarray:

    # 16k sampling frequency
    pgram = welch(time_series, 16000, nperseg=2048)
    
    # only keep frequencies in the human vocal range
    return pgram[1][pgram[0] < 300]


def load_data_and_extract_features(metadata: Dict) -> Tuple[np.ndarray, np.ndarray]:

    try: 
        label = metadata['Gender']
        
        file_locations = metadata['wav_files']
        
        all_features = []
        all_labels = []
        for f in file_locations:
            # get the intensity time series
            time_series = wavfile.read(f)[1]

            features = extract_features(time_series)

            all_features.append(features)
            all_labels.append(label)

        
        return np.row_stack(all_features), all_labels
    except:
        return None


def get_features_and_labels():

    all_metadata = json.loads(Path('all_metadata.json').read_text())

    with Pool(8) as p:
        features_and_labels = list(tqdm(p.imap_unordered(load_data_and_extract_features, all_metadata), total=len(all_metadata)))

    features_and_labels = [fl for fl in features_and_labels if fl]

    all_labels = []
    all_features = []
    for features, labels in features_and_labels:
        all_labels += labels
        all_features.append(features)


    np.savetxt('features.txt', np.row_stack(all_features))
    Path('labels.txt').write_text('\n'.join(all_labels))
    

if __name__ == '__main__':
    get_features_and_labels()