# Assets, autoria e licenciamento

Auditoria em 2026-11-25. Nenhum código ou geometria foi copiado do repositório de referência visual. Os cinco gráficos dos produtos, o desenho de cofre, os cubos, as linhas financeiras, o grafo, a esfera neural, os elementos de interface e os monogramas `in`/`LK` foram desenhados nesta implementação. Os ícones genéricos e C# já recuperados de `scripts/icons.py` também são geometria autoral.

## Fontes recuperadas

- Inter: Inter Project Authors, [repositório oficial](https://github.com/rsms/inter), SIL Open Font License 1.1. Texto preservado em `assets/fonts/LICENSE-Inter.txt`.
- JetBrains Mono: JetBrains Mono Project Authors, [repositório oficial](https://github.com/JetBrains/JetBrainsMono), SIL Open Font License 1.1. Texto preservado em `assets/fonts/LICENSE-JetBrainsMono.txt`.
- Os WOFF2 são subsetados localmente para os caracteres efetivamente usados. Os arquivos de licença acompanham os originais. Não há busca de fontes em servidores externos em tempo de exibição; fallbacks de sistema permanecem configurados.

## Ícones por arquivo

A coleção [Simple Icons](https://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md) distribui sua geometria sob CC0 1.0, preservada em `assets/icons/LICENSE-simple-icons.md`. Isso não elimina direitos de marca nem substitui licenças indicadas para a arte original. A origem individual foi consultada nos metadados oficiais de [13.21.0](https://github.com/simple-icons/simple-icons/blob/13.21.0/_data/simple-icons.json), que ainda inclui CSS3. Essa versão é uma referência de metadados; a versão originalmente usada pelo Claude não pôde ser comprovada. Hashes dos arquivos locais e os metadados correspondentes estão em `docs/icon-provenance.json`.

| Arquivo | Origem individual | Resultado da auditoria |
|---|---|---|
| `typescript.svg` | [TypeScript branding](https://www.typescriptlang.org/branding/) | CC0 da coleção; página oficial permite variante de uma cor e proíbe sugerir endosso |
| `javascript.svg` | [logo.js, Christopher Williams](https://github.com/voodootikigod/logo.js) | Arte original MIT; copyright e texto MIT preservados em `assets/icons/LICENSE-javascript-MIT.txt` |
| `python.svg` | [Python Software Foundation](https://www.python.org/community/logos/) | CC0 da coleção; marca da PSF, uso para indicar implementação/compatibilidade descrito na página oficial |
| `react.svg` | [Facebook create-react-app, logo.svg](https://github.com/facebook/create-react-app/blob/282c03f9525fdf8061ffa1ec50dce89296d916bd/test/fixtures/relative-paths/src/logo.svg) | CC0 da coleção; metadados não indicam outra licença individual |
| `html5.svg` | [W3C HTML5 logo](https://www.w3.org/html/logo/) | Arte original W3C sob CC-BY-3.0; atribuição abaixo |
| `css3.svg` | [W3C HTML5 identity system](https://www.w3.org/html/logo/) | CC0 da coleção; fonte é o sistema visual W3C, tratado com atribuição CC-BY-3.0 abaixo |
| `nodedotjs.svg` | [Node.js branding](https://nodejs.org/en/about/branding) | CC0 da coleção; diretrizes da marca separadas |
| `fastapi.svg` | [FastAPI, icon-white.svg](https://github.com/tiangolo/fastapi/blob/ffb4f77a11f83132b521ba0aac6c95792c19e797/docs/en/docs/img/icon-white.svg) | CC0 da coleção; metadados não indicam outra licença individual |
| `mysql.svg` | [MySQL logo policy](https://www.mysql.com/about/legal/logos.html) | CC0 da coleção; política da marca separada |
| `postgresql.svg` | [PostgreSQL logo](https://wiki.postgresql.org/wiki/Logo) | CC0 da coleção; política da marca separada |
| `git.svg` | [Git logos](https://git-scm.com/community/logos) | Arte original de Jason Long sob CC-BY-3.0; atribuição abaixo |
| `github.svg` | [GitHub logos](https://github.com/logos) | CC0 da coleção; diretrizes da marca separadas |
| `docker.svg` | [Docker media resources](https://www.docker.com/company/newsroom/media-resources/) | CC0 da coleção; diretrizes da marca separadas |

Git Logo por **Jason Long**, disponibilizado pelo projeto Git sob [Creative Commons Attribution 3.0 Unported](https://creativecommons.org/licenses/by/3.0/). HTML5/CSS3 identity system por **W3C**, disponibilizado sob [Creative Commons Attribution 3.0](https://creativecommons.org/licenses/by/3.0/). Nesta implementação essas artes aparecem em geometria vetorial adaptada pela coleção Simple Icons, em escala menor e cor monocromática. Nenhum endosso é declarado. Atribuições também aparecem na descrição acessível do SVG de stack.

## Retrato

`assets/portrait/source.jpg` foi atualizada na V1.1 a partir do avatar público de LukasAlexandre. Requisições sem cache com tamanhos 2048 e 4096 retornaram os mesmos bytes e resolução 460×460. URL, data, hash atual e hash anterior estão em `docs/portrait-source.json`. A imagem foi convertida em caracteres reais com o pipeline recuperado, agora ajustado para preservar a mão, corrente e enquadramento completo. Não é uma imagem gerada por IA. A fotografia não recebe uma licença inventada.

## Limitações verificáveis

Os quatro badges de achievements usados **somente na simulação lateral da preview** foram coletados dos URLs públicos do próprio GitHub, correspondendo aos achievements do perfil. Origem e data em `docs/profile-public.json`, arquivos em `preview/achievements/`. São artes do GitHub; não se declara licença autoral própria ou permissão geral de reutilização para essas marcas. Não integram os SVGs de conteúdo do README.

Os arquivos locais das fontes e a geometria dos ícones foram preservados. A licença original da coleção e o MIT adicional foram mantidos no repositório. A consulta aos metadados individuais não é uma declaração de que todas as marcas possuem uma licença independente permissiva; entradas sem campo `license` estão descritas como tal. Revisão da plataforma GitHub real permanece pendente, pois nada foi publicado.
