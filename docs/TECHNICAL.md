# Desenvolvimento local

Python 3.12+. A V1.2 foi publicada na main. A V1.3 trabalha em `fix/production-parity-v1.3`, sem merge nem nova publicacao. Consulte `PRODUCTION_PARITY_RCA.md`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/build.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
.\.venv\Scripts\python.exe scripts/serve_preview.py
```

Para atualizar a coleta pública: `python scripts/build.py --refresh`. A execução normal é offline e determinística para o mesmo cache e configuração. O coletor não consulta nomes de repositórios privados. Detalhes do intervalo e das métricas em `DATA_SOURCES.md`.

Na V1.2, o Hero foi redesenhado sem retrato. O gerador ASCII, seu arquivo de caracteres e o manifesto de dependências exclusivo foram removidos. NumPy/OpenCV não são necessários nem estão no ambiente isolado atual. A fotografia é compartilhada pela sidebar e permanece preservada. Pillow consta somente em `requirements-media.txt`, opcional para exportação/análise de mídia offline; não é dependência do build diário.

O Bento Grid usa `layout.rows` e `layout.featured` em `config/projects.json`: ETHAN/VORCEN na primeira linha, GIDACE/INORYX/Vaultify na segunda. As dimensões estão nos tokens `ecosystem`; cada card tem variantes desktop/mobile e estáticas. ETHAN usa mídia pré-renderizada do renderer original; os demais continuam SVGs. `render_ecosystem.py` valida a presença dos assets ETHAN e remove somente SVGs `project-*.svg` obsoletos dentro de `generated/{theme}`. Não reconstrói nem acessa o projeto privado durante o build. Histórico anterior permanece preservado no Git.

As cores, famílias tipográficas, medidas e parâmetros de movimento estão em `config/design-tokens.json`. Identidade e conexões estão em `config/profile.json`; produtos públicos em `config/projects.json`. Uma URL só é vinculada pelo README quando estiver explicitamente marcada como verificada. SVGs são auto-contidos, sem scripts, fontes externas ou eventos. A V1.3 adiciona wrappers SVG do raster ETHAN com data URIs estritamente validadas contra os bytes do export original. A fotografia aparece somente na coluna lateral da preview; o Hero contém identidade e código, sem fotografia ou ASCII.

O card ETHAN seleciona WebP animado, com fallback GIF pelo tipo de mídia, e PNG para movimento reduzido. A animação já inclui fundo, bordas e tipografia do card; usa wrappers SVG adaptativos nas variantes mobile e estaticas, sem canvas, WebGL ou JavaScript no README. O ambiente de exportação original fica fora deste repositório e não é publicado. Somente a mídia visual final é versionada; o pipeline diário é offline/determinístico e verifica os arquivos existentes. Detalhes, formato, tamanho e limitações em `REFINEMENT_V1_2.md` e `ethan-export.json`.

O README utiliza `<picture>`, `<source>`, imagens de largura percentual e links HTML permitidos no GitHub. As mesmas imagens e o mesmo fragmento do README são usados na preview. O JavaScript da preview controla apenas a simulação de tema e a inserção do fragmento; não faz parte dos componentes publicáveis.

CSS animado está contido em cada SVG; o estado base final é legível quando animações não são executadas. `prefers-reduced-motion` desativa movimento. A composição tem fontes locais incorporadas em WOFF2 com fallbacks do sistema. O cache de imagens e a sanitização do GitHub real ainda exigem homologação posterior à autorização para publicação; nenhum teste local equivale a esse teste remoto.

## Workflow preparado

`.github/workflows/main.yml` esta ativo na main desde a V1.2. Nenhum workflow foi disparado para a V1.3. Agenda diária e dispatch manual, sem gatilho push, concorrência serializada, timeout, dependências fixas e actions presas por SHA. O job lê o calendário público, usa o cache válido versionado se a rede falhar, regenera e valida antes de qualquer commit automatizado. O único caminho de escrita remota futura é o commit dos dados/arte gerada na própria referência da execução. Nenhuma execução remota foi realizada nesta entrega.

## Referências consultadas

- [Artigo técnico de Avi Vashishta](https://www.avivashishta.com/blog/build-animated-github-profile-readme): referência de arquitetura em contexto de imagem, não código reutilizado.
- [Repositório de referência](https://github.com/AVIVASHISHTA29/AVIVASHISHTA29): em 2026-11-25, API pública com `license: null`, raiz sem arquivo de licença; decisão autoral mantida.
- [Segurança de GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use).
- [Gatilhos e prevenção de recursão](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## V1.3 production parity

Sources com largura/movimento usam `generated/adaptive/` sem consulta de tema no media externo. Vetores preservam geometria e animacoes originais; variaveis CSS internas fazem a troca exata de paleta. Wrappers ETHAN incorporam somente os bytes dos assets originais, com WebP/GIF/PNG. O gerador valida esses bytes e rejeita referencias externas. Preview: `?theme=dark&mode=parity` (padrao) reproduz a reescrita integral de media do GitHub; `mode=design` preserva as condicoes compostas para comparacao. `npm run test:theme` compara pixels entre adaptativos e originais em tema oposto ao sistema. Veja RCA para evidencias, limites e rollout.
