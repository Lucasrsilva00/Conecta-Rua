#!/usr/bin/env python3
"""
Verifica contraste WCAG 2.2 entre cores de texto e fundos de um site
scroll-driven.

O motor de sites animados desenha quadros de vídeo no canvas. Texto sobre
canvas só é acessível se o scrim/overlay garantir contraste mínimo em TODOS
os quadros — inclusive nos claros e nos escuros. Este script faz duas coisas:

1. Calcula a razão de contraste entre duas cores (sem dependências).
2. Amostra a luminância média de uma região de um quadro (precisa Pillow)
   e calcula o contraste do texto contra ela.

Uso básico (cores):
    python checar_contraste.py --texto "#EAF6EE" --fundo "#05080a"

Texto grande (>= 18.66px bold ou >= 24px):
    python checar_contraste.py --texto "#F97316" --fundo "#05080a" --grande

Lote a partir de um JSON:
    python checar_contraste.py --pares pares.json
    # pares.json: [{"texto": "#EAF6EE", "fundo": "#05080a", "rotulo": "hero"}]

Quadro real do vídeo (precisa Pillow):
    python checar_contraste.py --imagem frame-0001.webp --regiao 0,0,640,720 \
        --texto "#EAF6EE" --scrim "#05080a" --scrim-opacidade 0.92

O scrim é composto sobre a cor média da região antes do cálculo, simulando
o overlay real da página.

Saída: tabela legível + JSON no stdout. Código de saída 1 se algum par falhar.

Requisitos: Python 3.8+. Pillow apenas para --imagem (pip install Pillow).
"""

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constantes WCAG 2.2
# ---------------------------------------------------------------------------

LIMIAR_NORMAL = 4.5   # AA texto normal
LIMIAR_GRANDE = 3.0   # AA texto grande
LIMIAR_AAA_NORMAL = 7.0
LIMIAR_AAA_GRANDE = 4.5


# ---------------------------------------------------------------------------
# Conversão e matemática de cor
# ---------------------------------------------------------------------------

def hex_para_rgb(valor):
    """Converte '#RRGGBB' ou 'RRGGBB' em tupla (r, g, b) 0-255."""
    texto = valor.strip().lstrip("#")
    if len(texto) == 3:
        texto = "".join(c * 2 for c in texto)
    if len(texto) != 6:
        raise ValueError(f"cor inválida: {valor!r} (use #RRGGBB)")
    return tuple(int(texto[i:i + 2], 16) for i in (0, 2, 4))


def rgb_para_hex(rgb):
    """Converte (r, g, b) em '#RRGGBB'."""
    return "#{:02X}{:02X}{:02X}".format(*[max(0, min(255, round(c))) for c in rgb])


def luminancia_relativa(rgb):
    """Luminância relativa WCAG (0-1) de uma cor sRGB."""
    canais = []
    for c in rgb:
        s = c / 255.0
        canais.append(s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4)
    r, g, b = canais
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def razao_contraste(rgb_texto, rgb_fundo):
    """Razão de contraste WCAG entre duas cores (1.0 a 21.0)."""
    l1 = luminancia_relativa(rgb_texto)
    l2 = luminancia_relativa(rgb_fundo)
    claro, escuro = max(l1, l2), min(l1, l2)
    return (claro + 0.05) / (escuro + 0.05)


def compor_sobre(fundo_rgb, scrim_rgb, opacidade):
    """Compõe um scrim sobre a cor de fundo (alpha blending simples)."""
    a = max(0.0, min(1.0, opacidade))
    return tuple(
        fundo_rgb[i] * (1 - a) + scrim_rgb[i] * a for i in range(3)
    )


def classificar(razao, grande=False):
    """Devolve (nivel_aa, nivel_aaa) para a razão informada."""
    limiar_aa = LIMIAR_GRANDE if grande else LIMIAR_NORMAL
    limiar_aaa = LIMIAR_AAA_GRANDE if grande else LIMIAR_AAA_NORMAL
    return razao >= limiar_aa, razao >= limiar_aaa


# ---------------------------------------------------------------------------
# Amostragem de imagem (opcional — requer Pillow)
# ---------------------------------------------------------------------------

def cor_media_regiao(caminho, regiao=None):
    """Luminância/cor média de uma região do quadro.

    `regiao` no formato 'x,y,largura,altura'. Sem região, usa o quadro inteiro.
    """
    try:
        from PIL import Image
    except ImportError:
        print(
            "Erro: --imagem exige Pillow. Instale com: pip install Pillow",
            file=sys.stderr,
        )
        sys.exit(1)

    imagem = Image.open(caminho).convert("RGB")

    if regiao:
        try:
            x, y, largura, altura = (int(v) for v in regiao.split(","))
        except ValueError:
            print("Erro: --regiao deve ser 'x,y,largura,altura'", file=sys.stderr)
            sys.exit(1)
        caixa = (x, y, x + largura, y + altura)
        imagem = imagem.crop(caixa)

    # Reduz para 1x1: média ponderada dos pixels da região
    media = imagem.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    return tuple(media)


# ---------------------------------------------------------------------------
# Avaliação de um par
# ---------------------------------------------------------------------------

def avaliar_par(texto_hex, fundo_rgb, rotulo, grande=False, scrim_hex=None,
                scrim_opacidade=0.0):
    """Calcula e devolve o resultado de um par texto/fundo."""
    rgb_texto = hex_para_rgb(texto_hex)

    if scrim_hex:
        fundo_rgb = compor_sobre(fundo_rgb, hex_para_rgb(scrim_hex), scrim_opacidade)

    razao = razao_contraste(rgb_texto, fundo_rgb)
    passa_aa, passa_aaa = classificar(razao, grande)

    return {
        "rotulo": rotulo,
        "texto": texto_hex.upper(),
        "fundo": rgb_para_hex(fundo_rgb),
        "razao": round(razao, 2),
        "grande": grande,
        "aa": passa_aa,
        "aaa": passa_aaa,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def ler_argumentos():
    cli = argparse.ArgumentParser(
        description="Verifica contraste WCAG 2.2 para sites scroll-driven"
    )
    cli.add_argument("--texto", help="Cor do texto em #RRGGBB")
    cli.add_argument("--fundo", help="Cor de fundo em #RRGGBB")
    cli.add_argument(
        "--grande", action="store_true",
        help="Texto grande (>= 18.66px bold ou >= 24px): limiar 3:1",
    )
    cli.add_argument("--pares", help="JSON com lista de pares para checar em lote")
    cli.add_argument("--imagem", help="Quadro do vídeo (WebP/PNG) para amostrar")
    cli.add_argument(
        "--regiao", help="Região da imagem: 'x,y,largura,altura' (padrão: tudo)",
    )
    cli.add_argument("--scrim", help="Cor do scrim/overlay aplicado sobre o quadro")
    cli.add_argument(
        "--scrim-opacidade", type=float, default=0.0,
        help="Opacidade do scrim de 0 a 1 (padrão: 0)",
    )
    cli.add_argument("--json", action="store_true", help="Saída somente em JSON")
    return cli.parse_args()


def imprimir_tabela(resultados):
    """Mostra os resultados em tabela legível."""
    cabecalho = f"{'RÓTULO':<22} {'TEXTO':<9} {'FUNDO':<9} {'RAZÃO':>6}  AA   AAA"
    print(cabecalho)
    print("-" * len(cabecalho))
    for r in resultados:
        aa = "SIM" if r["aa"] else "NÃO"
        aaa = "SIM" if r["aaa"] else "NÃO"
        print(
            f"{r['rotulo'][:22]:<22} {r['texto']:<9} {r['fundo']:<9} "
            f"{r['razao']:>5}:1  {aa:<3}  {aaa}"
        )


def principal():
    args = ler_argumentos()

    # Modo lote
    if args.pares:
        caminho = Path(args.pares)
        if not caminho.exists():
            print(f"Erro: arquivo não encontrado: {caminho}", file=sys.stderr)
            sys.exit(1)
        with open(caminho, encoding="utf-8") as arq:
            pares = json.load(arq)
        resultados = [
            avaliar_par(
                p["texto"], hex_para_rgb(p["fundo"]),
                p.get("rotulo", f"par-{i + 1}"), p.get("grande", False),
                p.get("scrim"), p.get("scrim_opacidade", 0.0),
            )
            for i, p in enumerate(pares)
        ]
    else:
        if not args.texto:
            print("Erro: informe --texto e --fundo (ou --pares)", file=sys.stderr)
            sys.exit(1)

        if args.imagem:
            fundo_rgb = cor_media_regiao(args.imagem, args.regiao)
            rotulo = f"imagem:{Path(args.imagem).name}"
            if args.regiao:
                rotulo += f"@{args.regiao}"
        elif args.fundo:
            fundo_rgb = hex_para_rgb(args.fundo)
            rotulo = "cores"
        else:
            print("Erro: informe --fundo ou --imagem", file=sys.stderr)
            sys.exit(1)

        resultados = [
            avaliar_par(
                args.texto, fundo_rgb, rotulo, args.grande,
                args.scrim, args.scrim_opacidade,
            )
        ]

    if args.json:
        print(json.dumps(resultados, indent=2, ensure_ascii=False))
    else:
        imprimir_tabela(resultados)
        print()
        print(json.dumps(resultados, indent=2, ensure_ascii=False))

    if any(not r["aa"] for r in resultados):
        print(
            "\nFALHA: pelo menos um par não atinge AA (4.5:1 normal / 3:1 grande).",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    principal()
