# Changelog — Conecta-Rua

Histórico de alterações do projeto. As entradas anteriores à criação deste arquivo foram reconstruídas a partir da auditoria atual do repositório (não há commits datados anteriores a 2026-11).

## [Não lançado]

### Adicionado
- Mapa global interativo (Leaflet + OpenStreetMap) centralizado no SENAI de Camaçari, com modo satélite (Esri World Imagery), marcadores de missões, botão "Centralizar no SENAI" e seletor Mapa/Satélite.
- Logo oficial circular na navbar (substituição do ponto verde), 44px, `border-radius: 50%`, `object-fit: contain`.
- Preconnect para fontes, CDN do Leaflet e servidores de tiles; lazy loading da logo e inicialização sob demanda do mapa.

### Corrigido
- Overlay de correção do typo "Desgãs" do vídeo: fundo amostrado do próprio quadro, alinhamento pela linha de base real, compressão horizontal, fade apenas do texto (fundo opaco).
- Ocultação do overlay via IntersectionObserver fora da intro.

### Alterado
- README.md atualizado (descrição do patch do typo).

## [2026-11] — Histórico retrospectivo (identificado na auditoria)

- `feat`: refinar ranking, brilho de títulos e animações textuais (`ecbc055`).
- `feat`: adicionar navegação lateral, carrossel de missões e animação de contagem (`cb15f04`).
- `feat`: elevar qualidade WebP dos quadros (78 desktop, 68 mobile) (`a3fc6ca`).
- `fix`: corrigir legenda flutuante de correção do typo durante scroll (`357d328`).
- `fix`: eliminar sobreposição da legenda de correção do typo (`6ccfea3`).
- `fix`: garantir ocultação do overlay de correção via IntersectionObserver (`14ca3ae`).
- `fix`: corrigir definitivamente overlay de correção do typo (`6b817e9`).
- `feat`: adicionar modo satélite e centro operacional SENAI no mapa (`f3ce5d3`).
- `feat`: substituir ponto verde da navbar pela logo oficial (`52a6a7f`).
- `refine`: logo circular perfeita na navbar (`42bb6fe`).
- `perf`: preconnect e lazy loading (`1ee7679`).
- `fix`: corrigir caminho da logo para deploy e adicionar img ao projeto (`fd8d227`).
- `feat`: adicionar modo satélite e centro operacional SENAI no mapa global (`f3ce5d3`).

---

*Entradas anteriores são retrospectivas: identificadas na auditoria atual, não necessariamente registradas no GitHub na época.*