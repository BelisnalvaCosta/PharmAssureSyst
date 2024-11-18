from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''  # Substitua com seu email
app.config['MAIL_PASSWORD'] = ''  # Substitua com sua senha
mail = Mail(app)

# Banco de dados simples em memória (Substitua com um banco real)
clientes = []
medicamentos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de autenticação do usuário (Simulada)
        email = request.form['email']
        senha = request.form['senha']
        # Simulação de verificação (substitua com um banco real)
        for cliente in clientes:
            if cliente['email'] == email and check_password_hash(cliente['senha'], senha):
                return redirect(url_for('index'))
        flash('Email ou senha incorretos')
    return render_template('login.html')

@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        endereco = request.form['endereco']
        clientes.append({
            'nome': nome,
            'telefone': telefone,
            'email': email,
            'senha': senha,
            'endereco': endereco
        })
        flash('Cliente cadastrado com sucesso')
        return redirect(url_for('login'))
    return render_template('cadastro_cliente.html')

@app.route('/cadastro_medicamento', methods=['GET', 'POST'])
def cadastro_medicamento():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        local = request.form['local']
        medicamentos.append({
            'nome': nome,
            'descricao': descricao,
            'preco': preco,
            'local': local
        })
        flash('Medicamento cadastrado com sucesso')
        return redirect(url_for('index'))
    return render_template('cadastro_medicamento.html')

@app.route('/buscar_medicamento', methods=['GET', 'POST'])
def buscar_medicamento():
    resultado = None
    if request.method == 'POST':
        nome = request.form['medicamento']
        for medicamento in medicamentos:
            if medicamento['nome'].lower() == nome.lower():
                resultado = f"Medicamento encontrado: {medicamento['nome']}, Local: {medicamento['local']}, Preço: {medicamento['preco']}."
                send_email('Medicamento Encontrado', f'O medicamento {medicamento["nome"]} foi encontrado no local: {medicamento["local"]}.')
                return render_template('buscar_medicamento.html', resultado=resultado)
        
        resultado = "Medicamento não encontrado."
        send_email('Medicamento Não Encontrado', f'O medicamento solicitado não foi encontrado.')
    return render_template('buscar_medicamento.html', resultado=resultado)

def send_email(subject, body):
    msg = Message(subject,
                  sender='',
                  recipients=[''])
    msg.body = body
    try:
        mail.send(msg)
    except Exception as e:
        print(f'Erro ao enviar email: {e}')

if __name__ == '__main__':
    app.run(debug=True)


