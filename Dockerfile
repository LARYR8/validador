# Use uma imagem base com Python 3.9
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante da aplicação
COPY . .

# Exponha a porta que a aplicação Flask usará
EXPOSE 8080

# Comando para executar o servidor Flask com gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
