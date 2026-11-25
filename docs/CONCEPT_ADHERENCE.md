# Matriz de aderência — LKR Engineering Intelligence V1

## Critério e limites

O concept citado no handover não foi anexado nesta conversa nem localizado no clone. Foi solicitado seu caminho. Assim, a fidelidade **à imagem aprovada não pode ser aferida**; nenhum percentual é declarado. A matriz avalia a estrutura explicitamente descrita no handover e as capturas da preview local. A comparação com o concept e a homologação no GitHub real continuam pendentes.

Evidências: 12 capturas completas em `outputs/screenshots/` da entrega (dark/light × 1920×1080, 1440×900, 1280×720, 768×1024, 390×844, 375×812), `report.json`, `animation-report.json` e relatório `VALIDATION.md`. As imagens exibidas na preview são exatamente os SVGs locais do README.

| Componente / elemento esperado | Implementado e estrutura | Movimento / estado estático | Fidelidade visual e divergências | Evidência e status |
|---|---|---|---|---|
| Hero: ASCII à esquerda, identidade à direita, código abaixo | Script recuperado; retrato 112×84 caracteres, nome, cargo, áreas e empresa; SVG desktop e composição vertical mobile | Retrato revela por linha, identidade entra, código digita, cursor, status decorativo e reflexos; alternativas estáticas por `<picture>` | Estrutura textual atendida; mobile empilha para leitura. Retrato é derivado da fotografia preservada e regeneração produziu SHA-256 idêntico. Comparação com concept pendente | Capturas de todos os tamanhos, frames hero; implementado localmente |
| Development Activity: quatro indicadores | Total, dias ativos, streak atual e maior streak do mesmo snapshot validado | Entrada escalonada; estado final sem movimento | Métricas reais do período declarado; não reutiliza 1.386 do handover sem contexto | Testes de calendário/cache, capturas; implementado localmente |
| Heatmap: últimos 12 meses, dias/meses e escala dourada | 365 datas de 26/11/2025 a 25/11/2026; células com título acessível e legenda | Revelação por coluna/linha; versão estática | Desktop contínuo; mobile em duas faixas cronológicas para legibilidade. Espaçamento da legenda corrigido após primeira inspeção. Comparação com concept pendente | Capturas desktop/mobile; implementado localmente |
| Monthly Activity: barras proporcionais | Escala linear desde zero, gradiente dourado e rótulos; 13 meses de calendário, com extremos parciais identificados | Crescimento das barras; alternativa estática | Rolling year cruza 13 meses parciais; documentado em DATA_SOURCES. Não usa dados fictícios | Testes de totais/vazio, capturas; implementado localmente |
| LK System: camadas flutuantes | SVG independente, quatro planos com arestas e profundidade, descrição fornecida | Flutuação individual e reflexo | Geometria autoral, tokens preservados; comparação com concept pendente | project-lk-system, capturas; implementado |
| ETHAN: esfera neural | SVG independente, esfera, elipses, conexões e nós | Pulsação controlada e reflexo | Geometria autoral; comparação com concept pendente | project-ethan, capturas; implementado |
| VORCEN: linha financeira dourada | SVG independente, curva, área gradual, grade e endpoint | Traçado progressivo e linha base estática sempre legível | Linha base acrescentada após captura revelar desaparecimento antes da animação em imagem fora da tela | project-vorcen, frames e capturas finais; implementado |
| GIDACE: agentes e orquestração | SVG independente, cubos com faces e conexões | Flutuação escalonada | Geometria autoral; comparação com concept pendente | project-gidace, capturas; implementado |
| INORYX: conhecimento | SVG independente, grafo com nós e arestas | Nós com pulsação suave | Geometria autoral; comparação com concept pendente | project-inoryx, capturas; implementado |
| Vaultify: cofre com profundidade | SVG independente, corpo com perspectiva, dobradiças e mostrador | Rotação discreta do mostrador | Geometria autoral; comparação com concept pendente | project-vaultify, capturas; implementado |
| Bento Grid dos seis produtos | Pares de imagens independentes, três linhas, larguras percentuais suportadas no README | Animação interna independente | Duas colunas preservam leitura em mobile sem CSS externo; a disposição exata do concept ainda precisa ser comparada | Capturas 375–1920; implementado com layout provisório documentado |
| Technology Stack: seis grupos, ícones monocromáticos | Todos os itens especificados; desktop 3×2, mobile 2×3; sem níveis de proficiência | Estado estático e entrada sutil | Licenças/fontes e atribuições auditadas por arquivo. Comparação com concept pendente | stack, stack-mobile, ASSET_LICENSES; implementado |
| Professional Connections: quatro cards | LinkedIn, GitHub, Website, LK Technologies; URLs existentes preservadas | Reflexo discreto; fallback estático | GitHub/site HTTP 200; LinkedIn HTTP 999 impede verificação, card sem link ativo até validação. Website/empresa usam a mesma URL já configurada, sem inventar endereço | LINKS.json, capturas; LinkedIn pendente |
| Rodapé, divisores e tipografia espaçada | LKR — ENGINEERING INTELLIGENCE com divisor dourado e missão | Estático | Tokens originais preservados; comparação com concept pendente | footer desktop/mobile; implementado |
| Shell GitHub local | Cabeçalho, navegação, coluna lateral, avatar público, dados e achievements públicos verificados, container README | Apenas controles locais de tema; SVGs fazem seu próprio movimento | Aproximação local; não replica serviços do GitHub. Nenhum contador/achievement inventado | profile-public.json, capturas; preview funcional |

## Ajustes após inspeção

1. Validação XML passou a remover corretamente caracteres inválidos e surrogates também antes da subsetagem das fontes.
2. Heatmap recebeu mais espaço para impedir sobreposição da legenda com a última linha de células.
3. VORCEN recebeu linha base estática, preservando o conteúdo quando o navegador posterga uma animação fora da área visível.
4. Testes em imagens revelaram que Chromium pode não propagar movimento reduzido ao SVG, embora o documento SVG direto respeite a preferência. Foram gerados SVGs `*-static.svg`, selecionados por media query no próprio README.

## Pendências reais

- Receber/localizar o concept e comparar proporções, geometria, densidade, ritmo e distribuição exata dos cards.
- Validar o LinkedIn manualmente ou por uma fonte pública que permita consulta.
- Após autorização futura para publicação, testar GitHub real, proxy/cache de imagens e seleção de fontes/tema/movimento em navegadores adicionais.
- Nenhum push, merge, execução de workflow remoto ou alteração na main foi realizado. A publicação não é condição para a preview local.
