function generateDVR() {
    const btn = document.querySelector('.download-btn');
    const messageDiv = document.getElementById('message');
    
    btn.disabled = true;
    btn.innerHTML = '⏳ Generazione in corso...';
    messageDiv.innerHTML = '';

    // Raccogli i dati dal form
    const companyId = parseInt(document.getElementById('company-id').value);
    const riskType = document.getElementById('risk-type').value;
    const probability = parseInt(document.getElementById('probability').value);
    const severity = parseInt(document.getElementById('severity').value);
    const exposure = parseInt(document.getElementById('exposure').value);
    const description = document.getElementById('description').value;

    // Validazione
    if (!companyId || !riskType) {
        alert('Seleziona un\'azienda e un tipo di rischio');
        btn.disabled = false;
        btn.innerHTML = '📄 Genera e Scarica DVR';
        return;
    }

    // Prepara il payload
    const riskData = {
        company_id: companyId,
        risks: [
            {
                type: riskType,
                probability: probability,
                severity: severity,
                exposure: exposure,
                priority: probability * severity * exposure,
                description: description
            }
        ]
    };

    // Invia richiesta al backend
    fetch('/api/generate-dvr', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(riskData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => { throw new Error(data.error); });
        }
        return response.blob();
    })
    .then(blob => {
        // Crea link per il download
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `DVR_${Date.now()}.docx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        messageDiv.innerHTML = '✅ DVR generato e scaricato con successo!';
        messageDiv.classList.add('success');
        
        btn.disabled = false;
        btn.innerHTML = '📄 Genera e Scarica DVR';
    })
    .catch(error => {
        messageDiv.innerHTML = '❌ Errore: ' + error.message;
        messageDiv.classList.add('error');
        
        btn.disabled = false;
        btn.innerHTML = '📄 Genera e Scarica DVR';
    });
}
