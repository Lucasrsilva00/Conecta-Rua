# Extração de Quadros — Conecta-Rua

> Passo 3 do plano v2. Fonte: `skill sites animados/Animação CONECTA-RUA.mp4`.
> Regenerável a qualquer momento com o comando da seção 6.

## 1. Comando usado

```bash
python extrair_quadros.py \
  --entrada "Animação CONECTA-RUA.mp4" \
  --saida "sites-animados/conecta-rua/quadros" \
  --quadros 157 \
  --qualidade-desktop 70 \
  --qualidade-mobile 65 \
  --res-desktop 1280x720 \
  --res-mobile 720x405 \
  --altura-scroll 590 \
  --filtro "delogo=x=1104:y=650:w=170:h=60" \
  --selecao "not(mod(n,2))+between(n,72,143)"
```

## 2. Resultado e budgets

| Versão | Resolução | Quadros | Qualidade | Tamanho | Meta | Status |
|---|---|---|---|---|---|---|
| Desktop | 1280×720 | 157 | 70 | **5,65 MB** | < 8 MB | ✅ |
| Mobile | 720×405 | 157 | 65 | **2,88 MB** | < 3 MB | ✅ |

- Média por quadro: 37,8 KB (desktop) · 19,2 KB (mobile).
- `manifest.json` com `total_quadros_origem = 241` (corrigido: usa a duração do
  stream, não a do container).
- `altura_scroll_recomendada = 590vh` (override via `--altura-scroll`).

## 3. Amostragem não uniforme

A expressão `select` mantém **12 fps** na maior parte e **24 fps** na cena de
ação (frames originais 72–143 = 3,0–6,0 s), onde acontece o toque no card, o
zoom nas rotas e o pin verde.

| Índices extraídos (0-based) | Frames originais | Tempo coberto | Passo |
|---|---|---|---|
| 0–35 | 0, 2, 4, …, 70 | 0,000 – 2,917 s | 1/12 s |
| 36–107 | 72, 73, …, 143 | 3,000 – 5,958 s | 1/24 s |
| 108–156 | 144, 146, …, 240 | 6,000 – 10,000 s | 1/12 s |

Conversões úteis (índice extraído `i` → frame original `n` → tempo `t`):

```
i ≤ 35   : n = 2i          t = i / 12
36 ≤ i ≤ 107 : n = 72 + (i-36)   t = (i + 36) / 24
i ≥ 108  : n = 144 + 2(i-108)    t = (i - 36) / 12
```

**Consequência:** o progresso de scroll **não** é linear no tempo do vídeo. O
trecho de 3–6 s ocupa 72 dos 157 quadros (46%), então recebe mais scroll.

## 4. Paradas recalibradas (progresso efetivo)

Os centros de pausa foram recalculados no espaço de **progresso efetivo**
(fração do índice de quadro), para cada beat cair na cena certa:

| Parada | Cena | Tempo | Índice | Stop (progresso efetivo) |
|---|---|---|---|---|
| P1 Hero | título + cidade | 0,5 s | 6 | **0,0385** |
| P2 Problema | celular sobe | 1,5 s | 18 | **0,1154** |
| P3 Solução | app de frente | 2,5 s | 30 | **0,1923** |
| P4 Como funciona | toque → zoom → pin | 4,5 s | 72 | **0,4615** |
| P5 Impacto | gota → ondas | 7,5 s | 126 | **0,8077** |
| P6 CTA | fade com ponto de luz | 9,5 s | 150 | **0,9615** |

Parâmetros: `DWELL_PEAK 2.6 · DWELL_WIDTH 0.04 · 590vh · LERP 0.12`.

### Onde a pausa acontece no scroll

Com o remap correto (inversa da integral), a pausa em espaço de scroll fica em
`F(stop)`. Todas desaceleram ~43%:

| Parada | Stop | Posição de scroll da pausa | Velocidade |
|---|---|---|---|
| P1 | 0,0385 | 0,056 | 0,57× |
| P2 | 0,1154 | 0,181 | 0,56× |
| P3 | 0,1923 | 0,307 | 0,57× |
| P4 | 0,4615 | 0,526 | 0,58× |
| P5 | 0,8077 | 0,781 | 0,58× |
| P6 | 0,9615 | 0,945 | 0,58× |

## 5. Janelas de cena para os textos

Em progresso efetivo (mesmo espaço dos stops), para usar nos
`data-show-at` / `data-hide-at` do Passo 5:

| Cena | Tempo | Índices | Janela efetiva |
|---|---|---|---|
| P1 | 0–1 s | 0–12 | 0,000 – 0,077 |
| P2 | 1–2 s | 12–24 | 0,077 – 0,154 |
| P3 | 2–3 s | 24–36 | 0,154 – 0,231 |
| P4 | 3–6 s | 36–108 | 0,231 – 0,692 |
| P5 | 6–9 s | 108–144 | 0,692 – 0,923 |
| P6 | 9–10 s | 144–156 | 0,923 – 1,000 |

> Ajustar com pequenas sobreposições (~0,01) para crossfade entre seções no
> Passo 5.

## 6. Regenerar

```bash
# a partir da raiz do projeto, com ffmpeg no PATH
python "skill sites animados/skill sites animados/scripts/extrair_quadros.py" \
  --entrada "skill sites animados/Animação CONECTA-RUA.mp4" \
  --saida "sites-animados/conecta-rua/quadros" \
  --quadros 157 \
  --qualidade-desktop 70 --qualidade-mobile 65 \
  --res-desktop 1280x720 --res-mobile 720x405 \
  --altura-scroll 590 \
  --filtro "delogo=x=1104:y=650:w=170:h=60" \
  --selecao "not(mod(n,2))+between(n,72,143)"
```

## 7. Requisitos do motor (achado no Passo 3)

O `SKILL.md` manda **inverter** a integral cumulativa no remap, mas o template
`base-single-html.html` retornava a integral direta. Efeito do bug: o vídeo
**acelera** nos pontos de texto em vez de pausar. Além disso, a visibilidade
das paradas usava o progresso bruto, não o efetivo.

Correções obrigatórias no Passo 4:

1. `construirRemap()` devolve `F⁻¹(x)` (busca binária na integral normalizada).
2. `atualizarParadas(efetivo)` — e não `atualizarParadas(p)`.
3. `stops` do template viram placeholder `{{STOPS}}` (por projeto).
4. `inicioAnimado = 0` na Conecta-Rua (poster = frame 0, conforme requisito).
