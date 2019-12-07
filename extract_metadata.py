import json
from pathlib import Path
from constants import DATA_DIR


def extract_metadata():
    # just do everything relative to the readme
    all_metadata = []
    for en,readme_file in enumerate(Path(DATA_DIR).rglob('*README')):
        with open(readme_file) as f:
            metadata = {}
            for l in f:
                split = l[:-1].split(':')
                if len(split) == 2:
                    metadata[split[0].strip()] = split[1].strip()

        # get the wav file locations
        metadata['wav_files'] = [str(wav_file) for wav_file in readme_file.parent.parent.rglob('*.wav')]

        # assign a uid
        metadata['uid'] = en
        all_metadata.append(metadata)
            
    with open('all_metadata.json', 'w') as f:
        json.dump(all_metadata, f)


if __name__ == '__main__':
    extract_metadata()
