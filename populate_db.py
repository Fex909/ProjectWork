import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='dvr_db',
        user='root',
        password='Esselunga2018!'
    )

def populate_aziende():
    """Popola la tabella aziende con dati di esempio"""
    aziende = [
        ('Esselunga S.p.A.', 'Via Giambologna 1, Milano', '12345678901'),
        ('Brico C S.r.l.', 'Via Roma 50, Torino', '23456789012'),
        ('TechSoft Italia', 'Corso Venezia 10, Milano', '34567890123'),
        ('LogisticaPro S.p.A.', 'Viale Europa 100, Bologna', '45678901234'),
        ('SafetyFirst Ltd.', 'Piazza Duomo 5, Firenze', '56789012345'),
    ]
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = "INSERT INTO aziende (nome, indirizzo, partita_iva) VALUES (%s, %s, %s)"
    
    try:
        for azienda in aziende:
            cursor.execute(query, azienda)
        connection.commit()
        print(f"✅ {len(aziende)} aziende inserite con successo!")
    except Exception as e:
        print(f"❌ Errore nell'inserimento aziende: {e}")
    finally:
        cursor.close()
        connection.close()

def populate_rischi():
    """Popola la tabella rischi con dati di esempio"""
    rischi = [
        # Rischi per Esselunga (id_azienda = 1)
        (1, 'Sicurezza Fisica', 4, 5, 4, 'Incendio in magazzino con merce infiammabile'),
        (1, 'Sicurezza Informatica', 5, 5, 4, 'Ransomware su sistema di e-commerce'),
        (1, 'Sicurezza Informatica', 3, 4, 5, 'Furto di dati clienti da database'),
        (1, 'Rischio Organizzativo', 3, 3, 3, 'Mancanza di backup dei dati critici'),
        
        # Rischi per Brico C (id_azienda = 2)
        (2, 'Sicurezza Fisica', 3, 4, 3, 'Caduta merce da scaffali'),
        (2, 'Sicurezza Informatica', 4, 4, 3, 'Attacco DDoS su sito web di vendita'),
        (2, 'Sicurezza Informatica', 3, 3, 4, 'Compromissione sistema di pagamento'),
        
        # Rischi per TechSoft (id_azienda = 3)
        (3, 'Sicurezza Informatica', 5, 5, 5, 'Attacco APT (Advanced Persistent Threat)'),
        (3, 'Sicurezza Informatica', 4, 4, 4, 'Phishing ai dipendenti'),
        (3, 'Rischio Organizzativo', 3, 4, 3, 'Scarsa formazione sulla sicurezza'),
        
        # Rischi per LogisticaPro (id_azienda = 4)
        (4, 'Sicurezza Fisica', 4, 5, 4, 'Furto di merci in transito'),
        (4, 'Sicurezza Informatica', 3, 4, 4, 'Compromissione sistema di tracciamento'),
        (4, 'Sicurezza Fisica', 3, 3, 3, 'Incidente stradale durante trasporto'),
        
        # Rischi per SafetyFirst (id_azienda = 5)
        (5, 'Sicurezza Fisica', 2, 5, 4, 'Infortunio sul lavoro'),
        (5, 'Sicurezza Informatica', 2, 3, 2, 'Accesso non autorizzato a dati medici'),
    ]
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
        INSERT INTO rischi (id_azienda, tipo, probabilita, gravita, esposizione, descrizione)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    try:
        for rischio in rischi:
            cursor.execute(query, rischio)
        connection.commit()
        print(f"✅ {len(rischi)} rischi inseriti con successo!")
    except Exception as e:
        print(f"❌ Errore nell'inserimento rischi: {e}")
    finally:
        cursor.close()
        connection.close()

def populate_mitigazioni():
    """Popola la tabella mitigazioni con dati di esempio"""
    mitigazioni = [
        # Mitigazioni per rischio 1 (Incendio Esselunga)
        (1, 'Impianto sprinkler automatico', 'Sistema antincendio sprinkler con sensori di temperatura'),
        (1, 'Piano di evacuazione', 'Procedure di evacuazione regolarmente testate e comunicate'),
        
        # Mitigazioni per rischio 2 (Ransomware Esselunga)
        (2, 'Backup giornaliero crittografato', 'Backup automatici su server separato con crittografia AES-256'),
        (2, 'Antimalware avanzato', 'Installazione di EDR (Endpoint Detection and Response)'),
        (2, 'Firewall di nuova generazione', 'Firewall con deep packet inspection e IPS integrato'),
        
        # Mitigazioni per rischio 3 (Furto dati Esselunga)
        (3, 'Crittografia database', 'Database MySQL con crittografia end-to-end'),
        (3, 'Segmentazione di rete', 'Database in DMZ separata da accesso internet'),
        
        # Mitigazioni per rischio 4 (Mancanza backup Esselunga)
        (4, 'Strategia backup 3-2-1', '3 copie dati, 2 media diversi, 1 offline'),
        (4, 'Test di recovery mensili', 'Verifiche mensili della capacità di ripristino'),
        
        # Mitigazioni per rischio 5 (Caduta merce Brico)
        (5, 'Sistemi di ancoraggio scaffali', 'Scaffali ancorati a parete con divisori di sicurezza'),
        (5, 'Formazione sui rischi', 'Corsi di sicurezza per tutti i dipendenti'),
        
        # Mitigazioni per rischio 6 (DDoS Brico)
        (6, 'CDN e WAF', 'Content Delivery Network con Web Application Firewall'),
        (6, 'Rate limiting', 'Implementazione di rate limiting sulla API'),
        
        # Mitigazioni per rischio 8 (APT TechSoft)
        (8, 'Zero Trust Architecture', 'Implementazione di principi Zero Trust con MFA'),
        (8, 'SOC 24/7', 'Security Operations Center con monitoraggio continuo'),
        (8, 'Threat Intelligence', 'Sottoscrizione a servizi di threat intelligence'),
        
        # Mitigazioni per rischio 9 (Phishing TechSoft)
        (9, 'Formazione anti-phishing', 'Simulazioni di phishing mensili con feedback'),
        (9, 'Email gateway sicuro', 'Gateway email con sandboxing e analisi comportamentale'),
        
        # Mitigazioni per rischio 10 (Scarsa formazione TechSoft)
        (10, 'Programma di consapevolezza', 'Corsi di sicurezza informatica obbligatori'),
        (10, 'Policy di sicurezza', 'Documentazione e aggiornamento continuo delle policy'),
        
        # Mitigazioni per rischio 11 (Furto merci LogisticaPro)
        (11, 'GPS tracking real-time', 'Sistema di tracciamento GPS su tutti i veicoli'),
        (11, 'Scorta armata', 'Utilizzo di scorta armata per carichi ad alto valore'),
        
        # Mitigazioni per rischio 12 (Compromissione tracciamento LogisticaPro)
        (12, 'API sicura con autenticazione', 'API RESTful con OAuth2 e SSL/TLS'),
        (12, 'Audit logging', 'Registrazione di tutti gli accessi al sistema di tracciamento'),
    ]
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
        INSERT INTO mitigazioni (id_rischio, nome, descrizione)
        VALUES (%s, %s, %s)
    """
    
    try:
        for mitigazione in mitigazioni:
            cursor.execute(query, mitigazione)
        connection.commit()
        print(f"✅ {len(mitigazioni)} mitigazioni inserite con successo!")
    except Exception as e:
        print(f"❌ Errore nell'inserimento mitigazioni: {e}")
    finally:
        cursor.close()
        connection.close()

def main():
    print("🚀 Inizio popolazione database DVR...")
    print("=" * 50)
    
    populate_aziende()
    populate_rischi()
    populate_mitigazioni()
    
    print("=" * 50)
    print("✅ Database popolato con successo!")
    print("\nDati inseriti:")
    print("  - 5 aziende")
    print("  - 16 rischi")
    print("  - 22 mitigazioni")

if __name__ == '__main__':
    main()
