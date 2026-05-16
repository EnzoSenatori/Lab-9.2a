from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

mensagens = {}
proximo_id = 1


@app.get("/")
def raiz():
    return {"mensagem": "API de mensagens. Use /mensagens para listar."}


@app.get("/mensagens")
def listar_mensagens():
    return mensagens


@app.get("/mensagens/{id}")
def obter_mensagem(id: int):
    if id not in mensagens:
        return JSONResponse({"erro": "Mensagem nao encontrada"}, status_code=404)
    return mensagens[id]


@app.post("/mensagens")
async def criar_mensagem(request: Request):
    global proximo_id
    dados = await request.json()
    if dados is None or "texto" not in dados:
        return JSONResponse({"erro": "Campo 'texto' e obrigatorio"}, status_code=400)
    nova_mensagem = {"texto": dados["texto"]}
    mensagens[proximo_id] = nova_mensagem
    resposta = {"id": proximo_id, "texto": nova_mensagem["texto"]}
    proximo_id = proximo_id + 1
    return JSONResponse(resposta, status_code=201)


@app.put("/mensagens/{id}")
async def atualizar_mensagem(id: int, request: Request):
    if id not in mensagens:
        return JSONResponse({"erro": "Mensagem nao encontrada"}, status_code=404)
    dados = await request.json()
    if dados is None or "texto" not in dados:
        return JSONResponse({"erro": "Campo 'texto' e obrigatorio"}, status_code=400)
    mensagens[id] = {"texto": dados["texto"]}
    return {"id": id, "texto": mensagens[id]["texto"]}


@app.delete("/mensagens/{id}")
def deletar_mensagem(id: int):
    if id not in mensagens:
        return JSONResponse({"erro": "Mensagem nao encontrada"}, status_code=404)
    del mensagens[id]
    return {"mensagem": "Mensagem deletada com sucesso"}