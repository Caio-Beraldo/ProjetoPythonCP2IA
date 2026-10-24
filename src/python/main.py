import json
import time
from pyscript import document

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


renderizar(instrumentos)
atualizar_telemetria()