# Hefesto Skill Generator - Documentação de Contexto

## Visão Geral do Projeto

O **Hefesto Skill Generator** é um sistema de geração de "Agent Skills" padronizadas para múltiplos CLIs de IA, seguindo o padrão aberto [agentskills.io](https://agentskills.io) e as melhores práticas academicamente consolidadas. O nome vem do deus ferreiro da mitologia grega, que forjava ferramentas divinas - assim como ele, este projeto forja "ferramentas" (skills) que empoderam agentes de IA a realizar tarefas especializadas.

### Propósito Principal
- Gerar skills padronizadas para diversos CLIs de IA (Claude Code, Gemini CLI, OpenAI Codex, VS Code/Copilot, OpenCode, Cursor, Qwen Code)
- Seguir o padrão aberto Agent Skills Specification
- Implementar detecção automática de CLIs instalados
- Utilizar abordagem "template-first" com expansão guiada
- Incorporar "Human Gate" para validação humana antes de persistir

## Arquitetura e Funcionalidades

### Comandos Principais
- `/hefesto.create` - Cria skill a partir de descrição natural
- `/hefesto.extract` - Extrai skill de código/documentos existentes
- `/hefesto.validate` - Valida skill contra Agent Skills spec
- `/hefesto.adapt` - Adapta skill para outro CLI
- `/hefesto.sync` - Sincroniza skill entre CLIs
- `/hefesto.list` - Lista skills do projeto
- `/hefesto.init` - Inicializa infraestrutura Hefesto no projeto
- `/hefesto.detect` - Re-detecta CLIs instalados e adiciona novos

### Estrutura de uma Skill
```
skill-name/
├── SKILL.md              # Core (<500 linhas, <5000 tokens)
├── scripts/              # Código executável
│   ├── validate.py
│   └── execute.sh
├── references/           # Documentação detalhada
│   ├── REFERENCE.md
│   └── EXAMPLES.md
└── assets/               # Recursos estáticos
    ├── templates/
    └── schemas/
```

### Fluxo de Geração de Skills
1. **TEMPLATE-FIRST**: Carregar skill-template.md, extrair conceitos-chave da descrição, gerar SKILL.md inicial
2. **HUMAN GATE**: Apresentar skill gerada, validar contra Agent Skills spec, opções: [approve] [expand] [edit] [reject]
3. **WIZARD INTERATIVO** (opcional): Perguntas sobre scripts, referências e CLIs
4. **GERAÇÃO MULTI-CLI**: Detectar CLIs instalados, gerar estrutura para cada CLI, criar sub-arquivos JIT

## Regras de Arquitetura (T0 - Absolutas)

As seguintes regras são invioláveis no projeto:

1. **T0-HEFESTO-01**: Todas as skills devem seguir a especificação Agent Skills
2. **T0-HEFESTO-02**: Human Gate obrigatório - nunca persistir sem aprovação humana
3. **T0-HEFESTO-03**: Progressive Disclosure - SKILL.md < 500 linhas e < 5000 tokens
4. **T0-HEFESTO-04**: Nomenclatura padrão - nome deve seguir formato específico (lowercase, hyphens, max 64 chars)
5. **T0-HEFESTO-05**: Descrição obrigatória com "Use when:" ou similar
6. **T0-HEFESTO-06**: Detecção automática de CLIs antes de perguntar ao usuário
7. **T0-HEFESTO-07**: Validação pré-persistência contra a especificação
8. **T0-HEFESTO-08**: Operações devem ser idempotentes
9. **T0-HEFESTO-09**: Armazenamento local no projeto atual por padrão
10. **T0-HEFESTO-10**: Skills técnicas devem citar fontes

## Diretórios Suportados
- Claude Code: `.claude/skills/<name>/`
- Gemini CLI: `.gemini/skills/<name>/`
- OpenAI Codex: `.codex/skills/<name>/`
- VS Code/Copilot: `.github/skills/<name>/`
- OpenCode: `.opencode/skills/<name>/`
- Cursor: `.cursor/skills/<name>/`
- Qwen Code: `.qwen/skills/<name>/`

## Desenvolvimento e Convenções

### Princípios de Desenvolvimento
- **Progressive Disclosure**: Informações detalhadas em sub-arquivos JIT
- **Validação Contínua**: Conformidade com Agent Skills spec
- **Segurança por Padrão**: Sanitização de entradas e saídas, princípio do menor privilégio
- **Compatibilidade Multi-CLI**: Geração para todos os CLIs detectados automaticamente

### Estrutura de Arquitetura
O projeto utiliza um sistema de tiers para organização de regras:
- **T0**: Regras absolutas (inválidas)
- **T1**: Regras normativas
- **T2**: Informações contextuais
- **T3**: Exemplos ilustrativos

### Arquivos Importantes
- `CONSTITUTION.md`: Regras invioláveis do sistema
- `.context/`: Contexto para IAs
- `commands/`: Implementações dos comandos principais
- `docs/`: Documentação para humanos
- `docs/cards/`: CARDs de implementação

## Considerações de Segurança
- Validação de entradas contra injeção de prompts
- Sanitização de saídas antes de execução
- Não inclusão de credenciais, tokens ou secrets
- Aplicação do princípio do menor privilégio