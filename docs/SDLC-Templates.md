# Guia Prático: Templates SDLC e Exemplos de Implementação

## Seção 1: Templates Essenciais de Documentação

### 1.1 Template SRS (Software Requirements Specification)

```markdown
# Software Requirement Specification (SRS)
## Versão 1.0 | Data: 2025-01-15

### 1. Identificação do Projeto
- **Nome do Projeto:** [Nome]
- **Cliente/Sponsor:** [Nome]
- **Data de Início:** [Data]
- **Data Estimada de Conclusão:** [Data]
- **Responsável:** [Nome]

### 2. Propósito do Documento
Este documento define os requisitos funcionais e não-funcionais para [projeto].

### 3. Escopo
**Incluído:**
- Funcionalidade A
- Funcionalidade B
- Integração com Sistema X

**Excluído:**
- Funcionalidade C (planeada para v2.0)
- Integração com Sistema Y

### 4. Definições e Acrônimos
| Acrônimo | Significado |
|----------|-------------|
| API | Application Programming Interface |
| JWT | JSON Web Token |

### 5. Requisitos Funcionais

#### RF-001: Autenticação de Usuário
**Descrição:** O sistema deve permitir autenticação segura via email/senha
**Tipo:** Funcional
**Prioridade:** Alta
**Ator:** Usuário
**Pré-condições:** 
- Usuário não autenticado
- Conta ativa no sistema

**Fluxo Principal:**
1. Usuário clica em "Login"
2. Sistema exibe formulário de autenticação
3. Usuário insere email e senha
4. Sistema valida credenciais
5. Se válidas, cria sessão e redireciona para dashboard
6. Se inválidas, exibe mensagem de erro

**Pós-condições:** Usuário autenticado com sessão válida

**Critérios de Aceitação:**
- [ ] Senha é criptografada com bcrypt
- [ ] Rate limiting: máx 5 tentativas por minuto
- [ ] Mensagem de erro não revela se email existe
- [ ] Token JWT válido por 24h
- [ ] Logout funciona corretamente

#### RF-002: Gerenciamento de Perfil
**Descrição:** Usuário pode atualizar dados de perfil
**Tipo:** Funcional
**Prioridade:** Média
...

### 6. Requisitos Não-Funcionais

#### RNF-001: Performance
- Tempo de resposta < 200ms para 95% das requisições
- Suportar 1000 usuários simultâneos
- Cache implementado para consultas frequentes

#### RNF-002: Segurança
- HTTPS obrigatório
- OWASP Top 10 compliance
- Penetration testing bienal

#### RNF-003: Escalabilidade
- Arquitetura em microserviços
- Horizontal scaling via Kubernetes
- Suportar 10x crescimento em 12 meses

#### RNF-004: Usabilidade
- Interface responsiva (mobile-first)
- WCAG 2.1 Level AA accessibility
- Suporte multilíngue (PT, EN, ES)

### 7. Restrições e Limitações
- Baseado em .NET Framework
- Banco de dados SQL Server
- Deploy em AWS
- Orçamento máximo: R$ 500k

### 8. Dependências
- API externa de pagamento (Stripe)
- Serviço de email (SendGrid)
- CDN para assets (CloudFlare)

### 9. Aprovações
- [ ] Product Manager: ______ Data: ______
- [ ] Tech Lead: ______ Data: ______
- [ ] Cliente: ______ Data: ______
```

### 1.2 Template RTM (Requirements Traceability Matrix)

```markdown
# Requirements Traceability Matrix (RTM)

| Req ID | Descrição | Tipo | Prioridade | Test Case ID | Status | Notas |
|--------|-----------|------|------------|--------------|--------|-------|
| RF-001 | Autenticação via Email | Func | Alta | TC-001, TC-002 | ✅ Completo | |
| RF-002 | Reset de Senha | Func | Alta | TC-003, TC-004 | 🔄 Em Teste | |
| RF-003 | 2FA via SMS | Func | Média | TC-005 | 📋 Planejado | |
| RNF-001 | Tempo de resposta <200ms | Perf | Alta | TC-006 | 🔄 Em Teste | |
| RNF-002 | HTTPS obrigatório | Segurança | Alta | TC-007 | ✅ Completo | |

## Rastreabilidade Bidirecional

**Forward Traceability (Req → Test):**
- RF-001 → TC-001, TC-002 ✅

**Backward Traceability (Test → Req):**
- TC-001 → RF-001 ✅

## Matriz de Cobertura

| Fase | Requisitos | Desenvolvidos | Testados | Taxa Cobertura |
|------|-----------|---------------|----------|----------------|
| Planning | 15 | 15 | 15 | 100% |
| Development | - | 12 | 0 | 80% |
| Testing | - | - | 10 | 67% |
```

### 1.3 Template HLD (High-Level Design)

```markdown
# High-Level Design (HLD)

## 1. Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────┐
│                Cliente (Browser)                │
└────────────────┬────────────────────────────────┘
                 │ HTTPS
                 ▼
┌─────────────────────────────────────────────────┐
│              API Gateway (Kong)                 │
├─────────────────────────────────────────────────┤
│ - Autenticação JWT                              │
│ - Rate Limiting                                 │
│ - Request/Response Logging                      │
└────────┬─────────────────────┬──────────────────┘
         │                     │
         ▼                     ▼
  ┌────────────┐       ┌─────────────┐
  │Auth Service│       │User Service │
  └────┬───────┘       └──────┬──────┘
       │                      │
       ▼                      ▼
  [PostgreSQL]         [PostgreSQL]
```

## 2. Componentes Principais

### 2.1 API Gateway
- **Tecnologia:** Kong API Gateway
- **Responsabilidade:** Roteamento, autenticação, rate limiting
- **Escalabilidade:** Horizontal via Docker Swarm

### 2.2 Auth Service
- **Tecnologia:** Node.js + Express
- **Responsabilidade:** Gerenciamento de autenticação e autorização
- **Banco de Dados:** PostgreSQL
- **Cache:** Redis para tokens

### 2.3 User Service
- **Tecnologia:** .NET 6
- **Responsabilidade:** Gerenciamento de perfis de usuário
- **Banco de Dados:** SQL Server
- **Cache:** Redis

## 3. Padrões de Design

### 3.1 Autenticação
- **Tipo:** Token-based (JWT)
- **Flow:** OAuth 2.0 + OpenID Connect
- **Expiração:** 24 horas para access token

### 3.2 Comunicação Inter-serviços
- **Protocolo:** REST com JSON
- **Retry:** Exponential backoff (3 tentativas)
- **Timeout:** 10 segundos

### 3.3 Persistência de Dados
- **Padrão:** Repository Pattern
- **ORM:** Entity Framework Core (.NET), Sequelize (Node.js)

## 4. Segurança
- HTTPS em todas as comunicações
- Secrets em environment variables
- Validação de input em todos os endpoints
- CORS restrito a domínios conhecidos

## 5. Performance e Escalabilidade
- CDN para assets estáticos (CloudFlare)
- Caching em múltiplas camadas (Redis, HTTP cache)
- Database indexes otimizados
- Connection pooling em todos os serviços

## 6. Monitoramento e Logging
- **Logs centralizados:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **APM:** New Relic ou DataDog
- **Alertas:** PagerDuty para críticos
```

### 1.4 Template LLD (Low-Level Design)

```markdown
# Low-Level Design (LLD) - Auth Service

## 1. Estrutura de Diretórios

```
src/
├── controllers/
│   └── AuthController.ts
├── services/
│   └── AuthService.ts
├── repositories/
│   └── UserRepository.ts
├── models/
│   └── User.ts
├── middleware/
│   ├── JWTMiddleware.ts
│   └── ErrorHandler.ts
├── utils/
│   ├── PasswordHasher.ts
│   └── JWTGenerator.ts
├── config/
│   └── Database.ts
└── tests/
    ├── unit/
    └── integration/
```

## 2. Pseudocódigo - AuthController

```pseudocode
CLASS AuthController
  
  METHOD login(email: string, password: string): Response
    BEGIN
      // Validação de input
      IF email é vazio OR password é vazio THEN
        RETURN BadRequest("Email e senha obrigatórios")
      END IF
      
      // Rate limiting
      attempts := redis.get(f"login_attempts:{email}")
      IF attempts >= 5 THEN
        RETURN TooManyRequests("Muitas tentativas, tente depois")
      END IF
      
      // Buscar usuário
      user := userRepository.findByEmail(email)
      IF user é NULL THEN
        redis.increment(f"login_attempts:{email}", 1)
        RETURN Unauthorized("Email ou senha inválidos")
      END IF
      
      // Validar senha
      IF NOT passwordHasher.verify(password, user.passwordHash) THEN
        redis.increment(f"login_attempts:{email}", 1)
        RETURN Unauthorized("Email ou senha inválidos")
      END IF
      
      // Gerar tokens
      accessToken := jwtGenerator.generate(user.id, "24h")
      refreshToken := jwtGenerator.generate(user.id, "7d", "refresh")
      
      // Limpar tentativas
      redis.delete(f"login_attempts:{email}")
      
      // Registrar login
      auditLog.record(user.id, "LOGIN", "Sucesso")
      
      RETURN Success({
        accessToken: accessToken,
        refreshToken: refreshToken,
        user: user
      })
    END
  END METHOD
  
END CLASS
```

## 3. Diagrama de Sequência - Login

```
Cliente          API Gateway    AuthController   UserRepository   Database
  │                 │                │                 │              │
  │─────Login───────>│                │                 │              │
  │            JWT Validation         │                 │              │
  │                 │───Validate──────>                 │              │
  │                 │<────Valid───────│                 │              │
  │                 │────FindUser────────────────────>  │              │
  │                 │                 │                 │              │
  │                 │                 │                 │──Query────────>
  │                 │                 │                 │<─User────────│
  │                 │                 │                 │              │
  │                 │     Verify Password               │              │
  │                 │─────Generate Token─>              │              │
  │                 │<────Token────────                 │              │
  │<────Token───────│                                   │              │
```

## 4. Classes e Métodos

### AuthService
```typescript
class AuthService {
  private userRepository: UserRepository;
  private passwordHasher: PasswordHasher;
  private jwtGenerator: JWTGenerator;
  private redisClient: Redis;
  
  async authenticate(email: string, password: string): Promise<AuthResponse> {
    // Implementação conforme pseudocódigo
  }
  
  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    // Validar refresh token
    // Gerar novo access token
  }
  
  async logout(userId: string): Promise<void> {
    // Invalidar refresh tokens
  }
}
```

## 5. Padrões Usados

- **Repository Pattern:** Abstração de acesso a dados
- **Dependency Injection:** Injetar dependências via construtor
- **Middleware Pattern:** Executar logic antes de resolver requisição
- **Observer Pattern:** Event-driven logging

## 6. Tratamento de Erros

| Cenário | Status | Mensagem |
|---------|--------|----------|
| Email/Senha vazio | 400 | "Email e senha obrigatórios" |
| Usuário não existe | 401 | "Email ou senha inválidos" |
| Senha incorreta | 401 | "Email ou senha inválidos" |
| Muitas tentativas | 429 | "Muitas tentativas, tente depois" |
| Erro BD | 500 | "Erro interno do servidor" |
```

### 1.5 Template Test Plan

```markdown
# Test Plan

## 1. Objetivo
Validar que o sistema atende todos os requisitos funcionais e não-funcionais antes da implantação em produção.

## 2. Escopo
- Testes de funcionalidade: Todos os RF
- Testes de performance: Todos os RNF
- Testes de segurança: Penetration testing
- **Fora do escopo:** Testes de compatibilidade com navegadores legados

## 3. Estratégia de Teste

### 3.1 Níveis de Teste
| Nível | Objetivo | % de Cobertura | Ferramentas |
|-------|----------|----------------|------------|
| Unit | Testar funções individuais | 80% | Jest, pytest |
| Integration | Testar comunicação entre módulos | 70% | Postman |
| System | Testar sistema completo | 85% | Selenium |
| UAT | Validar com usuários reais | 100% | Manual |

### 3.2 Tipos de Teste
- **Smoke Testing:** Verificar funcionalidades críticas
- **Regression Testing:** Garantir que mudanças não quebram existentes
- **Performance Testing:** Verificar tempo de resposta (<200ms)
- **Security Testing:** OWASP Top 10, Penetration testing
- **Load Testing:** Simular 1000 usuários simultâneos

## 4. Casos de Teste

### TC-001: Login com Credenciais Válidas
**Pré-condição:** Usuário cadastrado e ativo
**Steps:**
1. Navegar para página de login
2. Inserir email válido
3. Inserir senha válida
4. Clicar em "Login"

**Resultado Esperado:**
- Usuário redirecionado para dashboard
- Token JWT armazenado em cookie seguro
- Mensagem de boas-vindas exibida

**Prioridade:** P0 (Crítica)

### TC-002: Login com Senha Incorreta
**Pré-condição:** Usuário cadastrado
**Steps:**
1. Inserir email válido
2. Inserir senha incorreta
3. Clicar em "Login"

**Resultado Esperado:**
- Erro "Email ou senha inválidos"
- Usuário não autenticado
- Contador de tentativas incrementa

**Prioridade:** P0 (Crítica)

### TC-003: Rate Limiting (5+ tentativas)
**Pré-condição:** 4 tentativas falhadas
**Steps:**
1. Inserir email válido
2. Inserir senha incorreta
3. Clicar em "Login" (5ª tentativa)

**Resultado Esperado:**
- Erro "Muitas tentativas, tente depois"
- Sistema bloqueia por 1 minuto

**Prioridade:** P1 (Alta)

## 5. Cronograma de Testes
| Fase | Período | Responsável |
|------|---------|------------|
| Teste Unitário | Semana 3-4 | Desenvolvedores |
| Teste Integração | Semana 5 | QA |
| Teste Sistema | Semana 6 | QA |
| UAT | Semana 7 | Cliente |

## 6. Critérios de Saída
- [ ] 80% cobertura de testes unitários
- [ ] Todas as funções críticas testadas
- [ ] 0 bugs críticos abertos
- [ ] Performance <200ms para 95% requisições
- [ ] UAT aprovado pelo cliente
- [ ] Penetration testing sem falhas críticas
```

---

## Seção 2: Exemplos de Slash Commands Práticos

### 2.1 Slash Command Completo: /sdlc-review

Arquivo: `.claude/commands/sdlc-review.md`

```markdown
---
allowed-tools: Read, Bash(git log:*, git diff:*)
argument-hint: [file-path] [phase]
description: Revisa código/documentação contra SDLC standards
---

# SDLC Review: $1 (Phase: $2)

## Context

Current file: @$1
Current phase: $2
Git log: !`git log --oneline -5`
Recent changes: !`git diff HEAD~1`

## Review Checklist

### Documentação (Planning/Requirements)
- [ ] Documento versionado com data e autor
- [ ] Escopo claramente definido
- [ ] Requisitos são SMART (Specific, Measurable, Achievable, Relevant, Timely)
- [ ] Critérios de aceitação definidos
- [ ] Riscos identificados
- [ ] Aprovações coletadas

### Design
- [ ] HLD documenta arquitetura geral
- [ ] LLD tem pseudocódigo detalhado
- [ ] Componentes seguem SOLID
- [ ] Diagramas UML presentes
- [ ] Design patterns identificados
- [ ] Segurança considerada desde início

### Implementação
- [ ] Código segue padrões estabelecidos
- [ ] Nomes de variáveis descritivos
- [ ] Funções pequenas (<20 linhas)
- [ ] Sem duplicação de código (DRY)
- [ ] Tratamento de erros apropriado
- [ ] Testes unitários inclusos
- [ ] Documentação inline quando complexo

### Testes
- [ ] Test cases mapeados para requisitos
- [ ] Casos de sucesso cobertos
- [ ] Casos de erro cobertos
- [ ] Edge cases considerados
- [ ] Dados de teste preparados
- [ ] Resultados esperados claros

### Deployment
- [ ] Plano de implantação documento
- [ ] Rollback strategy definida
- [ ] Backup considerado
- [ ] Monitoramento planejado
- [ ] Checklist de pré-deployment

## Análise SOLID

**S - Single Responsibility:**
Cada classe/módulo tem uma única razão para mudar? $1

**O - Open/Closed:**
Fácil de estender sem modificar código existente?

**L - Liskov Substitution:**
Subtipos são substituíveis de forma segura?

**I - Interface Segregation:**
Interfaces são específicas ao que o cliente precisa?

**D - Dependency Inversion:**
Depende de abstrações, não de implementações?

## Security Checklist

- [ ] Validação de entrada em todos endpoints
- [ ] Autenticação obrigatória para recursos sensíveis
- [ ] Autorização baseada em roles implementada
- [ ] Senhas criptografadas com algoritmo forte (bcrypt)
- [ ] HTTPS ativado
- [ ] CORS configurado restritamente
- [ ] Rate limiting ativo
- [ ] Logs de segurança criados
- [ ] Secrets em environment variables
- [ ] SQL injection prevenido (prepared statements)

## Performance

- [ ] Queries otimizadas com indexes
- [ ] N+1 queries problem resolvido
- [ ] Cache implementado onde necessário
- [ ] Lazy loading considerado
- [ ] Compressão de responses ativa
- [ ] Assets minificados
- [ ] CDN configurado

## Quality Metrics

- Code Coverage: Deve ser >= 70%
- Cyclomatic Complexity: Deve ser < 10
- Duplicação: Deve ser < 5%
- Technical Debt: Deve estar diminuindo

## Recomendações

[Forneça recomendações específicas baseado na review]
```

### 2.2 Slash Command: /rtm-generator

Arquivo: `.claude/commands/rtm-generator.md`

```markdown
---
allowed-tools: Read, Write
argument-hint: [requirement-file] [test-file]
description: Gera Requirements Traceability Matrix
---

# RTM Generator

Arquivos:
- Requisitos: @$1
- Testes: @$2

## Análise

1. Extraia todos os Requirement IDs de @$1
2. Extraça todos os Test Case IDs de @$2
3. Mapeie relacionamentos entre requisitos e testes
4. Identifique requisitos sem testes (gaps)
5. Identifique testes sem requisitos (escopo extra)

## Matriz Gerada

| Req ID | Descrição | Test Case | Status | Coverage |
|--------|-----------|-----------|--------|----------|
| [Será preenchido baseado em análise] |

## Análise de Gaps

### Requisitos sem testes
[Liste requisitos que não têm testes associados]

### Testes sem requisitos
[Liste testes que não mapeiam para requisitos]

### Recomendações
1. [Criar testes para requisitos descobertos]
2. [Revisar testes extras para escopo creep]
3. [Priorizar cobertura de requisitos críticos]
```

---

## Seção 3: Fluxo Completo SDLC com Exemplos

### 3.1 Exemplo: Implementar Sistema de Notificações

**Semana 1: Planning & Requirements**

```
1. /sdlc-checklist "Notification System" "Planning"
   ↓ Documentar escopo e objetivos
   ↓ Criar SRS com requisitos

2. /requirements-review docs/requirements/SRS.md
   ↓ Validar requisitos contra checklist SDLC

3. Criar RTM: /rtm-generator SRS.md test-requirements.md
```

**Semana 2: Design**

```
1. Criar HLD:
   - Arquitetura com múltiplos provedores (Email, SMS, Push)
   - Queue de notificações (RabbitMQ)
   - Database para histórico

2. Criar LLD:
   - Classes: NotificationService, NotificationQueue, Provider
   - Pseudocódigo para cada método
   - Diagramas de sequência

3. /design-review docs/design/HLD.md
   ↓ Validar contra princípios SOLID
   ↓ Verificar segurança
   ↓ Checar escalabilidade

4. Design Review Meeting:
   - Tech Lead aprova HLD
   - Arquiteto aprova LLD
   - Security team aprova security design
```

**Semana 3-4: Development**

```
1. Setup do projeto:
   - Estrutura de diretórios
   - Testes unitários skeleton
   - Configuração CI/CD

2. Implementar NotificationService:
   /git-commit-msg
   feat(notifications): add base NotificationService

3. Para cada commit:
   - Code review obrigatório
   - /code-quality src/services/NotificationService.ts
   - Testes unitários devem passar
   - Cobertura >= 80%

4. Implementar Providers (Email, SMS):
   - Seguir mesmo padrão
   - Herdar de BaseProvider (polimorfismo)
   - Testes para cada provider

5. Integração com Database:
   - Repository pattern
   - Migrations versionadas
   - Testes de integração
```

**Semana 5: Testing**

```
1. /test-strategy "Notification System"
   ↓ Definir tipos de testes
   ↓ Preparar dados de teste

2. Unit Tests:
   - Teste cada provider isoladamente
   - Mock das dependências
   - Teste casos de erro
   - Meta: 85% coverage

3. Integration Tests:
   - Teste fluxo completo (requisição → BD)
   - Teste fila de notificações
   - Teste retry logic

4. System Tests:
   - Teste toda pipeline de notificações
   - Teste com dados realistas
   - Teste escalabilidade

5. UAT:
   - Cliente testa todas as funcionalidades
   - Testa scenarios do mundo real
   - Aprova user stories
```

**Semana 6: Deployment**

```
1. /sdlc-document "DeploymentPlan"
   - Ambiente de staging idêntico ao prod
   - Rollback strategy
   - Backup strategy

2. Deployment em Staging:
   - Teste em ambiente de produção
   - Teste performance sob carga
   - Teste monitoramento

3. Deployment em Produção:
   - Canary deployment (1% tráfego)
   - Monitor metod detentamente
   - Escalar para 100%

4. Manutenção:
   - Monitor logs
   - Rastrear performance
   - Coletar feedback

5. /sdlc-checklist "Notification System" "Maintenance"
   - Verificar SLAs
   - Planejar melhorias
```

---

## Seção 4: Métricas e KPIs para Monitoramento

### 4.1 Dashboard SDLC

```markdown
# SDLC Metrics Dashboard

## Qualidade do Código

| Métrica | Meta | Atual | Status |
|---------|------|-------|--------|
| Code Coverage | 80% | 82% | ✅ OK |
| Cyclomatic Complexity | <10 | 8.5 | ✅ OK |
| Duplicação | <5% | 2.1% | ✅ OK |
| Security Issues | 0 Critical | 0 | ✅ OK |
| Technical Debt | Decreasing | -5% | ✅ OK |

## Teste

| Métrica | Meta | Atual | Status |
|---------|------|-------|--------|
| Test Pass Rate | 100% | 98% | ⚠️ Atenção |
| Test Coverage | 80% | 82% | ✅ OK |
| Defect Escape Rate | <5% | 2% | ✅ OK |
| Mean Time to Remediate | <48h | 24h | ✅ OK |

## Deployment

| Métrica | Meta | Atual | Status |
|---------|------|-------|--------|
| Deployment Frequency | 1x/semana | 2x/semana | ✅ OK |
| Lead Time | <7 dias | 5 dias | ✅ OK |
| MTTR | <1h | 45min | ✅ OK |
| Change Failure Rate | <15% | 5% | ✅ OK |

## Negócio

| Métrica | Meta | Atual | Status |
|---------|------|-------|--------|
| Requisitos Completos | 100% | 85% | 🔄 20% |
| Escopo Controlado | <10% creep | 5% | ✅ OK |
| Satisfação do Cliente | >8/10 | 8.5/10 | ✅ OK |
| ROI | >150% | 180% | ✅ OK |
```

---

## Conclusão

Este documento fornece templates prontos para uso imediato no SDLC de qualquer projeto. Adapte conforme necessário para seu contexto específico.
