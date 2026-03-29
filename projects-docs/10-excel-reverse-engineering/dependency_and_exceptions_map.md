# Mapa de dependencias criticas e excecoes

## Dependencias criticas
### Contexto inicial -> tabela base -> simulacao
Antes do calculo, existe uma cadeia obrigatoria de preparacao:
1. `Analise Proposta!E5` define o empreendimento
2. `Analise Proposta!F8` define a unidade do empreendimento
3. `Analise Proposta!E11` define a data base da analise
4. `Analise Proposta!E6` e formado a partir de empreendimento + unidade
5. `Referencias` e `Tabela Venda - Parcela` preenchem a base usada para o PV padrao
6. so entao a planilha compara o PV padrao com o PV da proposta

### Analise Proposta -> Fluxo
A aba nao apenas exibe resultados do fluxo, ela depende do Fluxo para a propria analise de PV.

### Permuta -> Fluxo
A aba Permuta depende fortemente do Fluxo, mas le o bloco do cenario com permuta.

### Fluxo -> Analise Proposta
O Fluxo consome a proposta normal como dado de entrada do motor.

### Fluxo -> Permuta
Quando a flag de permuta esta ativa, o Fluxo passa a ler a proposta com permuta.

### Fluxo -> PRC + COORD
O Fluxo depende de PRC + COORD para comissao indireta.

### PRC + COORD -> Analise Proposta / Permuta
A aba usa a proposta normal ou a proposta com permuta como base de distribuicao da comissao, conforme o trilho ativo.

## Papel exato de PRC + COORD
1. calcula a base de comissao
2. distribui a comissao por papel e por parcela
3. gera a comissao indireta do fluxo, consolidada em `O34`

## Regras sensiveis para paridade
1. comutacao entre cenario normal e permuta
2. distribuicao sequencial da comissao por parcela
3. calculo da base de comissao com unidade de troca
4. lancamento pontual da comissao indireta
5. separacao entre buckets reajustavel e irreajustavel
6. desconto diferente por bucket
7. arredondamentos visiveis
8. guard rails com minimo zero e `IFERROR`
