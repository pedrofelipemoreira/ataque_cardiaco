from flask import Flask, request, render_template, jsonify
import pickle

app = Flask(__name__)

try:
    # Carregar o modelo salvo
    with open('venv/kcla_model.pkl', 'rb') as model_file:
        kcla = pickle.load(model_file)

except FileNotFoundError:
    print("Arquivo do modelo não encontrado.")
    kcla = None

except AttributeError as e:
    print(f"Erro ao carregar o modelo: {e}")
    kcla = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/genero')
def genero():
    return render_template('genero.html')

@app.route('/f.etaria')
def f_etaria():
    return render_template('f.etaria.html')

@app.route('/predict', methods=['POST']) 
def predict():
    if kcla is None:
        return "Erro: Modelo não carregado. Verifique se o arquivo do modelo está presente."

    # Obter os parâmetros do formulário
    parametros = [
        float(request.form['age']),
        float(request.form['sex']),
        float(request.form['cp']),
        float(request.form['trtbps']),
        float(request.form['chol']),
        float(request.form['fbs']),
        float(request.form['thalachh']),
    ]

    # Fazer a predição
    resultado = kcla.predict([parametros])[0]

    # Interpretação do resultado
    if resultado == 0: 
        resultado = 'Não há chances de ataque cardíaco'
    else:
        resultado = 'Há chances de ter um ataque cardíaco'

    return f'Seu resultado é: "{resultado}"!'

if __name__ == '__main__':
    app.run(debug=True)
