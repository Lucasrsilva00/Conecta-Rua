# Marca — Rede Conecta-Rua

> Referência de marca da skill `sites-animados` v2.
> Use quando o projeto for da Conecta-Rua ou quando o usuário citar
> "Conecta-Rua", "economia circular", "Camaçari" ou "combate à fome".

## Identidade

- **Nome:** Rede Conecta-Rua
- **Local:** Camaçari, Bahia
- **Propósito:** conectar excedentes de feiras e hortifrútis a ONGs,
  cozinhas comunitárias e pessoas em vulnerabilidade.
- **Mensagem central:** "O alimento que sobra na feira vira refeição na mesa."
- **Tom de voz:** comunitário, transparente, acolhedor e objetivo.
  Frases curtas. Só português — sem termos em inglês na interface.
- **Público:** feirantes/comerciantes (30–65 anos, sol forte, mãos ocupadas)
  e ONGs/lideranças comunitárias (25–55 anos).

## Tokens (direção Neon Noir adaptada — vídeo noturno)

```css
:root {
  --bg:          #05080a;
  --surface:     #0d1218;
  --text:        #EAF6EE;
  --text-dim:    #A0B8A8;
  --muted:       #5A6B60;
  --line:        #1C2B24;
  --accent:      #34D97B;   /* verde neon */
  --accent-2:    #F97316;   /* laranja das rotas */
  --accent-cta:  #C2410C;   /* botão sólido (branco = 5.4:1) */
  --accent-glow: rgba(52, 217, 123, 0.35);
  --heading: 'Inter', 'Roboto', system-ui, sans-serif;
  --body:    'Inter', 'Roboto', system-ui, sans-serif;
  --raio-card: 12px;
  --raio-botao: 16px;
  --altura-scroll: 590vh;
  --dwell-peak: 2.6;
  --dwell-width: 0.04;
  --lerp: 0.12;
}
```

## Regras de contraste

- Texto normal: mínimo **4.5:1**; texto grande: mínimo **3:1**.
- `#F97316` só como fundo de borda/ícone ou **texto grande** (>= 18.66px bold).
- Botão sólido usa `#C2410C` (branco em cima = 5.4:1 AA).
- Validar sempre com `scripts/checar_contraste.py` contra o quadro **mais claro**
  (celular aceso) e o **mais escuro** (gota / fade final).

### Scrim lateral calibrado (medido no vídeo real)

O fade linear até 0 em 55% **falha** (4,27:1) sobre o card branco do app, e o
pior caso (pixel branco puro na coluna de texto) derruba dim/accent. Manter
opacidade ≥ 0,90 até 48% da largura:

```css
--scrim-lateral: linear-gradient(
  90deg,
  rgba(5, 8, 10, 0.95) 0%,
  rgba(5, 8, 10, 0.90) 48%,
  rgba(5, 8, 10, 0) 72%
);
```

Medições: scrim 0,90 sobre `#C0C3AE` → `#181B1A` = **15,67:1** (AAA).
Texto dim `#A0B8A8` → **8,21:1** (AAA). Sobre branco puro: texto 14,63:1,
dim 7,67:1, accent 8,78:1 (AAA); laranja grande 5,79:1 (AA).

## Eixos visuais

| Eixo | Valor |
|------|-------|
| Luminosidade | escuro (`#05080a`) |
| Textura | grão 1.5% + partículas verdes lentas (12 mobile / 28 desktop) |
| Cards | superfície escura + borda 1px gradiente verde → laranja |
| Cantos | 12px |
| Tipografia | Inter 800 em caixa alta nos títulos, 400 no corpo |
| Alinhamento | esquerda, alternando nas paradas 4 e 5 |
| Entrada | opacidade 160ms + translateY(12px) |
| Ritmo | DWELL_PEAK 2.6 · DWELL_WIDTH 0.04 · 590vh |
| Cursor | nativo, sem efeitos |

## Paradas obrigatórias do site

| # | Seção | Stop (progresso efetivo) | Janela de cena |
|---|---|---|---|
| 1 | Hero — lema + barra de stats | 0,0385 | 0,000–0,077 |
| 2 | O Problema — logística, não falta de doadores | 0,1154 | 0,077–0,154 |
| 3 | A Solução — cadastro em 3 toques | 0,1923 | 0,154–0,231 |
| 4 | Como Funciona — 3 passos (doador, voluntário, ONG) | 0,4615 | 0,231–0,692 |
| 5 | Impacto — rastreio, refeições, relatório | 0,8077 | 0,692–0,923 |
| 6 | CTA final — Quero doar · Quero ser voluntário · Sou ONG | 0,9615 | 0,923–1,000 |

> Stops em progresso efetivo (fração do índice de quadro), calibrados para a
> amostragem não uniforme de 157 quadros. Ver `extracao.md` do projeto.

## Restrições

- Vídeo tem marca d'água "Dola AI" no canto inferior direito: aplicar
  `delogo=x=1104:y=650:w=170:h=60` na extração (ver SKILL.md, Passo 3).
- Textos gravados no vídeo têm erros de português ("Desgãs de Alimentos"):
  cobrir com chip HTML correto ou desfocar na janela de frames indicada.
- Título "CONECTA-RUA" gravado no vídeo: o hero usa HTML real (`h1`) por SEO e
  acessibilidade. A animação começa no **frame 0** (poster), com o título
  gravado sob scrim de 0,95 — vira textura de fundo. O frame 0 é também o
  poster do `prefers-reduced-motion`/noscript.
- `prefers-reduced-motion`: poster estático (frame 0) + seções em fluxo normal.
