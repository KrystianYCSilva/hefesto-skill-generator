# Investigação Técnica: Slash Commands em CLIs de IA para Programação

> Escopo: Como desenvolvedores podem **entender, estender ou adicionar slash commands**
> em CLIs de IAs voltadas para programação/código.  
> Fontes: Documentações oficiais + releases recentes (últimos 6 meses).  
> Plataforma: Agnóstico (Linux / macOS / Windows).

---

## Conceito Geral: O que são Slash Commands em CLIs de IA

Em CLIs de IA para código, **slash commands (`/`) não são comandos shell tradicionais**.
Eles funcionam como:

- **roteadores semânticos**
- **atalhos de prompt estruturado**
- **gatilhos de pipelines internos**
- **interfaces de extensão (quando suportado)**

Arquiteturalmente, quase todas seguem este fluxo:

```

Input do usuário
└── Parser de linha
└── Detector de prefixo "/"
└── Command Registry
├── Handler interno
├── Prompt Template
├── Tool / Agent
└── Output Renderer

```

⚠️ Importante: **nem toda CLI permite adicionar slash commands customizados**.
Na maioria dos casos, apenas **desenvolvedores da ferramenta** podem.

---

## 1. Claude Code / Claude CLI (Anthropic)

### Como funcionam os Slash Commands
- Slash commands são **mapeamentos internos para prompts especializados**
- Ex: `/explain`, `/fix`, `/tests`, `/doc`
- Cada comando ativa:
  - um **prompt template**
  - um **context loader**
  - ferramentas internas (code analysis, diff, etc.)

### Onde são definidos
- Definições **hardcoded no CLI**
- Sem registro público de plugins ou hooks
- Parsing ocorre antes do envio ao modelo

### Extensibilidade para desenvolvedores
❌ **Não suportado oficialmente**

Não há:
- API de registro
- Plugins
- Arquivos de configuração para novos comandos

### Alternativa recomendada
- Criar **wrappers externos**:
  - shell scripts
  - aliases
  - CLIs intermediárias que geram prompts

### Documentação oficial
- Anthropic Claude Code Docs
- Claude Code Release Notes (últimos releases)

---

## 2. Gemini CLI (Google)

### Arquitetura dos Slash Commands
- Slash commands são **shortcuts para “Prompt Presets”**
- Integrados ao fluxo de ferramentas do Gemini Code Assist
- Ex: `/explain`, `/refactor`, `/test`

### Implementação
- Parser interno → Prompt Router → Gemini API
- Comandos definidos via **catálogo interno**

### Extensão por desenvolvedores
❌ **Não permitido**

Não existe:
- Plugin system
- Command registry externo
- Arquivo declarativo (YAML/JSON)

### Possível workaround
- Usar **scripts externos** chamando Gemini API
- Criar sua própria CLI sobre a API Gemini

### Docs oficiais
- Gemini CLI Documentation
- Gemini Code Assist CLI Releases

---

## 3. GitHub Copilot CLI

### Como funcionam os Slash Commands
- Slash commands mapeiam para **scenarios**
- Ex: `/explain`, `/fix`, `/suggest`
- Internamente:
  - command → scenario → prompt template

### Registro de comandos
- Definidos no código do CLI (Node.js)
- Cada comando possui:
  - schema de entrada
  - prompt
  - renderer

### Extensibilidade
❌ **Não há suporte oficial para adicionar novos slash commands**

### O que é possível
- Fork do CLI
- Modificação direta do registry interno
- Uso de aliases shell

### Documentação
- GitHub Copilot CLI Docs
- Copilot CLI GitHub Repository (releases)

---

## 4. Cursor IDE / Cursor CLI

### Diferença importante
Cursor é **IDE-first**, não CLI-first.

### Slash Commands
- Slash commands fazem parte do **Chat interno**
- Ex: `/edit`, `/fix`, `/explain`
- Ligados a:
  - AST do projeto
  - contexto de arquivos abertos

### Arquitetura
```

Slash Command
└── Action Resolver
└── Code Context Extractor
└── Model Call

````

### Extensibilidade
❌ **Usuários/desenvolvedores não podem registrar novos slash commands**

Não existe:
- Plugin API para slash commands
- Configuração declarativa

### Observação
Cursor permite **custom instructions**, mas **não novos comandos**

---

## 5. Qwen Code CLI (Alibaba)

### Estado atual
- CLI ainda em **rápida evolução**
- Slash commands usados como **modos de operação**

### Implementação
- Comandos mapeiam para:
  - perfis de prompt
  - modos (chat, code, refactor)

### Extensão
❌ **Nenhum mecanismo oficial documentado**
- Sem plugin system
- Sem registry público

### Possível caminho
- Uso direto da API Qwen
- Construção de CLI customizada

---

## 6. OpenCode

### Diferencial importante ✅
OpenCode é **a mais extensível do grupo**.

### Slash Commands
- Definidos como **comandos declarativos**
- Podem ser:
  - scripts
  - prompts
  - pipelines

### Como adicionar comandos
✔️ **Suportado oficialmente**

Normalmente via:
- arquivos de configuração (YAML / JSON)
- diretório de comandos
- bindings para scripts

### Exemplo conceitual
```yaml
commands:
  explain:
    prompt: "Explique o código a seguir"
  test:
    script: "./run-tests.sh"
```

### Documentação

* OpenCode CLI Docs
* OpenCode GitHub Releases

---

## 7. Codex CLI (OpenAI – estado atual)

### Slash Commands

* Funcionam como **aliases semânticos**
* Traduzidos para prompts estruturados

### Extensibilidade

❌ **Não documentada oficialmente**

* Sem plugins
* Sem API pública de registro

### Alternativa

* Criar CLIs customizadas usando OpenAI API
* Usar wrappers + templates

---

## Tabela Comparativa

| Ferramenta    | Slash Commands | Extensível | Plugins    | Config Declarativa |
| ------------- | -------------- | ---------- | ---------- | ------------------ |
| Claude Code   | Sim            | ❌ Não      | ❌          | ❌                  |
| Gemini CLI    | Sim            | ❌ Não      | ❌          | ❌                  |
| Copilot CLI   | Sim            | ❌ Não      | ❌          | ❌                  |
| Cursor        | Sim (IDE)      | ❌ Não      | ❌          | ❌                  |
| Qwen Code CLI | Sim            | ❌ Não      | ❌          | ❌                  |
| Codex CLI     | Sim            | ❌ Não      | ❌          | ❌                  |
| **OpenCode**  | Sim            | ✔️ Sim     | ⚠️ Parcial | ✔️ Sim             |

---

## Conclusões Técnicas

1. **Slash commands não são um padrão aberto**
2. Na maioria das CLIs:

    * são atalhos internos
    * não extensíveis
3. **OpenCode é a exceção**
4. Para extensibilidade real:

    * criar sua própria CLI
    * ou usar wrappers + APIs
5. Tendência atual:

    * foco em UX
    * pouco interesse em plugin ecosystems (por enquanto)