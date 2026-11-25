# Validação local

Preview: `http://localhost:8765/preview/`.

O shell reproduz o cabeçalho, navegação, coluna lateral e container README do GitHub. O conteúdo é o fragmento gerado a partir do README, com os mesmos arquivos SVG em elementos `img`/`picture`. O JavaScript local seleciona o tema da preview; não participa das animações dos componentes.

Informações laterais verificadas no perfil público: 23 repositórios públicos, 4 seguidores, 3 seguindo, localização `Itapeva - MG` e achievements Pair Extraordinaire, Quickdraw, Pull Shark e YOLO. As imagens dos achievements estão salvas localmente; procedência e data da coleta em `docs/profile-public.json`. Nenhum achievement ou contador foi inventado.

## Execução

```powershell
.venv\Scripts\python.exe scripts\build.py
.venv\Scripts\python.exe scripts\serve_preview.py --port 8765
node tests\visual\capture.cjs <diretorio-de-evidencias>
node tests\visual\animation.cjs <diretorio-de-evidencias>
node tests\visual\reduced-selection.cjs <diretorio-de-evidencias>
```

O Node requer o pacote `playwright` e seu Chromium instalado. É possível usar `NODE_PATH` apontando para o diretório `node_modules` do runtime empacotado do Codex.

O harness captura screenshots completas em dark e light em 1920×1080, 1440×900, 1280×720, 768×1024, 390×844 e 375×812. Verifica decodificação das imagens, textos alternativos, erros HTTP/JavaScript, seleção dos SVGs por tema, overflow e largura do artigo. Abre ainda cada SVG separadamente para verificar XML, título/descrição, animações CSS e preferência de movimento reduzido. Registra medições locais de carregamento, sem converter essas medições em alegações sobre performance no GitHub remoto.

`animation.cjs` compara pixels de screenshots dos elementos `img` reais do README em dois instantes separados por 4 segundos. Exige mudança de pixels no hero, activity e VORCEN normais e estabilidade completa quando o navegador prefere movimento reduzido. `reduced-selection.cjs` verifica a seleção efetiva das alternativas `-static.svg` nos dois temas, em desktop e mobile.

## Correções observadas durante a validação

- Chromium pode postergar animações de SVGs fora da viewport. O harness visita o activity e rola o README antes da screenshot completa, permitindo registrar conteúdo concluído, em vez de falsos espaços vazios de quadros iniciais.
- A emulação de `prefers-reduced-motion` no documento principal não se propagou consistentemente ao CSS interno dos SVGs carregados em `img`, embora funcionasse ao abrir o SVG diretamente. Isso motivou a implementação de arquivos SVG estáticos e fontes de `picture` com a preferência de movimento reduzido no próprio README.
- VORCEN recebeu uma linha de base estática e um traço progressivo reforçado depois da primeira inspeção visual.

## Limites

- O concept aprovado não está entre os anexos disponíveis; comparação visual com essa imagem pendente.
- Nenhuma publicação, GitHub Camo ou execução remota foi realizada. O comportamento na plataforma real ainda precisa de homologação depois de autorização para publicar.
- O shell é uma aproximação local do GitHub, não uma cópia integral de seus serviços. Não há busca, follow ou navegação de repositórios funcionais nessa preview.

## Resultado V1 — histórico de 2026-11-25

- **26 testes Python aprovados**: integridade de calendário, dois anos da fonte pública, cache atômico, erro de gravação, fallback, dados vazios, métricas, leap year, XML/Unicode/injeção, visibilidade explícita, todas as fontes de picture existentes, contraste e determinismo de fontes.
- **88 SVGs**: 44 versões padrão + 44 alternativas estáticas, ambos os temas, XML válido e sem script, foreignObject, imagens raster internas ou referências externas ativas.
- **Geração central determinística**: hashes dos 88 SVGs idênticos após nova execução de `scripts/build.py`. `scripts/build.py --refresh` também executado com coleta pública real, preservando o cache sem mudanças.
- **12 screenshots completas aprovadas**, 16 imagens do README decodificadas por captura, zero overflow de página/README, erros HTTP/JavaScript, imagens quebradas ou temas incorretos.
- **44 verificações de SVG direto** (tema dark, incluindo as alternativas estáticas): XML, título, descrição, CSS e texto visível com movimento reduzido; zero falhas. Ambos os temas também foram validados via XML e imagens na preview.
- **6 comparações de frames no contexto de imagem aprovadas**: picture real isolado para não consumir a animação enquanto carrega o restante da página. Em quatro segundos mudaram 118.885 pixels no hero, 83.845 no activity e 29.185 no VORCEN. As três alternativas reduzidas tiveram **zero pixels alterados**.
- Seleção estática via picture aprovada em dark/light, desktop 1440 e mobile 375.
- Inspeção visual pelo agente: dark desktop e mobile, light desktop; retrato reconhecível, textos sem corte e gráfico financeiro visível após correções. Isso não substitui comparação com o concept ausente.
- Payload local carregado: aproximadamente **691–694 kB** por preview. DOMContentLoaded local: aproximadamente **630–663 ms**. Medições do ambiente Chromium local, sem alegação sobre o GitHub remoto.
- `pip check` sem conflitos; cinco dependências de produção/retrato consultadas na OSV, sem vulnerabilidades retornadas. Resultado em `dependency-audit.json`. Workflow parseado como YAML e conferido sem gatilho push; nenhuma execução remota.
- `git diff --check` aprovado. Busca de padrões de credenciais em fonte/config/dados/docs sem ocorrência. Coleta guarda somente datas/contagens agregadas publicamente expostas, sem nomes de repositórios privados.

Ferramentas: Python 3.12, Playwright 1.62.1, Chromium 151 e pngjs 7.0.0. Para instalar somente as ferramentas de evidência: `npm ci`, depois `npx playwright install chromium`; iniciar a preview antes de executar os scripts de teste. Elas não são dependências do README nem do workflow diário.

As evidências estão no diretório `screenshots/` da entrega local; relatórios JSON permitem conferir cada viewport e a seleção real dos arquivos. A captura completa foi refeita após os ajustes de espaço do activity, linha financeira, fontes estáticas e inclusão de achievements públicos verificados.

## Resultado V1.1 — refinamento de identidade e ecossistema

- **30 testes Python aprovados**; quatro novos contratos cobrem fotografia atual/hash, ausência do card removido com preservação da empresa, ordem 2 + 3 e encaixe de textos nas variantes dos cinco produtos.
- **104 SVGs** válidos, com geração determinística confirmada. Retrato real de 132×79 caracteres, proporção preservada e fotografia lateral atualizada.
- **12 screenshots completas aprovadas**, dark/light em 1920×1080, 1440×900, 1280×720, 768×1024, 390×844 e 375×812. Quinze imagens do README por captura; zero falhas de decodificação, tema, HTTP/JavaScript ou overflow. As coordenadas medidas também confirmam dois cards na primeira linha, três na segunda e destaque maior nos dois primeiros.
- **52 verificações de SVG direto aprovadas** (um tema, todas as versões padrão/estáticas); ambos os temas foram validados no contexto de imagem em todas as resoluções.
- Comparação real de frames, picture/img: hero **96.217**, activity **86.528**, VORCEN **21.037** pixels alterados. As respectivas alternativas estáticas têm **zero** pixels alterados com movimento reduzido. Seleção estática aprovada nos dois temas, em desktop/mobile.
- Inspeção visual das capturas Dark desktop, Dark 375 e Light 390 confirmou postura da nova fotografia, legibilidade e composição 2 + 3 sem placeholders.
- Nenhuma referência ao produto retirado nas áreas ativas de configuração, scripts, README, preview ou SVGs. Registros históricos e strings de testes de regressão são mantidos intencionalmente.
- `pip check` e `git diff --check` aprovados; espaços finais do ASCII são colunas intencionais, configurados em `.gitattributes`.
- Preview reiniciada em loopback na porta 8765 e resposta HTTP 200 verificada. Evidências atuais em `outputs/v1.1/screenshots/` da entrega; fontes e comportamento seguem os mesmos contratos da V1. Nenhum teste ou publicação remota foi realizado.

Detalhes e proveniência em `REFINEMENT_V1_1.md` e `portrait-source.json`. Os resultados V1 acima permanecem como histórico, sem substituir as medições atuais.
