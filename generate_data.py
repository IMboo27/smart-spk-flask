
import json

WEIGHTS = {
    'kualitas': 0.25,
    'keamanan': 0.20,
    'kecepatan': 0.20,
    'keahlian': 0.20,
    'harga': 0.15
}

RATINGS_FILE = 'ratings.json'
DATA_FILE = 'data.json'

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def normalisasi_nilai(data, kriteria):
    nilai_list = [r[kriteria] for r in data]
    min_val = min(nilai_list)
    max_val = max(nilai_list)
    for r in data:
        if max_val != min_val:
            r[f'norm_{kriteria}'] = (r[kriteria] - min_val) / (max_val - min_val)
        else:
            r[f'norm_{kriteria}'] = 1

def hitung_smart_normalisasi(ratings):
    for kriteria in WEIGHTS:
        normalisasi_nilai(ratings, kriteria)

    hasil = {}
    for r in ratings:
        pid = r['penebang_id']
        total = sum(r[f'norm_{k}'] * WEIGHTS[k] for k in WEIGHTS)
        hasil[pid] = {
            'total_smart': round(total, 3),
            'rating_bintang': round(1 + (total * 4), 2)
        }
    return hasil

def update_data_file():
    ratings = load_json(RATINGS_FILE)
    penebang = load_json(DATA_FILE)
    hasil_smart = hitung_smart_normalisasi(ratings)

    for p in penebang:
        pid = p['id']
        if pid in hasil_smart:
            p['total_smart'] = hasil_smart[pid]['total_smart']
            p['rating_bintang'] = hasil_smart[pid]['rating_bintang']

    save_json(penebang, DATA_FILE)

if __name__ == '__main__':
    update_data_file()
    print('Sukses membuat ulang file data.json dari ratings.json dengan normalisasi SMART.')
