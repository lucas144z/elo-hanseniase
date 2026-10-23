# Sugestões para os gráficos e a análise

## 1. Identidade visual e gráficos

A identidade do Elo já tem uma paleta definida. A proposta é manter essa paleta, mas usar as cores dos gráficos com a função de destacar a mensagem, seguindo os princípios de *Storytelling with Data*, de Cole Nussbaumer Knaflic: simplificar o que compete com os dados e conduzir o olhar para o ponto principal.

- **Definir uma cor de destaque por gráfico.** Usar o **<span style="color: #5B2A86">roxo do Elo (#5B2A86)</span>** para a série principal e tons neutros ou <span style="color: #B9A3D6">lavanda clara (#B9A3D6, com baixa saturação/opacidade)</span> para o contexto. No gráfico por UF, por exemplo, Mato Grosso pode ficar em destaque e as outras UFs em tons mais discretos.
- **Reservar o <span style="color: #E8A33D">âmbar (#E8A33D)</span> para eventos que precisem de atenção**, como o período da pandemia ou uma observação específica. Evitar colorir muitos anos ou séries ao mesmo tempo.
- **Usar o <span style='color: #2E9E7A'>verde (#2E9E7A)</span> apenas quando houver um significado claro**, como indicar melhora ou uma série escolhida. Não associar cores a significados diferentes entre gráficos.
- **Reduzir elementos decorativos:** manter grade leve apenas onde ajude a comparar valores; remover bordas e legendas dispensáveis; preferir rótulos diretos nas linhas quando houver espaço.
- **Escrever títulos que expressem a conclusão do gráfico**, acompanhados de subtítulo com medida, local e período. Adicionar anotações curtas para explicar quedas ou mudanças importantes, sem repetir no texto o que o gráfico já mostra.
- **Checar contraste e legibilidade**, inclusive em escala de cinza e para pessoas com deficiência na percepção de cores. A cor não deve ser o único meio de distinguir uma série: combinar com rótulos, estilos de linha ou marcadores.

## 2. Investigar a queda de diagnósticos na pandemia

Investigar se a queda de casos diagnosticados/notificados durante a pandemia está associada a mudanças no acesso aos serviços, na busca por atendimento ou na capacidade de diagnóstico. Os dados do SINAN representam diagnósticos/notificações registrados; uma queda nesses registros, isoladamente, não demonstra redução da transmissão ou da incidência real da hanseníase.

Para tornar a análise mais informativa:

1. **Buscar dados mensais ou trimestrais**, se disponíveis, além das contagens anuais. Uma série mensal permite observar melhor a mudança em 2020 e a retomada posterior.
2. **Comparar períodos definidos antes da análise**, por exemplo: pré-pandemia (2011–2019), pandemia (2020–2021) e período posterior (2022 em diante). Explicitar que os limites são uma escolha analítica e verificar se há dados parciais nos anos finais.
3. **Mostrar a tendência e a variação**, com uma linha ou faixa indicando o início da pandemia e anotações sobre mudanças no contexto de atendimento. Se houver dados adequados, considerar uma análise de série temporal interrompida para estimar a mudança de nível e de tendência, levando em conta sazonalidade e sobredispersão.
4. **Procurar medidas de contexto**, como consultas, exames, notificações ou atendimentos da Atenção Básica, para verificar se a redução de diagnósticos ocorreu junto a uma redução da oferta ou procura de serviços. Registrar a fonte e a compatibilidade geográfica e temporal de cada indicador.
5. **Interpretar com cautela:** diferenças observadas podem refletir alterações na detecção e no registro, atrasos de notificação ou outros fatores. Descrever o resultado como associação ou mudança temporal; não afirmar que a pandemia causou a queda sem evidência que sustente essa conclusão.

## 3. Implementação rápida

- **No código:** ajustar as cores e os rótulos em scripts/tratar_dados.py; usar uma cor de destaque e tons discretos para as demais séries; incluir uma faixa/anotação para 2020–2021 e revisar os títulos para que comuniquem a mensagem principal.
- **Nos dados:** verificar no TABNET/SINAN se há extrações mensais comparáveis e documentar período, data de extração, cobertura e anos incompletos em dados/README.md. Se só houver dados anuais, apresentar a comparação como exploratória e reconhecer essa limitação.
- **Na análise:** montar uma tabela ou gráfico com os períodos pré-pandemia, pandemia e pós-pandemia; comparar contagens e, quando possível, taxas ou indicadores de atendimento. Para uma análise inferencial, avaliar com orientação estatística uma série temporal interrompida e registrar hipóteses e limitações.
- **Na apresentação:** atualizar os gráficos em docs/graficos/ e revisar as afirmações correspondentes no README.md, deixando claro o que os dados mostram e o que ainda é hipótese.

**Referência de visualização:** Cole Nussbaumer Knaflic, *Storytelling with Data: A Data Visualization Guide for Business Professionals*. A autora também apresenta os princípios de simplificação visual, foco e uso intencional da cor em [Storytelling with Data](https://www.storytellingwithdata.com/books) e no artigo [Focusing with color](https://www.storytellingwithdata.com/blog/2014/04/focusing-with-color).
