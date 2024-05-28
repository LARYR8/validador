from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
from validar_telefone import validar_telefones_em_lote
import os
from werkzeug.utils import secure_filename
import io
from io import BytesIO  # Adicionado

print("Iniciando o servidor Flask...")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}

resultados_globais = []

# Função para converter números de telefone para o formato correto
def converter_telefone(telefone):
    telefone = ''.join(filter(str.isdigit, str(telefone)))
    if not telefone.startswith('55'):
        telefone = '55' + telefone
    return telefone

# Função para validar números de telefone
def validar_numero(telefone):
    return len(telefone) == 13 and telefone.isdigit()

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    global resultados_globais
    resultados = []
    if request.method == 'POST':
        if 'file' not in request.files:
            print("Nenhum arquivo enviado")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("Nenhum arquivo selecionado")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print("Carregando a nova planilha Excel...")
            df = pd.read_excel(filepath, header=None)
            print("Obtendo a coluna de telefones...")
            telefones = df[0].dropna().tolist()
            telefones_convertidos = [converter_telefone(tel) for tel in telefones if validar_numero(converter_telefone(tel))]
            print("Processando os resultados...")
            resultados_api = validar_telefones_em_lote(telefones_convertidos)
            if isinstance(resultados_api, list) and all(isinstance(item, dict) for item in resultados_api):
                resultados = [{"phone": phone, "exists": result.get('exists', False)} for phone, result in zip(telefones_convertidos, resultados_api)]
                resultados.sort(key=lambda x: x['exists'], reverse=True)
                resultados_globais = resultados  # Salvar os resultados globalmente
            else:
                print("Formato inesperado de resposta da API:", resultados_api)
                resultados = []

    return render_template('index.html', resultados=resultados)

@app.route('/download_results')
def download_results():
    global resultados_globais
    # Converter os resultados globais em um DataFrame
    df = pd.DataFrame(resultados_globais)
    # Salvar o DataFrame em um buffer de memória como CSV usando BytesIO
    buffer = BytesIO()
    df.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)
    # Enviar o buffer como um arquivo para download
    return send_file(buffer, as_attachment=True, download_name='resultados_validacao.csv', mimetype='text/csv')

if __name__ == '__main__':
    print("Executando o servidor Flask...")
    app.run(debug=True, host='0.0.0.0', port=8080)