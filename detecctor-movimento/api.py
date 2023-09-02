from flask import Flask ,send_file

app = Flask(__name__)

@app.route("/imagem", methods=['GET'])
def enviarMensagem():
    return send_file('imagem-bandido/imagem.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)