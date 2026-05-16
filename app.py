from flask import Flask, jsonify, request

app = Flask(__name__)

# Armazenamento em memória
mensagens = {}
proximo_id = 1


@app.route("/", methods=["GET"])
def raiz():
    return jsonify({
        "mensagem": "API de mensagens. Use /mensagens para listar."
    })


@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    return jsonify(mensagens)


@app.route("/mensagens/<int:id>", methods=["GET"])
def obter_mensagem(id):
    if id not in mensagens:
        return jsonify({"erro": "Mensagem nao encontrada"}), 404
    return jsonify(mensagens[id])


@app.route("/mensagens", methods=["POST"])
def criar_mensagem():
    global proximo_id

    dados = request.get_json()

    if dados is None or "texto" not in dados:
        return jsonify({"erro": "Campo 'texto' e obrigatorio"}), 400

    nova_mensagem = {"texto": dados["texto"]}
    mensagens[proximo_id] = nova_mensagem

    resposta = {"id": proximo_id, "texto": nova_mensagem["texto"]}
    proximo_id = proximo_id + 1

    return jsonify(resposta), 201


@app.route("/mensagens/<int:id>", methods=["PUT"])
def atualizar_mensagem(id):
    if id not in mensagens:
        return jsonify({"erro": "Mensagem nao encontrada"}), 404

    dados = request.get_json()

    if dados is None or "texto" not in dados:
        return jsonify({"erro": "Campo 'texto' e obrigatorio"}), 400

    mensagens[id] = {"texto": dados["texto"]}

    return jsonify({"id": id, "texto": mensagens[id]["texto"]})


@app.route("/mensagens/<int:id>", methods=["DELETE"])
def deletar_mensagem(id):
    if id not in mensagens:
        return jsonify({"erro": "Mensagem nao encontrada"}), 404
    del mensagens[id]
    return jsonify({"mensagem": "Mensagem deletada com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)