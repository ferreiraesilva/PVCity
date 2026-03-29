# Inventario inicial da Template PV

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
Tela principal da negociacao sem permuta. A sequencia funcional obrigatoria e:
1. selecionar o empreendimento em `E5`
2. selecionar a unidade correspondente em `F8`
3. informar a data base da analise em `E11`

Com esse contexto, a aba monta a tabela base da venda padrao, carrega os dados da unidade, monta a proposta comercial, calcula comissao e premio, e compara o PV padrao com o PV da proposta do cliente. Tambem controla a chave de permuta por `N6`.

### Permuta
Versao da proposta quando existe bem entregue como parte do pagamento. Reaproveita grande parte do contexto da Analise Proposta, mantem grade propria e recalcula VGV, VPL, comissao e distribuicao.

### Fluxo
Motor matematico principal da planilha. Define premissas financeiras, monta a curva mensal do fluxo da tabela e da proposta, desconta os fluxos a valor presente e possui bloco separado para proposta com permuta.

### Tabela Venda - Parcela
Base parametrizadora do parcelamento padrao. Fornece quantidade de parcelas, periodicidade, percentuais, mes de inicio e composicao de sinal, entrada, mensais, semestrais, unica e financiamento.

### Referencias
Base pesada de consulta. Contem a tabela de lookup do produto, unidade, area, preco, garagem e outros atributos.

### PRC + COORD
Aba derivada que interfere no calculo, especialmente em comissao e rateios.

### Carta Proposta
Saida de apresentacao do resultado.

### tbCadastroProduto
Base cadastral de apoio, inclusive para taxa VPL e mes de entrega.

### Imobs
Base de imobiliarias.
