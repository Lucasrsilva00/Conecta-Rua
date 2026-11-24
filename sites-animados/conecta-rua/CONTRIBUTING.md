# Contribuindo com o Conecta-Rua

## Branches
- `main`: versão estável e publicada (Vercel).
- `develop`: integração de funcionalidades.
- `feature/<nome>`: novas funcionalidades.
- `fix/<nome>`: correções.
- `refactor/<nome>`: refatorações.
- `docs/<nome>`: documentação.

## Commits
Padrão Conventional Commits: `feat:`, `fix:`, `refactor:`, `perf:`, `style:`, `docs:`, `test:`, `chore:`.

## Fluxo
1. Crie uma branch a partir de `develop`.
2. Faça commits pequenos e objetivos.
3. Abra um Pull Request para `develop`.
4. Após revisão e testes, merge para `develop`.
5. Periodicamente, merge `develop` → `main`.

## Testes manuais
- Abrir o site em `http://127.0.0.1:8765/sites-animados/conecta-rua/`.
- Validar console sem erros.
- Validar scroll (entrada, revelação, destaque, fim, reverso).
- Validar mapa (mapa/satélite, centralização no SENAI, marcadores).
- Validar responsividade (desktop, tablet, mobile) e `prefers-reduced-motion`.

## Segurança
- Não commitar `.env`, tokens ou chaves.
- Não force push em `main`.
- Preservar a identidade visual e as animações cinematográficas.