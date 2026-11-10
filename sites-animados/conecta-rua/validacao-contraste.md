# Validação de Contraste — Scrims sobre o Canvas

> Passo 2.5 do plano v2. Método: varrer os 241 frames, achar o mais claro e o
> mais escuro, medir a coluna onde o texto fica e testar média + pior caso.

## 1. Quadros extremos (varredura dos 241 frames)

| | Frame | Tempo | YAVG |
|---|---|---|---|
| **Mais claro** | 109 | 4,54 s | **107,1** |
| **Mais escuro** | 240 | 10,00 s | **14,5** |

Amostras auxiliares: 3,5 s = 90,0 · 5,0 s = 89,7 · 2,5 s = 56,3 · 0,5 s = 49,5.

## 2. Média por faixa da coluna de texto (frame 109)

Coluna de texto: `left 6%` (x=77) + `max-width 520px` → ocupa até x=597 (46,6%).

| Faixa | Cor média | Opacidade do scrim no centro | Fundo composto | Texto #EAF6EE | Dim #A0B8A8 | Accent #34D97B |
|---|---|---|---|---|---|---|
| 0–10% | #1E2317 | 0,9325 | #070A0B | 17,91:1 | 9,39:1 | 10,75:1 |
| 10–20% | #33372F | 0,9175 | #090C0D | 17,69:1 | 9,27:1 | 10,62:1 |
| 20–30% | #777477 | 0,9025 | #101315 | 16,85:1 | 8,83:1 | 10,12:1 |
| 30–40% | #808169 | 0,8875 | #131615 | 16,45:1 | 8,62:1 | 9,88:1 |
| 40–55% | #94A27F | 0,6260 | #3A4236 | 9,43:1 | 4,94:1 | 5,66:1 |
| Hero (centro) | #424E36 | 0,92 | #0A0E0E | 17,52:1 | 9,19:1 | 10,52:1 |
| Frame 240 | #040005 | 0 | #040005 | 18,78:1 | 9,84:1 | 11,27:1 |

**Todas as médias passam AA.** Mas média não é garantia: o mapa tem ruas e
pins brancos.

## 3. Pior caso (pixels reais da coluna de texto)

Crop `520×720` em x=77 do frame 109 (374.400 pixels):

| Métrica | Valor |
|---|---|
| Luminância p95 | 0,773 |
| Luminância p99 | 0,830 |
| **Pixel mais claro** | **#FFFFFF (255,255,255)** |

Com o scrim antigo (0,657 no fim da coluna), o branco puro derruba:

| Cor | Fundo composto | Razão | AA |
|---|---|---|---|
| #EAF6EE | #5B5D5E | 5,99:1 | ✅ |
| #A0B8A8 | #5B5D5E | 3,14:1 | ❌ |
| #34D97B | #5B5D5E | 3,59:1 | ❌ |
| #F97316 (grande) | #5B5D5E | 2,37:1 | ❌ |

## 4. Correção obrigatória do scrim

Manter **opacidade ≥ 0,90 em toda a coluna de texto (até 48%)** e só então abrir:

```css
--scrim-lateral: linear-gradient(
  90deg,
  rgba(5, 8, 10, 0.95) 0%,
  rgba(5, 8, 10, 0.90) 48%,
  rgba(5, 8, 10, 0) 72%
);
```

Validação sobre **branco puro** com 0,90:

| Cor | Razão | Resultado |
|---|---|---|
| #EAF6EE | 14,63:1 | AAA ✅ |
| #A0B8A8 | 7,67:1 | AAA ✅ |
| #34D97B | 8,78:1 | AAA ✅ |
| #F97316 (grande) | 5,79:1 | AA ✅ |

## 5. Regras derivadas

1. **Nunca** usar gradiente que chegue a 0 dentro da coluna de texto.
2. Chips de correção de texto têm fundo próprio (`--surface`), então não
   dependem do scrim.
3. O botão sólido usa `--accent-cta #C2410C` com branco (5,18:1 AA) —
   independente do vídeo.
4. Texto `dim` só é permitido dentro da coluna de texto (x ≤ 48%); à direita,
   usar apenas texto principal sobre painel.
5. Revalidar com `checar_contraste.py` sempre que o scrim ou a paleta mudarem.
