# Inventário inicial da Template PV

## Abas existentes
- tbCadastroProduto
- Tabela Venda - Parcela
- Referencias
- Analise Proposta
- Permuta
- Fluxo
- PRC + COORD
- Imobs
- Carta Proposta

## Leitura funcional inicial por aba
### Analise Proposta
Tela principal da negociação sem permuta. Captura dados da proposta, monta tabela base, monta proposta comercial, calcula comissão e prêmio, mostra análise comparativa de PV e controla a chave de permuta por `N6`.

### Permuta
Versão da proposta quando existe bem entregue como parte do pagamento. Reaproveita grande parte do contexto da Analise Proposta, mantém grade própria e recalcula VGV, VPL, comissão e distribuição.

### Fluxo
Motor matemático principal da planilha. Define premissas financeiras, monta a curva mensal do fluxo da tabela e da proposta, desconta os fluxos a valor presente e possui bloco separado para proposta com permuta.

### Tabela Venda - Parcela
Base parametrizadora do parcelamento padrão. Fornece quantidade de parcelas, periodicidade, percentuais, mês de início e composição de sinal, entrada, mensais, semestrais, única e financiamento.

### Referencias
Base pesada de consulta. Contém a tabela de lookup do produto, unidade, área, preço, garagem e outros atributos.

### PRC + COORD
Aba derivada que interfere no cálculo, especialmente em comissão e rateios.

### Carta Proposta
Saída de apresentação do resultado.

### tbCadastroProduto
Base cadastral de apoio, inclusive para taxa VPL e mês de entrega.

### Imobs
Base de imobiliárias.
