# Motor Canvas Scroll-Driven — referência técnica

Extraído da skill `sites-animados`. É a parte fixa: o que muda entre sites é
apenas a camada visual (tokens) e o conteúdo (seções).

## 1. Estrutura mínima

```html
<section class="scroll-video" style="height: var(--altura-scroll)">
  <div class="palco">                 <!-- position: sticky; top: 0; height: 100vh -->
    <canvas id="quadro"></canvas>     <!-- aria-hidden="true" -->
    <div class="scrim-lateral"></div>
    <div class="scrim-inferior"></div>
    <div class="vinheta"></div>
    <div class="tint"></div>
    <div class="paradas">             <!-- overlays de texto -->
      <article class="parada" data-show-at="0.06" data-hide-at="0.16">...</article>
      <!-- ... -->
    </div>
  </div>
</section>
```

## 2. Progresso e remap de pausas (dwell)

```js
function progresso() {
  const r = secao.getBoundingClientRect();
  return clamp(-r.top / (r.height - innerHeight), 0, 1);
}
```

A LUT de remap é construída uma vez:

1. Centros de pausa `STOPS` em **progresso efetivo** (fração do índice de
   quadro, 0..1).
2. Para cada posição `y` em 0..1, densidade = `1 + PEAK * Σ exp(-((y-c)/WIDTH)²)`.
3. Integrar a densidade e normalizar para 0..1 → `F(y)` (posição de scroll
   acumulada até o progresso `y`).
4. `remap(x) = F⁻¹(x)` — **inverter** a integral (busca binária na tabela
   monotônica). `remap` leva posição de scroll → progresso efetivo.

> ⚠️ Retornar `F(x)` direto **acelera** o vídeo nos stops (o contrário de
> pausar). A inversa é obrigatória.

Parâmetros da Conecta-Rua: `PEAK = 2.6`, `WIDTH = 0.04`, `N = 2000`.
Mais PEAK = pausa mais dramática; mais WIDTH = pausa mais longa.

**Stops em progresso efetivo** (amostragem não uniforme de 157 quadros):
`0.0385 · 0.1154 · 0.1923 · 0.4615 · 0.8077 · 0.9615`.
Com amostragem uniforme, os stops coincidem com a fração de tempo do vídeo.

## 3. Frame e suavização

```js
const alvo = Math.round(remap(progresso()) * (TOTAL - 1));
atual += (alvo - atual) * LERP;       // LERP 0.09 desktop, 0.12–0.15 mobile
desenhar(Math.round(atual));
```

- `LERP` baixo = animação mais suave/atrasada; alto = mais responsiva.
- Fallback de quadro faltante: desenhar o vizinho mais próximo já carregado.
- Nunca desenhar índice fora de `[0, TOTAL-1]`.
- A visibilidade das paradas usa o **progresso efetivo** (`remap(p)`), não o
  progresso bruto — assim o texto fica ativo exatamente durante a pausa.

## 4. Desenho com cobertura (cover)

```js
const escala = Math.max(canvas.width / img.width, canvas.height / img.height);
const w = img.width * escala, h = img.height * escala;
ctx.drawImage(img, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h);
```

- DPR limitado a 2: `canvas.width = clientWidth * Math.min(devicePixelRatio, 2)`.
- Recriar o canvas em `resize` (debounce 150ms).

## 5. Carregamento progressivo

1. Poster (frame 0) desenhado imediatamente.
2. Frames críticos: índices espaçados (12 pontos) + vizinhos do atual.
3. Resto em lotes de 20 via `requestIdleCallback` (fallback `setTimeout`).
4. Loader com % real = bytes recebidos / total do manifest.
5. `navigator.connection.saveData` ou `effectiveType` lento → versão mobile e
   menos frames.

## 6. Loop único

Um só `requestAnimationFrame` faz tudo por frame:

```
progresso → remap → alvo → lerp → desenhar
         → visibilidade das paradas (data-show-at/hide-at)
         → marcadores laterais
         → tint da seção
```

Evite observers ou listeners que disparem desenho fora desse loop.

## 7. Acessibilidade

- Canvas `aria-hidden="true"`; o texto é DOM real.
- `prefers-reduced-motion`: não carregar frames; poster + seções em fluxo
  normal (sem pinning) + CTAs reais.
- Botão "Modo leitura (sem animação)" com a mesma alternativa.
- `<noscript>`: poster + seções estáticas.
- Transcrição completa em `<details>`.

## 8. Checklist de performance

- [ ] Só `transform` e `opacity` animados nos overlays.
- [ ] DPR ≤ 2; partículas ≤ 28 desktop / 12 mobile.
- [ ] Cache LRU de ~24 bitmaps decodificados (`createImageBitmap`).
- [ ] Primeiro quadro em < 1s; LCP = poster.
- [ ] 60fps em aparelho médio; se cair, cortar partículas antes dos frames.

## 9. Landing em DOM depois da intro

Quando o vídeo é só a abertura, a intro termina na última parada e o restante
do site é DOM normal. Não estique o canvas pelo site inteiro.

**Revelação reversível (blocos e letras):**

```js
// p = 0..1 conforme o bloco sobe; voltar o scroll reduz p e desfaz.
let p = (innerHeight * 0.94 - el.getBoundingClientRect().top) / (innerHeight * 0.4);

// A seção inteira precisa terminar antes do usuário parar com ela no topo.
// Sem isto, o último item de uma lista longa fica apagado.
const rs = el.closest('.secao').getBoundingClientRect();
p = Math.max(p, (innerHeight * 0.9 - rs.top) / (innerHeight * 0.35));
```

- Escreva `p` em `--p` no elemento e use `opacity: var(--p)` +
  `translateY(calc((1 - var(--p)) * 30px))`. Sem transição CSS: o rAF já
  interpola e a reversão fica imediata.
- Letras: quebre o texto em `.palavra > .letra`, com `--d` progressivo
  (0..0.45). `--lp: clamp(0, calc((var(--p) - var(--d)) * 3.2), 1)`.
  Preserve elementos internos (`<span class="destaque">`) percorrendo nós de
  texto recursivamente.
- Acessibilidade: guarde o texto original em `aria-label` antes de quebrar;
  leitores de tela não devem ler letra por letra.
- `prefers-reduced-motion`: force `--p: 1`, letras sem transform e blocos
  visíveis. A intro vira poster + paradas em fluxo normal.
- Atualize a revelação em um `scroll` com `requestAnimationFrame` (throttle),
  separado do loop do canvas. O loop do canvas pode parar quando o LERP
  assenta; não deixe um rAF eterno só para revelar DOM.
