# Use uma imagem base com Python 3.9
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requeriments.txt

# Copie o restante da aplicação
COPY . .

# Exponha a porta que a aplicação Flask usará
EXPOSE 8080

# Defina a variável de ambiente para permitir a inicialização do Flask
ENV FLASK_APP=app.py

# Comando para executar o servidor Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
