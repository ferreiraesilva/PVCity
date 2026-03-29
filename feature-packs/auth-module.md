# Auth & RBAC Module (Upcoming)

**Status**: PENDING (Phase: PACK-XX)
**Tech Stack**: NextAuth/Vite Auth + FastAPI OAuth2 (JWT)
**Focus**: Controle de quais corretores podem gerar propostas e com quais comissões.

## Overview
Atualmente o MVP opera com contexto aberto (o usuário pode escolher livremente os `commercial_context` e % de comissão na tela). Este módulo visa adicionar governança sobre a API e os cenários.

### Key Capabilities Planejadas
- **Perfis (RBAC):** `admin` (Construtora - pode alterar tabelas), `manager` (Imobiliária - pode ver comissões da equipe), `broker` (Corretor - apenas simula).
- **Proteção da API:** Adicionar `Depends(get_current_user)` nos endpoints de roteadores FastAPI.
- **Registro Automático do Broker:** Extrair o nome da corretora do JWT em vez do input manual no frontend.

### Extension Points
O Auth Module deve, inicialmente, usar uma tabela simples e JWT local. Se necessário, uma integração com AWS Cognito ou Supabase pode ser feita como provider. 
