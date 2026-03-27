# Mapa de dependências críticas e exceções

## Dependências críticas
### Analise Proposta -> Fluxo
A aba não apenas exibe resultados do fluxo, ela depende do Fluxo para a própria análise de PV.

### Permuta -> Fluxo
A aba Permuta depende fortemente do Fluxo, mas lê o bloco do cenário com permuta.

### Fluxo -> Analise Proposta
O Fluxo consome a proposta normal como dado de entrada do motor.

### Fluxo -> Permuta
Quando a flag de permuta está ativa, o Fluxo passa a ler a proposta com permuta.

### Fluxo -> PRC + COORD
O Fluxo depende de PRC + COORD para comissão indireta.

### PRC + COORD -> Analise Proposta / Permuta
A aba usa a proposta normal ou a proposta com permuta como base de distribuição da comissão, conforme o trilho ativo.

## Papel exato de PRC + COORD
1. calcula a base de comissão
2. distribui a comissão por papel e por parcela
3. gera a comissão indireta do fluxo, consolidada em `O34`

## Regras sensíveis para paridade
1. comutação entre cenário normal e permuta
2. distribuição sequencial da comissão por parcela
3. cálculo da base de comissão com unidade de troca
4. lançamento pontual da comissão indireta
5. separação entre buckets reajustável e irreajustável
6. desconto diferente por bucket
7. arredondamentos visíveis
8. guard rails com mínimo zero e `IFERROR`
