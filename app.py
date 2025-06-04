from flask import Flask, render_template, jsonify, request
from config.dispositivos import estado_dispositivos
from controladores.controle_led import controla_led
from controladores.controle_porta import controla_porta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', dispositivos=estado_dispositivos)

@app.route('/atualizar_led', methods=['POST'])
def atualizar_led():
    data = request.json
    predio = data['predio']
    comodo = data['comodo']
    acao = data['acao']
    
    controla_led(estado_dispositivos, predio, comodo, acao)
    return jsonify(estado_dispositivos)

@app.route('/atualizar_porta', methods=['POST'])
def atualizar_porta():
    data = request.json
    predio = data['predio']
    acao = data['acao']
    
    controla_porta(estado_dispositivos, predio, acao)
    return jsonify(estado_dispositivos)

if __name__ == '__main__':
    app.run(debug=True) 