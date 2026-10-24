import json
import time
from pyscript import document
import re
from pyodide.ffi import create_proxy

with open("dados.json", encoding="utf-8") as f:
    instrumentos = json.load(f)["instrumentos"]

telemetria = {"buscas": 0, "bloqueadas": 0, "inicio": time.time()}


def renderizar(lista):
    grid = document.getElementById("grid")
    grid.innerHTML = ""
    for item in lista:
        card = document.createElement("div")
        card.className = "card"
        card.innerHTML = (
            f'<img src="src/assets/{item["imagem"]}" alt="{item["nome"]}">'
            f'<h3>{item["nome"]}</h3><p class="norma"></p>'
        )
        grid.appendChild(card)


def atualizar_telemetria():
    seg = int(time.time() - telemetria["inicio"])
    document.getElementById("telemetria").innerText = (
        f'Buscas: {telemetria["buscas"]} | '
        f'Bloqueadas: {telemetria["bloqueadas"]} | Tempo: {seg}s'
    )


def validar_entrada(texto):
    texto = texto.strip()
    if not texto:
        return False, "Digite algo para buscar."
    if len(texto) > 30:
        return False, "Máximo de 30 caracteres."
    if not re.fullmatch(r"[A-Za-zÀ-ÿ0-9 ]+", texto):
        return False, "Caracteres inválidos."
    return True, texto


def buscar(event):
    texto = document.getElementById("busca").value
    msg = document.getElementById("mensagem")
    ok, resultado = validar_entrada(texto)
    if not ok:
        telemetria["bloqueadas"] += 1
        msg.innerText = resultado
    else:
        telemetria["buscas"] += 1
        msg.innerText = ""
        filtrados = [i for i in instrumentos if resultado.lower() in i["nome"].lower()]
        renderizar(filtrados)
    atualizar_telemetria()


document.getElementById("btn-buscar").addEventListener("click", create_proxy(buscar))

renderizar(instrumentos)
atualizar_telemetria()