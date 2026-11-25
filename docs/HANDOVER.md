# Recuperação — LKR Engineering Intelligence V1

Auditoria inicial em 2026-11-25. Nenhum reset, clean, merge, push ou execução remota.

- Clone existente: `C:\Users\lukas\Documents\Dev\Portifólio\LukasAlexandre`.
- Origin: `https://github.com/LukasAlexandre/LukasAlexandre.git`.
- Branch: `redesign/engineering-intelligence-v1`.
- HEAD inicial: `ae120ffced20c9c4b15d9e5b935615d45a963490`.
- `git diff` e `git diff --cached`: vazios. Arquivos não rastreados: `assets/`, `config/`, `generated/`, `scripts/`.
- Backup integral dos arquivos existentes (incluindo README e workflow) em `C:\Users\lukas\Documents\Codex\2026-11-25\files-pasted-by-the-user-handover\work\recovered-before`.

## Inspeção dos arquivos recuperados

| Arquivo | Estado inicial | Decisão |
|---|---|---|
| `scripts/common.py` | Construtor SVG, fontes WOFF2 subsetadas, escape XML, tokens e movimento reduzido | Reutilizar; testar determinismo e fallback |
| `scripts/icons.py` | Ícones Simple Icons e geometria autoral | Reutilizar; documentar procedência individual |
| `scripts/generate_ascii.py` | Pipeline real OpenCV/CLAHE/GrabCut e densidade configurável | Preservar, validar regeneração e entradas |
| `scripts/render_hero.py` | Hero desktop/mobile nos dois temas | Reutilizar; corrigir qualquer overflow observado |
| `config/design-tokens.json` | Tokens dark/light, fontes, layout, movimento | Preservar e completar apenas quando necessário |
| `config/profile.json` | Identidade, retrato e quatro conexões | Preservar; verificar links antes de ativar |
| `assets/portrait/source.jpg` | Fotografia pública já coletada | Preservar; origem preliminar informada no handover: avatar GitHub |
| `assets/portrait/portrait.txt` | Retrato ASCII de 112 colunas | Preservar e comparar com pipeline |
| `assets/fonts/*` | Inter e JetBrains Mono, WOFF2 e licenças SIL OFL 1.1 | Preservar e auditar |
| `assets/icons/*` | 14 SVGs e declaração CC0 Simple Icons | Preservar e auditar por marca |
| `generated/{dark,light}/hero*.svg` | Quatro SVGs existentes | Preservar backup e validar em navegador |
| `README.md` | Perfil antigo com badges e serviços externos | Reconstruir após auditoria, original preservado no backup |
| `.github/workflows/main.yml` | Workflow antigo de snake com push na main | Substituir localmente por atualização preparada, sem executar remotamente |

Ausentes inicialmente: coleta/cache de contribuições, activity, seis produtos, stack, conexões, comando central, testes, documentação e preview. Nenhum teste ou manifesto de dependências existente. Python padrão resolve para alias indisponível; runtime Python empacotado disponível, mas sem fontTools. Dependências serão instaladas isoladamente.

## Referência visual

O único anexo desta conversa é o handover textual. O concept não foi localizado no clone; solicitado caminho ao usuário. A comparação visual com a imagem aprovada permanece pendente enquanto ela não estiver disponível. Não declarar aderência integral nem homologação no GitHub real.

## Continuação e correções

- Reutilizados: fotografia, ASCII, todos os arquivos WOFF2/licenças, os 13 ícones locais, `icons.py`, tokens e composição do hero. O inventário inicial mencionava 14 SVGs de ícones; contagem final auditada: 13.
- `common.py`: escape XML corrigido para os intervalos Unicode válidos, remoção de surrogates antes da subsetagem, geração de alternativas estáticas. O teste de injeção revelou a necessidade da segunda correção.
- `generate_ascii.py`: valida densidade de 24–400 colunas e rejeita segmentação vazia. Regeneração em 112 colunas produziu exatamente o arquivo anterior, SHA-256 `b701e3ed0537466b82e972efac345f64fcf50233c5b49c1f032ead54fa78dc59`.
- `render_hero.py` e `icons.py` reutilizados sem reescrita. Os quatro SVGs originais foram regenerados pelo mesmo renderer; originais preservados no backup.
- `profile.json`: identidade e URLs mantidas; marcadores explícitos de verificação acrescentados. LinkedIn bloqueou consulta HTTP 999.
- README e workflow antigos substituídos localmente, com originais preservados no backup. O workflow novo está apenas preparado.
- Acrescentados: coleta/cache, activity, produtos, stack, conexões, build central, testes, preview, licenças adicionais e documentação. Nenhuma geometria do repositório de referência foi copiada.
- Dependências fixadas em manifests; cinco pacotes consultados na OSV sem vulnerabilidades retornadas na data da consulta (`dependency-audit.json`). Ambiente isolado `.venv` fora do versionamento; `pip check` aprovado.
- Avatar atual da API pública GitHub comparado por SHA-256: corresponde à fotografia recuperada. Fonte exata e dados laterais públicos registrados em `profile-public.json`.

Relatórios de teste/preview em `VALIDATION.md`; matriz honesta de aderência e pendências em `CONCEPT_ADHERENCE.md`. Branch permanece a original dedicada. Não houve alteração de main, publicação ou execução remota.

## Continuação V1.1

Estado inicial limpo em `04d0303`. Nova fotografia pública obtida sem cache, hash diferente confirmado, máscara/contraste e ASCII atualizados para 132×79, com enquadramento preservado. Produto retirado removido das áreas ativas e assets exclusivos; identificação e card institucional da empresa preservados. Cinco produtos na composição 2 + 3 solicitada, variantes mobile específicas e fallbacks estáticos. Trinta testes Python e doze capturas Dark/Light aprovados. Proveniência, detalhes, limitações e evidências atuais em `REFINEMENT_V1_1.md`, `portrait-source.json` e `VALIDATION.md`. Main permanece no HEAD original.

## Continuação V1.2

Estado inicial limpo em `b09c7eb`. Hero redesenhado sem retrato, container ou animações ASCII; gerador/arquivo de caracteres/manifesto exclusivo removidos após auditoria dos arquivos compartilhados. Fotografia lateral preservada. Renderer original ETHAN consultado em leitura e exportado em ambiente separado, sem source privado no perfil. Card ETHAN passa a selecionar WebP, GIF de fallback e PNG reduzido; outros cards/atividade/stack/conexões gerados permanecem idênticos. Trinta e dois testes Python, doze capturas e testes de animação/fallback aprovados. Detalhes em `REFINEMENT_V1_2.md` e `ethan-export.json`; evidências atuais em `outputs/v1.2/` da entrega local. Fonte ETHAN e suas alterações pré-existentes preservadas. Captura específica do ETHAN Desktop ainda não recebida.
