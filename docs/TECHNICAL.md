# Desenvolvimento local

Python 3.12+. O projeto continua a branch `redesign/engineering-intelligence-v1`; nada foi publicado.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/build.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
.\.venv\Scripts\python.exe scripts/serve_preview.py
```

Para atualizar a coleta pública: `python scripts/build.py --refresh`. A execução normal é offline e determinística para o mesmo cache e configuração. O coletor não consulta nomes de repositórios privados. Detalhes do intervalo e das métricas em `DATA_SOURCES.md`.

Para converter novamente a fotografia real: instale `requirements-portrait.txt`, depois execute `python scripts/generate_ascii.py --columns 112`. Esse pipeline usa OpenCV, NumPy e Pillow somente localmente. O workflow diário utiliza o ASCII já versionado.

As cores, famílias tipográficas, medidas e parâmetros de movimento estão em `config/design-tokens.json`. Identidade e conexões estão em `config/profile.json`; produtos públicos em `config/projects.json`. Uma URL só é vinculada pelo README quando estiver explicitamente marcada como verificada. SVGs são auto-contidos, sem scripts, raster interno, fontes externas ou eventos. A fotografia aparece somente na coluna lateral da preview; o hero usa caracteres vetoriais reais.

O README utiliza `<picture>`, `<source>`, imagens de largura percentual e links HTML permitidos no GitHub. As mesmas imagens e o mesmo fragmento do README são usados na preview. O JavaScript da preview controla apenas a simulação de tema e a inserção do fragmento; não faz parte dos componentes publicáveis.

CSS animado está contido em cada SVG; o estado base final é legível quando animações não são executadas. `prefers-reduced-motion` desativa movimento. A composição tem fontes locais incorporadas em WOFF2 com fallbacks do sistema. O cache de imagens e a sanitização do GitHub real ainda exigem homologação posterior à autorização para publicação; nenhum teste local equivale a esse teste remoto.

## Workflow preparado

`.github/workflows/main.yml` será executável somente após futura publicação autorizada. Agenda diária e dispatch manual, sem gatilho push, concorrência serializada, timeout, dependências fixas e actions presas por SHA. O job lê o calendário público, usa o cache válido versionado se a rede falhar, regenera e valida antes de qualquer commit automatizado. O único caminho de escrita remota futura é o commit dos dados/arte gerada na própria referência da execução. Nenhuma execução remota foi realizada nesta entrega.

## Referências consultadas

- [Artigo técnico de Avi Vashishta](https://www.avivashishta.com/blog/build-animated-github-profile-readme): referência de arquitetura em contexto de imagem, não código reutilizado.
- [Repositório de referência](https://github.com/AVIVASHISHTA29/AVIVASHISHTA29): em 2026-11-25, API pública com `license: null`, raiz sem arquivo de licença; decisão autoral mantida.
- [Segurança de GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use).
- [Gatilhos e prevenção de recursão](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
