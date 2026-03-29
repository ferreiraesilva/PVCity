# Proposta PDF Generator (Upcoming)

**Status**: PENDING (Phase: PACK-XX)
**Tech Stack**: Python (Backend) ou Frontend (jsPDF/html2canvas)
**Focus**: Emissão oficial do documento de proposta gerado pelo motor de cálculo.

## Overview
Este Feature Pack prevê a expansão futura para gerar propostas comerciais em PDF baseadas no cálculo de paridade matemática (`summary` e `monthly_flow`) retornado pela API.

### Key Capabilities Planejadas
- **Ingestão do Payload:** Consumir idêntico payload de `calculate_scenario` + meta-dados do Corretor.
- **Assinaturas:** Espaço destinado à assinatura do cliente, construtora e corretora.
- **Extrato Mês a Mês:** Tabela consolidada com o fluxo irreajustável esperado.

### Extension Points
Para implementar este módulo, deve-se decidir entre `ReportLab/WeasyPrint` no Backend (garantia de fidelidade) vs `React-PDF` no frontend (desacoplamento rápido). A preferência para o contexto governamentais/imobiliário costuma ser backend.
