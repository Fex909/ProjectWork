from flask import Flask, render_template, request, send_file, jsonify
import mysql.connector
from dvr_generator import DVRGenerator
from datetime import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'

def get_db_connection():
    """Funzione riutilizzabile per la connessione al database"""
    return mysql.connector.connect(
        host='localhost',
        database='dvr_db',
        user='root',
        password='mypassword'
    )

def get_risks_for_company(company_id):
    """Recupera tutti i rischi associati a un'azienda dal database"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, tipo, probabilita, gravita, esposizione, descrizione FROM rischi WHERE id_azienda = %s",
        (company_id,)
    )
    risks = cursor.fetchall()
    cursor.close()
    connection.close()
    return risks

def get_mitigations_for_risk(risk_id):
    """Recupera tutte le mitigazioni associate a un rischio"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT nome, descrizione FROM mitigazioni WHERE id_rischio = %s",
        (risk_id,)
    )
    mitigations = cursor.fetchall()
    cursor.close()
    connection.close()
    return mitigations

@app.route('/')
def index():
    """Home page con lista di aziende dal database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, nome FROM aziende")
        aziende = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html', aziende=aziende)
    except Exception as e:
        return f"Errore nel caricamento della pagina: {str(e)}", 500

@app.route('/api/generate-dvr', methods=['POST'])
def generate_dvr():
    """Endpoint per generare il DVR con i dati dal database"""
    try:
        data = request.json
        company_id = data.get('company_id')

        # Recupera i rischi dal database
        risks_data = get_risks_for_company(company_id)

        # Formatta i dati per il generatore
        formatted_risks = [
            {
                'type': r['tipo'],
                'probability': r['probabilita'],
                'severity': r['gravita'],
                'exposure': r['esposizione'],
                'priority': int(r['probabilita']) * int(r['gravita']) * int(r['esposizione']),
                'description': r['descrizione']
            }
            for r in risks_data
        ]

        # Crea istanza del generatore
        dvr = DVRGenerator()
        dvr.add_header()
        dvr.add_risk_matrix(formatted_risks)
        
        # Aggiungi mitigazioni se disponibili
        for risk in risks_data:
            mitigations = get_mitigations_for_risk(risk['id'])
            if mitigations:
                dvr.add_mitigation_section(mitigations)

        # Genera nome file univoco e salva
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"DVR_{timestamp}.docx"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        dvr.save(filepath)

        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add-risk', methods=['POST'])
def add_risk():
    """Endpoint per aggiungere un nuovo rischio al database"""
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO rischi (id_azienda, tipo, probabilita, gravita, esposizione, descrizione)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['id_azienda'],
            data['tipo'],
            data['probabilita'],
            data['gravita'],
            data['esposizione'],
            data.get('descrizione', '')
        ))
        conn.commit()
        return {'status': 'ok', 'message': 'Rischio aggiunto con successo'}
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/aziende', methods=['GET'])
def get_aziende():
    """Endpoint per recuperare la lista di aziende in formato JSON"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome FROM aziende")
        aziende = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(aziende)
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=8000)
