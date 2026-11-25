# LKR Engineering Intelligence V1.2

Continuação local de `b09c7eb`, na branch original `redesign/engineering-intelligence-v1`. Main preservada. Sem push, merge, publicação, CI remoto ou alterações de configuração da conta.

## Identidade

O retrato ASCII, seu container e suas animações foram removidos integralmente do Hero. O arquivo de caracteres, o gerador e `requirements-portrait.txt` foram removidos; NumPy/OpenCV também foram desinstalados do ambiente isolado. A fotografia compartilhada foi mantida somente na sidebar. Fontes, ícones genéricos e o construtor SVG são compartilhados e foram preservados.

O novo Hero ocupa toda a largura: identidade profissional à esquerda e código à direita no desktop, com composição vertical compacta no mobile. Nome, cargo, áreas, Co-Founder at LK Technologies Brasil, indicador decorativo e animações de código/entrada/reflexos foram preservados. Alturas vetoriais totais: 304 desktop e 406 mobile. Não há imagem substituta nem lacuna do retrato anterior.

## Auditoria e exportação original

O projeto original ETHAN foi consultado exclusivamente em leitura. A inspeção confirmou **Three.js/WebGL**, shaders GLSL, partículas procedurais, materiais, câmera e movimento do renderer visual original. Não foi presumida uma tecnologia nem desenhada uma esfera substituta. O visual usado é o preset branco original disponível no renderer, com as configurações visuais de composição do aplicativo. A qualidade alta mantém o conjunto original de partículas e camadas da esfera; somente elementos de fundo/UI foram excluídos da captura isolada.

O renderer e as dependências visuais mínimas foram isolados em um diretório de trabalho separado, fora do perfil e do ETHAN. Chromium/Playwright executaram o código original, com captura determinística do canvas em 512×512. A qualidade utilizada desenha 96.000 partículas de superfície e 203.824 pontos agregados das camadas visuais por frame; câmera perspectiva original e iluminação emissiva dos shaders foram preservadas. Nenhum .env, credencial, prompt interno ou código de backend foi consultado/copiado para a exportação. Nenhum código-fonte privado foi adicionado ao perfil: somente as imagens finais. Hashes dos oito módulos visuais utilizados e o estado Git pré-existente foram conferidos antes/depois, sem mudanças. O registro privado fica fora do perfil; `ethan-export.json` contém somente resultados e hashes dos assets finais.

Não houve gravação da interface completa nem captura estática como solução principal. A mídia exportada inclui movimento real do renderer e a composição original do card (fundo, bordas, tipografia e dimensões). O README carrega os mesmos arquivos da preview, sem WebGL, canvas ou JavaScript no componente publicável.

## Formato e medidas

| Variante | Dimensões do card | WebP selecionado | GIF fallback |
|---|---:|---:|---:|
| Dark desktop | 352×238 | 971.774 bytes | 2.282.535 bytes |
| Light desktop | 352×238 | 782.342 bytes | 1.971.622 bytes |
| Dark mobile | 174×204 | 410.754 bytes | 959.209 bytes |
| Light mobile | 174×204 | 366.404 bytes | 833.464 bytes |

Captura da esfera: **512×512**. Duração: **6 segundos**. Timeline de apresentação: **24 FPS**, 144 posições; frames idênticos são coalescidos pelos encoders para **129 quadros únicos**, taxa média de **21,5 FPS** com durações variáveis. GIF usa quantização temporal de centésimos de segundo; o total continua exatamente 6.000 ms.

O movimento procedural original não é naturalmente periódico. Para fechar um loop contínuo sem salto/crossfade, a exportação remapeia os quadros reais por uma trajetória temporal cossenoidal bidirecional: desacelera suavemente, retorna e encontra o mesmo quadro na emenda. Não altera shaders, geometria, distribuição de partículas ou materiais, mas **adapta a cronologia original**. Não é uma afirmação de reprodução temporal infinita idêntica ao aplicativo.

Os quadros fonte da emenda são idênticos. Na compressão WebP com perdas, a diferença média absoluta entre primeiro/último quadro ficou entre 0,66 e 0,89 em canais de 0–255. GIF usa paleta global de 256 cores para evitar cintilação da paleta; PSNR do primeiro quadro versus composição sem perdas: 38,71–39,47 dB. Métricas completas em `ethan-export.json`.

WebP foi escolhido pelo peso aproximadamente 57–60% menor que o GIF equivalente. O README oferece **GIF animado de fallback** por tipo de mídia e **PNG estático para movimento reduzido**. [O GitHub anunciou suporte a WebP](https://github.com/orgs/community/discussions/171343); [GIF consta nos formatos documentados](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files). Isso fundamenta a seleção; a publicação no perfil/Camo real permanece não executada por restrição do usuário.

## Integração e proteção

ETHAN/VORCEN continuam na primeira linha; GIDACE/INORYX/Vaultify na segunda. A esfera genérica SVG foi removida, juntamente com seus assets anteriores. Nenhum outro produto foi restaurado/adicionado. A identificação e o card institucional da LK Technologies Brasil permanecem.

O build normal regenera SVGs e valida os assets ETHAN já exportados; não lê nem recompila código privado e não depende do ETHAN no CI. O ambiente privado de exportação fica no diretório de trabalho separado desta execução, preservado localmente para ajustes futuros, e não integra o ZIP publicável. Pillow é opcional para mídia, conforme `requirements-media.txt`; Three.js não é dependência do README nem do build diário.

## Verificações e limites

- 32 testes Python aprovados: incluindo remoção ASCII, Hero compacto, formatos/assinaturas, duração GIF, limites de tamanho, fontes picture e preservação da composição 2 + 3.
- Testes reais de imagem aprovaram movimento de Hero, activity, VORCEN e ETHAN; quatro alternativas reduzidas tiveram zero pixels alterados em frames separados por quatro segundos.
- Seleção WebP, fallback GIF forçado e movimento reduzido PNG aprovados nos dois temas e em 375/1440 px.
- Doze screenshots completas nos dois temas e seis resoluções, com zero falhas de imagem, tema, JavaScript/HTTP, overflow ou distribuição do Bento. SVGs diretos também validados; números finais em `VALIDATION.md` e relatórios da entrega.
- Fontes de código/arquivos privados não estão em `generated/`. Arquivos não relacionados ao Hero/ETHAN em `generated/` permaneceram idênticos ao commit anterior.

As duas capturas enviadas da implementação anterior foram utilizadas para preservar as demais seções. **A terceira captura do ETHAN Desktop não foi recebida**: a comparação realizada é com o renderer original isolado e com seus quadros sem compressão, não uma comparação declarada com um anexo ausente. Cor/preset do estado específico daquela captura ainda podem exigir ajuste quando a imagem estiver disponível. Não foi declarado 100% de aderência a ela.

Evidências locais: `outputs/v1.2/screenshots/`, `original-vs-export.png`, `original-isolated-frame.png`, `export-report.json` e master visual 512×512. A animação master de qualidade alta é uma evidência local maior e não é carregada pelo README. Nada foi publicado.
