# Matriz de variacao por empreendimento, unidade e permuta

Fonte de observacao:
- workbook `Template PV - Março 26_v4.xlsx`
- cenarios simulados pelo motor Python a partir dos defaults reais da planilha
- data-base usada no default do workbook: `2026-03-28`

## Regra consolidada
O comportamento observado confirma o seguinte:
- primeiro se escolhe o empreendimento
- depois se escolhe a unidade desse empreendimento
- por fim se ancora a data-base da analise

Com isso, a planilha monta o fluxo padrao da venda para aquela combinacao. O empreendimento define a estrutura das parcelas; a unidade apenas recalcula os valores monetarios dessa mesma estrutura.

## Estrutura por empreendimento
### Garten
Fluxo base observado:
- `Sinal`: `1 x 4%`
- `Entrada`: `3 x 3%`
- `Mensais`: `14 x 1,428571%`
- `Semestrais`: `2 x 5%`
- `Unica`: `1 x 7%`
- `Financ. Bancario`: `1 x 50%`

Permuta observada:
- a linha `Semestrais` vira `1 x Permuta`
- o valor unitario da permuta e igual ao valor unitario da semestral
- o total do trilho de permuta cai, porque `2 x semestral` vira `1 x permuta`

### Haut
Fluxo base observado:
- `Sinal`: `1 x 10,5%`
- `Entrada`: `3 x 6,5%`
- `Mensais`: `0 x`
- `Semestrais`: `0 x` com valor latente parametrizado em `2%`
- `Unica`: `0 x` com valor latente parametrizado em `3%`
- `Financ. Bancario`: `1 x 70%`

Permuta observada:
- a linha `Semestrais` inativa e convertida em `1 x Permuta`
- isso adiciona uma parcela de permuta no valor unitario latente da semestral
- o financiamento continua com `70%`, mas a captura total sobe levemente porque o VGV total do trilho aumenta

## Matriz resumida dos cenarios
### Sem permuta
| Cenario | VGV Proposta | Captura Total | PV Status | Risco |
| --- | ---: | ---: | --- | --- |
| `Garten|801` | `2.689.236,00` | `50,00%` | `PV Reprovado` | `Alto` |
| `Garten|1001` | `2.723.368,00` | `50,00%` | `PV Reprovado` | `Alto` |
| `Haut|801` | `1.058.874,00` | `30,00%` | `PV Aprovado*` | `Baixo` |
| `Haut|1001` | `1.193.699,00` | `30,00%` | `PV Aprovado*` | `Baixo` |

### Com permuta
| Cenario | VGV Permuta | Captura Total | PV Status | Risco |
| --- | ---: | ---: | --- | --- |
| `Garten|801` | `2.554.774,20` | `47,37%` | `PV Aprovado*` | `Medio` |
| `Garten|1001` | `2.587.199,60` | `47,37%` | `PV Aprovado*` | `Medio` |
| `Haut|801` | `1.080.051,48` | `31,37%` | `PV Aprovado*` | `Baixo` |
| `Haut|1001` | `1.217.572,98` | `31,37%` | `PV Aprovado*` | `Baixo` |

## Implicacoes para backend e frontend
- o app precisa bloquear o calculo enquanto `empreendimento`, `unidade` e `data-base` nao estiverem definidos
- trocar a unidade dentro do mesmo empreendimento deve apenas recarregar valores e metadados da unidade
- trocar o empreendimento deve recarregar toda a estrutura padrao das parcelas
- habilitar permuta deve derivar o trilho de permuta a partir do fluxo normal, convertendo a linha semestral para `Permuta`
