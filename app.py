
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

DATA_FILE = 'data.json'
RATINGS_FILE = 'ratings.json'

WEIGHTS = {
    'kualitas': 0.25,
    'keamanan': 0.20,
    'kecepatan': 0.20,
    'keahlian': 0.20,
    'harga': 0.15
}

def hitung_smart(rating):
    nilai = (
        rating['kualitas'] * WEIGHTS['kualitas'] +
        rating['keamanan'] * WEIGHTS['keamanan'] +
        rating['kecepatan'] * WEIGHTS['kecepatan'] +
        rating['keahlian'] * WEIGHTS['keahlian'] +
        rating['harga'] * WEIGHTS['harga']
    ) / 5.0
    return round(nilai, 3)

def update_data_file():
    with open(RATINGS_FILE) as f:
        rating_data = json.load(f)
    with open(DATA_FILE) as f:
        penebang_data = json.load(f)

    id_to_total = {}
    for rating in rating_data:
        pid = rating['penebang_id']
        smart_value = hitung_smart(rating)
        rating_bintang = round(1 + (smart_value * 4), 2)
        id_to_total[pid] = {'total_smart': smart_value, 'rating_bintang': rating_bintang}

    for p in penebang_data:
        pid = p['id']
        if pid in id_to_total:
            p['total_smart'] = id_to_total[pid]['total_smart']
            p['rating_bintang'] = id_to_total[pid]['rating_bintang']

    with open(DATA_FILE, 'w') as f:
        json.dump(penebang_data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

@app.route('/layanan')
def layanan():
    with open(DATA_FILE) as f:
        penebang = json.load(f)
    penebang_sorted = sorted(penebang, key=lambda x: x.get('total_smart', 0), reverse=True)
    return render_template('layanan.html', penebang=penebang_sorted)

@app.route('/rating', methods=['GET', 'POST'])
def rating():
    if request.method == 'POST':
        new_rating = {
            'penebang_id': request.form['penebang_id'],
            'harga': int(request.form['harga']),
            'kualitas': int(request.form['kualitas']),
            'keahlian': int(request.form['keahlian']),
            'kecepatan': int(request.form['kecepatan']),
            'keamanan': int(request.form['keamanan'])
        }
        with open(RATINGS_FILE) as f:
            rating_data = json.load(f)
        rating_data.append(new_rating)
        with open(RATINGS_FILE, 'w') as f:
            json.dump(rating_data, f, indent=2)
        update_data_file()
        return redirect(url_for('layanan'))

    with open(DATA_FILE) as f:
        penebang = json.load(f)
    return render_template('rating.html', penebang=penebang)

if __name__ == '__main__':
    app.run(debug=True)
