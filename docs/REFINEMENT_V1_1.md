# LKR Engineering Intelligence V1.1

Continuação da branch `redesign/engineering-intelligence-v1`, partindo de `04d0303f65d6beb43e44596d5fceb7dae46ba5b2`. O estado inicial estava limpo. A main permanece em `ae120ffced20c9c4b15d9e5b935615d45a963490`.

## Identidade

A fotografia atual foi buscada pela API pública e por requisições diretas ao avatar com `Cache-Control: no-cache`, `Pragma: no-cache`, fetch `no-store` e parâmetro único. Os pedidos `s=2048` e `s=4096` retornaram os mesmos bytes em 460×460. Essa foi a maior resolução disponibilizada nas consultas; não houve upscale artificial. Hash atual e anterior, URL e data estão em `portrait-source.json`. A inspeção visual confirmou camiseta preta, óculos, corrente e mão próxima ao rosto.

O asset local e a fotografia da sidebar foram atualizados. A máscara GrabCut recebeu coordenadas específicas para a nova fotografia, incluindo cabelo, mão, braços e camiseta. Densidade 132×79, CLAHE, contraste, sombras e iluminação corporal foram ajustados. O renderer preserva a proporção quadrada completa dentro do painel existente, sem alongar o rosto. A revelação progressiva por linhas e os fallbacks estáticos permanecem ativos nos temas Dark e Light. A fotografia pública da conta não foi alterada.

## Ecossistema

O projeto de produto retirado foi removido da configuração, da geometria exclusiva do renderer, do README e de seus quatro SVGs anteriores. O histórico original permanece no commit anterior. Não foram removidos o cargo **Co-Founder at LK Technologies Brasil**, o ícone genérico de camadas usado nesse cargo nem o card institucional da empresa.

O layout agora contém exatamente cinco produtos:

- Primeira linha: **ETHAN / VORCEN**, 49% cada, SVGs de 352×238.
- Segunda linha: **GIDACE / INORYX / Vaultify**, 32% cada, SVGs de 232×222.

As proporções e os textos mantêm consistência entre as linhas. Não há placeholders. Cada produto tem variantes mobile com tipografia/linhas ajustadas para a largura menor, além de alternativa estática; a distribuição 2 + 3 é preservada. A composição do README utiliza somente picture/img e larguras percentuais, sem CSS externo, backend ou JavaScript para os componentes. Dimensões estão nos tokens; ordem e destaque na configuração de projetos.

O renderer agora elimina somente artefatos gerados `project-*.svg` que não pertencem mais aos projetos públicos configurados. Não altera fotos, fontes, outras seções ou arquivos fora de `generated/{theme}`.

## Verificações

- 30 testes Python aprovados, incluindo novos contratos de ordem 2 + 3, destaque, encaixe de texto, ausência do card retirado, preservação da empresa e hash da nova fotografia.
- 104 SVGs válidos (desktop/mobile, Dark/Light, padrão/estático). Nova geração confirmou hashes idênticos dos 104 arquivos.
- Testes de animação em picture/img aprovados: hero, activity e VORCEN têm mudança entre frames; com movimento reduzido os três têm zero pixels alterados. Seleção estática aprovada nos dois temas, em 375 e 1440 px.
- Busca por nomes/IDs obsoletos nas áreas ativas (`config`, `scripts`, `README`, `preview`, `generated`) sem ocorrência. Menções de auditoria/regressão e histórico não são referências exibidas ao visitante.
- `git diff --check` e `pip check` aprovados. Espaços finais do ASCII são colunas intencionais, declarados em `.gitattributes`.
- Preview reiniciada na porta 8765, bind em loopback. Fonte HTML e SVGs são os mesmos do README real. Relatórios de viewport e capturas completas estão na entrega `v1.1/screenshots`.

Captura final: **12 screenshots aprovadas**, nos dois temas e seis resoluções, com zero falhas. O harness conferiu a geometria real das linhas 2 + 3, destaque dos dois primeiros cards, imagens, temas e overflow; verificou ainda os 52 SVGs de um tema em modo normal/reduzido. Inspeção visual adicional de Dark desktop/mobile e Light mobile concluída. Validação continua local; GitHub real/Camo não foi publicado nem testado remotamente. Não houve push, merge, execução de CI remoto ou alteração nas configurações da conta.

Preview Dark aberta automaticamente em nova aba do **Chrome**, confirmado como navegador padrão pelo handler HTTP `ChromeHTML`. O controle nativo confirmou URL `http://localhost:8765/preview/?theme=dark`, título da preview e os cinco produtos na árvore de acessibilidade. A abertura pelo shell foi bloqueada pela política do ambiente; o controle de navegador concluiu a ação sem alterar configurações.
