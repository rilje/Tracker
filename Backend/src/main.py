from flask import Flask, render_template, request, session, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "RAF2021-2022"
CORS(app)

# Funkcija za povezivanje sa bazom
def get_sql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="lekarski"
    )

# Funkcija za formatiranje datuma u dd.mm.yyyy
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Pretpostavljamo da je datum u formatu 'yyyy-mm-dd'
        return date_obj.strftime('%d.%m.%Y')  # Formatiramo u 'dd.mm.yyyy'
    except ValueError:
        return date_str  

# Ruta za dohvat radnika
@app.route('/')
def index():
    sql_upit = "SELECT * FROM lekarski"
    mydb = get_sql_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(sql_upit)
    data = cursor.fetchall()

    # Formatiranje datuma pre nego što se pošalju u JSON odgovoru
    for radnik in data:
        if 'lekarski' in radnik:
            radnik['lekarski'] = format_date(radnik['lekarski'])
        if 'bzr' in radnik:
            radnik['bzr'] = format_date(radnik['bzr'])

    return jsonify({
        "data": {
            "radnici": data
        }
    }), 200

# Ruta za ažuriranje radnika
@app.route('/azuriraj-radnika', methods=['POST'])
def azuriraj_radnika():
    try:
        podaci = request.get_json()

        id_radnika = podaci['id']
        ime = podaci['ime']
        lekarski = format_date(podaci['lekarski'])  
        bzr = format_date(podaci['bzr'])  

        sql_upit = """
        UPDATE lekarski 
        SET ime = %s, lekarski = %s, bzr = %s 
        WHERE id = %s
        """

        mydb = get_sql_connection()
        cursor = mydb.cursor()
        cursor.execute(sql_upit, (ime, lekarski, bzr, id_radnika))
        mydb.commit()

        
        return jsonify({
            "message": "Radnik je uspešno ažuriran!",
            "data": {
                "ime": ime,
                "lekarski": lekarski,
                "bzr": bzr
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/godisnji')
def svi_godisnji():
    mydb = get_sql_connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute('select * from godisnji')
    data = cursor.fetchall()
    return jsonify({
        "data" : {
            "data" : data
        }
    }), 200

@app.route('/azuriraj-godisnji', methods=['POST'])
def azuriraj_godisnji():
    data = request.get_json()
    # Validacija podataka
    id = data['id']
    ime_prezime = data['ime_prezime']
    godisnji_ukupno_2024 = data['godisnji_ukupno_2024']
    godisnji_ukupno_2025 = data['godisnji_ukupno_2025']
    godisnji_iskorisceno_2024 = data['godisnji_iskorisceno_2024']
    godisnji_iskorisceno_2025 = data['godisnji_iskorisceno_2025']
    godisnji_preostalo_2024 = data['godisnji_preostalo_2024']
    godisnji_preostalo_2025 = data['godisnji_preostalo_2025']

    
    mydb = get_sql_connection()
    cursor = mydb.cursor(dictionary=True)

    sql_upit = """UPDATE godisnji SET godisnji_ukupno_2024=%s, godisnji_ukupno_2025=%s, godisnji_iskorisceno_2024=%s, godisnji_iskorisceno_2025=%s, godisnji_preostalo_2024=%s, godisnji_preostalo_2025=%s where id=%s"""

    cursor.execute(sql_upit, (godisnji_ukupno_2024, godisnji_ukupno_2025, godisnji_iskorisceno_2024, godisnji_iskorisceno_2025, godisnji_preostalo_2024, godisnji_preostalo_2025, id))
    mydb.commit()

    return jsonify({
        "data" : {
            "message" : "Godisnji uspesno izmenjen"
        }
    }), 200

@app.route('/ugovori')
def svi_ugovori():
    mydb = get_sql_connection()
    cursor = mydb.cursor(dictionary=True)

    cursor.execute('select * from ugovor')
    data = cursor.fetchall()
    if not data:
        return jsonify({
            "data" : {
                "message" : "Greska prilikom dohvatanja podataka iz baze"
            }
        }), 400
    return jsonify({
        "data" : {
            "message" : "Uspeno ste dohvatili podatke iz baze",
            "data" : data,
           
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=True)