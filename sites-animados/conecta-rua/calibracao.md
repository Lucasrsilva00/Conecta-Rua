# Calibração — Vídeo × Paradas (Conecta-Rua)

> Gerado no Passo 2 do plano v2. Fonte de verdade para a extração (Passo 3) e
> para os `data-show-at` das seções.

## 1. Vídeo (ffprobe)

| Campo | Valor |
|---|---|
| Arquivo | `skill sites animados/Animação CONECTA-RUA.mp4` |
| Codec | HEVC (h265) |
| Resolução | 1280×720 (16:9) |
| FPS | 24/1 |
| Duração | 10,08 s (formato) / 10,0417 s (stream) |
| Quadros | **241** (`nb_read_frames`) |
| Tamanho | 2,26 MB |
| Áudio | AAC — **ignorado** (site silencioso) |

## 2. Marca d'água — `delogo` calibrado

- Posição observada: canto inferior direito, ~x=1120–1267, y=667–693.
- Filtro aplicado na extração:

```
delogo=x=1104:y=650:w=170:h=60
```

- Teste no frame de 3,5 s: marca removida, sem artefato perceptível
  (fundo escuro da igreja/palmeiras favorece a interpolação).
- **Regra:** `x+w` e `y+h` devem ficar 1 px dentro do quadro
  (por isso 1104+170=1274 < 1280).

## 3. Cenas × paradas de scroll

| Parada | Tempo | Frames | Cena | Conteúdo sobreposto |
|---|---|---|---|---|
| **P1 Hero** | 0,0–1,0 s | 0–23 | Título "CONECTA-RUA" + lema sobre cidade à noite | Título HTML real (`h1`) + barra de stats |
| **P2 Problema** | 1,0–2,0 s | 24–47 | Título esmaece, celular sobe, mapa aparece | "O gargalo é a logística, não a vontade de doar" |
| **P3 Solução** | 2,0–3,0 s | 48–71 | App de frente: "Missões Disponíveis", mapa e card | "Doação em 3 toques" |
| **P4 Como funciona** | 3,0–6,0 s | 72–143 | Dedo toca o card → zoom nas rotas → pin verde central | 3 passos (doador, voluntário, ONG) |
| **P5 Impacto** | 6,0–9,0 s | 144–215 | Gota de cristal → ondas/anéis verdes | "Cada quilo é uma gota que se espalha" |
| **P6 CTA** | 9,0–10,0 s | 216–240 | Fade para preto com ponto de luz | 3 botões: doar, voluntário, ONG |

Centros de pausa (dwell): `0.06 · 0.20 · 0.38 · 0.55 · 0.75 · 0.93`
(PEAK 2.6 · WIDTH 0.04 · altura 590vh · LERP 0.12).

### Decisão do título (duplicação)

- O hero usa **HTML real** (`h1`) para SEO e acessibilidade.
- A cena 0–1 s mantém o título gravado, mas sob **scrim de 0,92**, virando
  textura de fundo (quase invisível).
- O **poster do `prefers-reduced-motion`/noscript é o frame 0** — nele o
  título gravado aparece em tela cheia, servindo de capa estática.

## 4. Textos com erro no vídeo

| Onde | Frames | Texto gravado | Tratamento |
|---|---|---|---|
| Card do app (close) | 72–96 | "Desgãs de Alimentos" | Chip HTML "Doação de Alimentos • 2,5 km • 15 min" |
| Card do app (zoom) | 96–143 | "Desgãs de Alimentos" grande no rodapé | Scrim inferior + chip HTML no rodapé |
| Cabeçalho do app | 48–96 | "Enesanta cdetes pricites e fegd o dVmingo" | Blur localizado (`backdrop-filter`) na janela 48–96 |
| Menu inferior | ~48–72 | "Ranking" (inglês) | Blur sutil na janela; ou ignorar (ilegível em mobile) |

> Os chips são posicionados em % do viewport e só ficam ativos na janela de
> frames correspondente. QA obrigatório em 414×896 e 1920×1080.

## 5. Contraste medido (quadro real)

Região medida: card branco do frame 3,5 s, `crop=470:180:385:470` →
cor média **#C0C3AE** (RGB 192,195,174).

| Cenário | Fundo composto | Razão | Resultado |
|---|---|---|---|
| Scrim 0,90 sobre o card | `#181B1A` | **15,67:1** | AA + AAA |
| Texto dim `#A0B8A8` + scrim 0,90 | `#181B1A` | **8,21:1** | AA + AAA |
| Scrim 0,42 (gradiente fraco) | `#717469` | **4,27:1** | **FALHA AA** |
| Quadro escuro (fade 9,5 s) | `#040005` | > 17:1 | AA + AAA |

**Conclusão:** o scrim lateral **não pode** ser um fade linear até 0 em 55%.
Deve manter **≥ 0,90 de opacidade até 48% da largura** (fim da coluna de texto)
e só então abrir. Pior caso medido (pixel branco puro no frame 109):

```css
--scrim-lateral: linear-gradient(
  90deg,
  rgba(5, 8, 10, 0.95) 0%,
  rgba(5, 8, 10, 0.90) 48%,
  rgba(5, 8, 10, 0) 72%
);
```

Com 0,90 sobre branco: texto 14,63:1 · dim 7,67:1 · accent 8,78:1 (todos AAA).
Relatório completo em `sites-animados/conecta-rua/validacao-contraste.md`.

## 6. Comandos usados

```bash
# Screenshots de calibração
ffmpeg -ss 3.5 -i video.mp4 -frames:v 1 -q:v 2 amostras/cena-3.5.png

# Teste do delogo
ffmpeg -ss 3.5 -i video.mp4 -vf "delogo=x=1104:y=650:w=170:h=60" \
  -frames:v 1 -q:v 2 amostras/teste-delogo.png

# Cor média de uma região (para o checar_contraste.py)
ffmpeg -i cena-3.5.png -vf "crop=470:180:385:470,scale=1:1" \
  -f rawvideo -pix_fmt rgb24 media-card.raw
```
