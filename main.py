from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ARQUIVO = "agenda.json"


def carregar():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar(lista):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)


@app.post("/agendar")
def agendar(dados: dict):

    agenda = carregar()

    for ag in agenda:
        if ag["data"] == dados["data"] and ag["hora"] == dados["hora"]:
            return {
                "sucesso": False,
                "mensagem": "Esse horário já está ocupado."
            }

    agenda.append(dados)

    salvar(agenda)

    return {
        "sucesso": True,
        "mensagem": "Agendamento realizado com sucesso!"
    }


@app.get("/agenda")
def agenda():
    return carregar()