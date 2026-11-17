# Conecta-Rua — site animado

Landing de página única da Rede Conecta-Rua (Camaçari, BA), com intro
dirigida por scroll e landing em DOM. Tudo em português, tema escuro,
verde + laranja, contraste WCAG AA/AAA.

## Como abrir

```bash
# na raiz do projeto
python -m http.server 8765
# abra http://127.0.0.1:8765/sites-animados/conecta-rua/
```

Também funciona abrindo `index.html` direto, mas o servidor local garante
o carregamento dos quadros e das fontes sem restrições do navegador.

## Arquitetura

| Parte | O que é | Onde |
|---|---|---|
| 1 | Intro em canvas, `position: sticky`, **480vh**, 6 paradas | `#inicio` |
| 2 | Landing em DOM com 8 seções e rodapé | `#impacto` … `footer` |

- **Intro:** 157 quadros WebP (desktop 1280×720 / mobile 720×405), `LERP 0.12`,
  `DWELL_PEAK 2.6`, `DWELL_WIDTH 0.04`. O remap usa `F⁻¹` e as paradas são
  avaliadas no progresso efetivo (fração do índice de quadro).
- **Stops:** `0,0385 · 0,1154 · 0,1923 · 0,4615 · 0,8077 · 0,9615`.
- **Seções:** impacto, três perfis, missões ao vivo, classificação semanal,
  EcoPontos, Painel de Gestão, login Google/WhatsApp e rodapé.
- **Imagens de seção:** reutilizam quadros já carregados pela intro
  (`frame-0006`, `0090`, `0105`, `0120`), sem bytes extras de arte.

## Revelação reversível

Cada bloco `[data-reveal]` recebe uma variável CSS `--p` (0–1) calculada por
scroll. Títulos `[data-letras]` são quebrados em letras com atraso
progressivo (`--d`). Descendo, letras e blocos aparecem; subindo, a opacidade
e o deslocamento voltam gradualmente. A seção inteira termina de revelar
quando o topo dela chega a 55% da tela — assim o último item nunca fica
apagado.

## Acessibilidade e desempenho

- `prefers-reduced-motion`: poster estático (frame 0), sem sticky, sem
  animação de letras; todas as seções em fluxo normal e visíveis.
- Foco visível, skip link, navegação por âncoras, `aria-current` nas paradas,
  títulos com `aria-label` após a quebra em letras.
- Cursor nativo; sem partículas ou efeitos pesados.
- Contraste: scrim lateral 0,95/0,90 até 48%; scrim vertical no mobile.
  Botão sólido `#C2410C` com branco = 5,4:1.
- Orçamento de quadros: **6,59 MB** desktop (< 8 MB) e **2,97 MB** mobile
  (< 3 MB). Qualidade WebP elevada para 78 (desktop) e 68 (mobile), mantendo
  a resolução nativa 720p do vídeo-fonte (HEVC 1280×720, 24 fps).

## Defeitos do vídeo tratados

- Marca d'água "Dola AI" removida na extração com
  `delogo=x=1104:y=650:w=170:h=60`.
- Título "CONECTA RUA" gravado no vídeo fica sob véu local na parada 1
  (ativa até efetivo 0,074); o `h1` real em HTML é a informação principal.
- O typo "Desgãs de Alimentos" do vídeo é corrigido com patch local
  (fundo amostrado do próprio quadro, texto alinhado à linha de base da
  palavra original, compressão horizontal) na janela do zoom
  (`efetivo 0,32–0,56`), sem afetar o restante da animação.

## QA executado

- 6 paradas mapeadas corretamente (0→5) nas posições de scroll documentadas.
- Nenhum erro de console ou requisição; sem overflow horizontal em 414 px.
- `prefers-reduced-motion` validado: poster, paradas visíveis, loader oculto.
- Imagens de seção carregadas (`naturalWidth > 0`) e sem termos proibidos
  ("Rank", "ESG", "Dashboard", "Terminal") no texto visível.

## Regenerar quadros

Ver `extracao.md` (comando completo, seleção não uniforme, stops e mapa
frame↔tempo). O manifest fica em `quadros/manifest.json`.
