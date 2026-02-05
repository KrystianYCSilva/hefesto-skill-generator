# **Protocolos Avançados de Engenharia Cognitiva e Arquitetura de Agentes Autônomos: Um Tratado sobre Prompt Engineering, Skills e Orquestração**

## **Introdução: A Transição da Arte para a Engenharia de Sistemas**

A interação entre humanos e sistemas de inteligência artificial generativa passou por uma metamorfose radical nos últimos anos. O que inicialmente se manifestava como uma prática empírica e quase artesanal de "Engenharia de Prompt" — a tentativa e erro de formular frases para obter uma resposta coerente — consolidou-se agora como uma disciplina rigorosa de engenharia de software e design de sistemas cognitivos. À medida que os Grandes Modelos de Linguagem (LLMs) evoluíram de simples completadores de texto para motores de raciocínio complexo, a necessidade de protocolos estruturados, definições de comportamento persistentes (Skills) e orquestração programática tornou-se imperativa para o desenvolvimento de aplicações robustas.

Este relatório técnico explora a fronteira atual da engenharia de prompt e da arquitetura de agentes, sintetizando dados de documentações oficiais de provedores de elite (OpenAI, Anthropic, Google, DeepSeek, Alibaba Cloud), pesquisas acadêmicas recentes e práticas de comunidade em ambientes de desenvolvimento integrados como o Cursor e o VS Code. O objetivo é dissecar não apenas *o que* dizer ao modelo, mas *como* arquitetar o ambiente onde o modelo opera, manipulando parâmetros de amostragem, janelas de contexto e definições de ferramentas para atingir níveis de autonomia e precisão anteriormente inatingíveis.

Analisaremos a divergência crítica entre modelos de chat convencionais e a nova classe de modelos de raciocínio (como DeepSeek-R1 e OpenAI o1), cujos comportamentos exigem uma reescrita completa das "melhores práticas" estabelecidas. Investigaremos a padronização emergente de "Skills" como unidades de competência modular para agentes, e a ascensão do *Programmatic Prompting* através de frameworks como DSPy e LangChain, que prometem substituir a escrita manual de prompts pela otimização algorítmica de instruções.

## ---

**Capítulo 1: Fundamentos Taxonômicos e a Teoria da Engenharia de Prompt**

A compreensão profunda da engenharia de prompt exige, primeiramente, o estabelecimento de uma taxonomia clara das técnicas disponíveis. Pesquisas recentes, incluindo levantamentos sistemáticos realizados em 2024 e 2025, identificaram e catalogaram dezenas de técnicas de prompting distintas, organizando-as em categorias funcionais que vão desde a simples instrução até arquiteturas de agentes complexas. A literatura acadêmica aponta que a eficácia de um prompt não reside apenas na sua clareza semântica, mas na sua capacidade de ativar mecanismos específicos de atenção e recuperação dentro da rede neural.1

### **1.1 O Espectro do Contexto: De Zero-Shot a Few-Shot**

A distinção fundamental na engenharia de prompt reside na quantidade de contexto e exemplos fornecidos ao modelo antes da execução da tarefa. O *Zero-Shot Prompting* baseia-se na premissa de que o modelo, durante seu pré-treinamento massivo, já internalizou a compreensão da tarefa e requer apenas um comando diretivo para executá-la. Esta abordagem, embora eficiente em termos de tokens, muitas vezes falha em capturar nuances específicas de formato ou estilo desejadas pelo usuário.3

Em contraste, o *Few-Shot Prompting* introduz o conceito de *In-Context Learning* (ICL), onde o engenheiro fornece um conjunto de exemplos (exemplares) de entrada e saída desejada dentro do prompt. Estudos indicam que a eficácia do *Few-Shot* depende criticamente de decisões de design como a quantidade de exemplares, sua ordenação e a distribuição dos rótulos. Curiosamente, a precisão dos exemplos pode ser menos importante do que a sua estrutura; o modelo muitas vezes aprende o formato e a intenção da tarefa mesmo se os rótulos dos exemplos contiverem erros factuais, demonstrando que o mecanismo de atenção prioriza padrões estruturais sobre a veracidade semântica em certos contextos.2

No entanto, uma das descobertas mais disruptivas recentes é a inversão dessa lógica para modelos de raciocínio avançado. Conforme documentado para modelos como o DeepSeek-R1, a introdução de exemplos *few-shot* pode, paradoxalmente, degradar a performance. Isso ocorre porque esses modelos operam através de cadeias de raciocínio internas reforçadas via *Reinforcement Learning* (RL), e exemplos externos podem interferir ou colidir com os padrões de raciocínio otimizados nativamente pelo modelo. Portanto, a regra de ouro do *Few-Shot* não é mais universal, exigindo uma adaptação estratégica baseada na arquitetura do modelo alvo.4

### **1.2 Mecanismos de Geração de Pensamento (Thought Generation)**

Para tarefas que exigem lógica, matemática ou planejamento, a simples previsão do próximo token é insuficiente. A técnica de *Chain-of-Thought* (CoT) revolucionou a área ao instruir o modelo a gerar passos intermediários de raciocínio antes da resposta final. Variações dessa técnica evoluíram rapidamente:

* **Zero-Shot-CoT:** A simples adição da frase "Let's think step by step" (Vamos pensar passo a passo) demonstrou desbloquear capacidades de raciocínio latentes sem a necessidade de exemplos específicos.2  
* **Step-Back Prompting:** Envolve instruir o modelo a primeiro abstrair a pergunta para um conceito ou princípio de nível superior, e então aplicar esse princípio ao problema específico, melhorando a precisão em tarefas que exigem generalização.2  
* **Analogical Prompting:** Solicita ao modelo que gere seus próprios exemplos análogos ao problema apresentado antes de tentar resolvê-lo, facilitando a transferência de conhecimento.2

A evolução mais sofisticada dessas técnicas manifesta-se em estruturas não-lineares como *Tree of Thoughts* (ToT) e *Graph of Thoughts* (GoT). Diferentemente do CoT, que segue uma linha linear, o ToT permite que o modelo explore múltiplos caminhos de raciocínio simultaneamente, avalie a promessa de cada ramo e realize *backtracking* (retrocesso) se um caminho se mostrar infrutífero. Isso mimetiza processos cognitivos humanos de planejamento e deliberação, sendo particularmente eficaz em tarefas de escrita criativa, jogos de lógica e problemas combinatórios onde a primeira intuição nem sempre é a correta.5

### **1.3 Decomposição e Crítica**

Para enfrentar a complexidade, estratégias de decomposição como *Least-to-Most Prompting* quebram problemas complexos em subproblemas sequenciais. O modelo resolve primeiro o componente mais simples, e sua resposta é anexada ao contexto para resolver o próximo passo, garantindo consistência e reduzindo a carga cognitiva em cada etapa de inferência.2

Paralelamente, técnicas de *Self-Criticism* e *Reflexion* introduzem a capacidade de auto-correção. Ao solicitar que o modelo critique sua própria saída anterior e gere uma versão refinada, cria-se um loop de feedback autônomo. Agentes que utilizam ferramentas externas (Tool Use Agents) beneficiam-se imensamente dessa capacidade, pois podem analisar erros de execução de código ou respostas de API e ajustar suas ações subsequentes sem intervenção humana, aproximando-se de uma verdadeira autonomia agêntica.2

## ---

**Capítulo 2: Divergência Arquitetural e Protocolos de Modelos**

A era da "abordagem única" para prompts acabou. A análise das documentações técnicas do DeepSeek, Qwen e Google Gemini revela que as melhores práticas de prompt agora dependem intrinsecamente da arquitetura subjacente do modelo — se ele é um modelo denso, um *Mixture-of-Experts* (MoE), ou um modelo otimizado por Aprendizado por Reforço para raciocínio.

### **2.1 DeepSeek: A Dualidade entre V3 e R1**

A DeepSeek introduziu uma bifurcação clara em sua linha de produtos que serve como estudo de caso crítico para engenheiros de prompt. A distinção entre o DeepSeek-V3 (modelo de chat geral) e o DeepSeek-R1 (modelo de raciocínio) exige protocolos operacionais quase opostos.

#### **DeepSeek-R1: O Paradigma do Raciocínio Puro**

O modelo R1 compete diretamente com a série "o1" da OpenAI, utilizando uma cadeia de pensamento internalizada. As diretrizes para este modelo desafiam as convenções estabelecidas:

* **Abolição do System Prompt:** A documentação é enfática ao desencorajar o uso de prompts de sistema separados. Todas as instruções, incluindo definições de tarefa e restrições, devem ser encapsuladas diretamente no prompt do usuário. A separação artificial em papéis de "sistema" parece diluir a atenção do modelo em sua fase de raciocínio.4  
* **Sensibilidade à Temperatura:** Diferente de modelos criativos que operam bem com temperaturas altas (acima de 1.0), o R1 exige uma faixa estreita entre **0.5 e 0.7**, com **0.6** sendo o ponto ideal recomendado. Desvios para cima causam alucinações incoerentes, enquanto desvios para baixo (próximos de 0\) podem levar a loops de repetição de pensamento, onde o modelo fica preso em sua própria cadeia lógica.4  
* **Formatação Matemática Rígida:** Para tarefas de STEM, o engenheiro deve instruir explicitamente o modelo a encapsular a resposta final em \\boxed{}, facilitando a extração programática da solução após a longa cadeia de pensamento.4  
* **Intervenção no Processo de Pensamento:** Em casos raros onde o modelo ignora a etapa de raciocínio, pode-se forçar o comportamento iniciando a resposta do assistente (prefill) com a tag \<think\>. Isso atua como um gatilho para o modelo entrar em seu modo de análise profunda.4

#### **DeepSeek-V3: Mixture-of-Experts e Mapeamento de Temperatura**

O modelo V3, baseado em arquitetura MoE, apresenta um comportamento mais tradicional, mas com uma peculiaridade técnica importante na API. Embora a documentação permita o envio de temperature=1.0, o sistema realiza um mapeamento interno onde esse valor é convertido para uma temperatura efetiva de **0.3** no modelo. Isso é feito para garantir estabilidade nas respostas padrão. Engenheiros que desejam verdadeira aleatoriedade ou criatividade devem estar cientes desse mapeamento e ajustar os parâmetros explicitamente para valores que o sistema interprete como "alta entropia".10

### **2.2 Qwen: Modos de Pensamento e Controle de Inferência**

A série Qwen da Alibaba Cloud, especificamente as versões Qwen 2.5 e Qwen-Max, introduziu controles granulares sobre o processo de raciocínio, permitindo que desenvolvedores alternem entre modos de resposta rápida e modos de análise profunda.

* **Configuração do Thinking Mode:** Para ativar o raciocínio profundo (enable\_thinking=True), os parâmetros de amostragem recomendados diferem significativamente do padrão. Recomenda-se **Temperature=0.6**, **TopP=0.95**, e **TopK=20**. É crucial notar a recomendação explícita contra o uso de *greedy decoding* (temperatura 0), que, similarmente ao DeepSeek R1, degrada a qualidade do raciocínio.11  
* **Gestão de Contexto Multi-Turno:** Uma nuance crítica na implementação do Qwen é a gestão do histórico de conversas. O conteúdo gerado dentro das tags de pensamento (\<think\>...\</think\>) nos turnos anteriores **não** deve ser re-submetido ao modelo como parte do histórico. Apenas a resposta final deve ser mantida. Incluir o "pensamento" passado consome tokens valiosos e pode confundir o modelo, que pode tentar continuar um raciocínio antigo em vez de focar na nova instrução.11  
* **Alternância Suave (Soft Switch):** Além da configuração via API, o Qwen suporta comandos *in-prompt* como /think e /no\_think para alternar dinamicamente o comportamento de raciocínio turno a turno, oferecendo flexibilidade para agentes que precisam ora responder rápido, ora deliberar profundamente.12

### **2.3 Google Gemini: Multimodalidade e Instruções de Sistema**

O ecossistema Gemini destaca-se pela sua janela de contexto massiva e integração nativa de multimodalidade, exigindo estratégias de prompt que priorizem a organização da informação.

* **Separação de Instruções de Sistema:** A Google advoga fortemente pelo uso do campo dedicado system\_instruction na API para definir persona, regras de segurança e restrições de formato. Testes indicam que instruções colocadas neste campo têm maior "aderência" (stickiness) ao longo de conversas longas do que aquelas colocadas no início do prompt do usuário.13  
* **Estratégia Multimodal (Contexto vs. Instrução):** Ao lidar com entradas mistas (vídeo, áudio, texto), a recomendação é estruturar o prompt de forma que o contexto massivo venha primeiro, seguido pelas instruções específicas. Isso aproveita o viés de recência dos mecanismos de atenção, garantindo que a instrução de tarefa não se perca no ruído dos dados multimodais.15  
* **Function Calling Tipado:** O Gemini diferencia-se pelo rigor na definição de chamadas de função, suportando esquemas OpenAPI completos. Isso permite que o modelo atue como um tradutor confiável de linguagem natural para chamadas de API estruturadas, minimizando erros de parâmetros que são comuns em modelos menos rigorosos.16

## ---

**Capítulo 3: Skills e a Definição de Comportamento de Agentes**

A evolução dos assistentes de codificação (Coding Agents) para verdadeiros parceiros de desenvolvimento trouxe a necessidade de persistir o contexto e as regras operacionais. Surgiram assim os conceitos de "Skills" (Habilidades) e arquivos de regras de projeto, que atuam como uma memória de longo prazo configurável para o agente.

### **3.1 GitHub Copilot e a Arquitetura de Agent Skills**

O GitHub Copilot expandiu sua funcionalidade além da autocompletação para incluir "Agent Skills", diretórios especializados que o agente pode consultar sob demanda. Esta arquitetura resolve o problema da sobrecarga de contexto, permitindo que o agente carregue instruções específicas apenas quando necessário.

A definição de uma Skill baseia-se em uma estrutura de diretórios padronizada. Recomenda-se armazenar skills específicas do projeto em .github/skills/ (ou no caminho legado .claude/skills/ para compatibilidade cruzada em alguns ambientes). Skills pessoais, que viajam com o desenvolvedor entre projetos, residem em \~/.copilot/skills/.

O núcleo de uma Skill é o arquivo SKILL.md. Este arquivo deve iniciar com um cabeçalho YAML (frontmatter) que define os metadados cruciais para a descoberta da skill:

| Campo | Descrição | Restrições |
| :---- | :---- | :---- |
| name | Identificador único da skill | Minúsculas, hífen, máx. 64 chars |
| description | Explicação semântica do propósito | Máx. 1024 chars; Usado para *matching* de intenção |

O corpo do SKILL.md contém as instruções processuais. Diferente de um prompt genérico, uma skill bem projetada deve incluir scripts executáveis, templates e referências relativas a outros arquivos dentro do diretório da skill. Isso permite criar fluxos de trabalho complexos, como "Testar Aplicação Web", que não apenas instrui o modelo a escrever testes, mas fornece os scripts de setup do ambiente de teste e os templates de asserção preferidos pela equipe.18

### **3.2 Cursor Rules: O Padrão de Contexto de Projeto**

O editor Cursor popularizou o uso do arquivo .cursorrules na raiz do projeto como um mecanismo para alinhar a IA com as convenções da equipe. A análise de repositórios comunitários revela que arquivos .cursorrules eficazes seguem princípios de design específicos, focados na densidade de informação e clareza técnica.

#### **Análise de Casos: Python e FastAPI**

Um arquivo .cursorrules otimizado para um projeto Python/FastAPI 19 não apenas pede "código bom", mas especifica a stack tecnológica com precisão cirúrgica:

* **Versão e Ferramentas:** Define Python 3.12, Poetry para dependências e Alembic para migrações.  
* **Bibliotecas Obrigatórias:** Instrui o modelo a usar Pydantic para validação de dados e SQLAlchemy para ORM, evitando que o modelo sugira bibliotecas alternativas ou obsoletas.  
* **Padrões de Código:** Força o uso de *Type Hints* (dicas de tipo), docstrings em todas as funções públicas e tratamento de exceções via blocos try-except específicos.  
* **Estilo:** Exige conformidade com PEP 8 e proíbe variáveis globais.

#### **Análise de Casos: TypeScript e Next.js**

Para projetos frontend modernos, as regras 20 focam em evitar a verbosidade e alucinações de padrões antigos:

* **Diretividade:** Instruções como "DO NOT GIVE ME HIGH LEVEL SHIT" (Não me dê conteúdo de alto nível genérico) e "ACTUAL CODE OR EXPLANATION" (Código real ou explicação) são usadas para ajustar o "tom" do agente, tornando-o mais sênior e direto.  
* **Stack Moderna:** Força o uso do "App Router" do Next.js e estilização via Tailwind, prevenindo a mistura com o antigo "Pages Router" ou CSS puro.  
* **Eficiência de Resposta:** Instrui o modelo a não repetir blocos de código inalterados, focando apenas nas linhas que precisam ser modificadas, o que economiza tempo de geração e leitura.

### **3.3 Claude Skills e Execução de Código**

A Anthropic implementou um sistema de skills que se integra profundamente com a ferramenta de *Code Execution* (sandbox de análise). As skills do Claude são frequentemente empacotadas como arquivos ZIP contendo o SKILL.md e recursos auxiliares. A distinção crucial aqui é a capacidade de incluir scripts Python que o Claude pode executar para realizar tarefas determinísticas (como análise de dados ou formatação de texto complexa), delegando ao código o que é difícil para o LLM fazer via predição de tokens. A descrição no frontmatter é vital, pois é o único sinal que o roteador do Claude usa para decidir se descomprime e carrega aquela skill específica no contexto ativo.21

## ---

**Capítulo 4: Orquestração Programática e Frameworks de Agentes**

A engenharia de prompt manual, embora poderosa, não escala para sistemas complexos. A indústria está migrando para o *Programmatic Prompting*, onde os prompts são construídos, otimizados e encadeados dinamicamente por código.

### **4.1 LangChain e a Sintaxe LCEL**

O LangChain introduziu a *LangChain Expression Language* (LCEL) para resolver a complexidade de encadear chamadas de LLM. O LCEL adota uma sintaxe declarativa inspirada em *pipes* de sistemas operacionais, permitindo a composição de cadeias complexas com facilidade.

A estrutura básica chain \= prompt | model | output\_parser encapsula uma quantidade significativa de lógica de engenharia. O operador | abstrai a passagem de dados, o gerenciamento de chamadas assíncronas e a tipagem.

Por exemplo, em um sistema RAG (Retrieval-Augmented Generation), o LCEL permite definir paralelismo na recuperação de documentos e fusão de contexto de forma transparente:

Python

\# Exemplo conceitual de LCEL para RAG  
setup\_and\_retrieval \= RunnableParallel(  
    {"context": retriever, "question": RunnablePassthrough()}  
)  
chain \= setup\_and\_retrieval | prompt | model | output\_parser

Esta abordagem transforma o prompt de um bloco de texto estático em um componente de um pipeline de dados vivo, onde entradas são transformadas e injetadas dinamicamente.23

### **4.2 DSPy: A Mudança de Paradigma para Otimização**

O DSPy (*Declarative Self-improving Python*) representa um salto evolutivo, movendo-se do "prompting" para a "programação". No DSPy, o engenheiro não escreve o prompt; ele define a **Assinatura** (Signature) da tarefa.

Uma assinatura é uma declaração tipada de entradas e saídas. Por exemplo, uma assinatura para classificação de sentimentos não contém instruções como "Você é um classificador útil...", mas sim a definição dos campos:

Python

class Emotion(dspy.Signature):  
    """Classify emotion."""  
    sentence: str \= dspy.InputField()  
    sentiment: Literal\['sadness', 'joy', 'love', 'anger', 'fear', 'surprise'\] \= dspy.OutputField()

O poder do DSPy reside nos **Teleprompters** (otimizadores). Dado um conjunto de dados de validação (exemplos de entrada e saída correta), o otimizador do DSPy "compila" o programa. Ele testa diferentes variações de prompts subjacentes, seleciona os melhores exemplos para *few-shot learning* e ajusta as instruções até maximizar a métrica de sucesso definida pelo usuário. Isso elimina a fragilidade dos prompts manuais, que quebram quando o modelo subjacente muda. No DSPy, mudar de GPT-4 para Llama-3 pode exigir apenas uma recompilação automática, sem reescrita manual de prompts.26

## ---

**Capítulo 5: Interface com o Mundo Real e Dados Estruturados**

A utilidade máxima de um agente reside na sua capacidade de interagir com sistemas externos e processar dados estruturados. A evolução do *Function Calling* e *Structured Outputs* transformou LLMs em interfaces de API universais.

### **5.1 Function Calling e o Modo Estrito da OpenAI**

A OpenAI introduziu o *Structured Outputs* com suporte a **Strict Mode** ("strict": true). Isso resolve um problema persistente de alucinação de esquemas. Quando ativado, o modelo é forçado, em nível de decodificação de tokens, a aderir exatamente ao esquema JSON fornecido.

Um exemplo prático é a extração de dados de artigos científicos.29 O esquema JSON define campos obrigatórios como title, authors (array de strings) e abstract. Ao marcar additionalProperties: false, garante-se que o modelo não invente campos não existentes. Isso é crucial para pipelines de dados automatizados onde a integridade do tipo é inegociável. Além disso, o suporte a estruturas recursivas permite modelar dados complexos, como elementos de UI aninhados (uma div contendo outras divs e buttons), permitindo que o modelo gere código de interface ou árvores de dados completas diretamente em JSON.29

### **5.2 Validação de Esquemas no Gemini**

O Google Gemini adota uma abordagem similarmente rigorosa. O modelo suporta definições de função via especificações OpenAPI. A documentação destaca a importância de descrições semânticas ricas dentro do esquema. Por exemplo, ao definir um parâmetro de data, descrevê-lo como "Data da reunião (ex: '2024-07-29')" ajuda o modelo a entender o formato esperado muito melhor do que apenas o tipo string. O Gemini demonstra alta fidelidade na execução de chamadas paralelas e composicionais, onde o resultado de uma função é usado como argumento para outra em um único turno de execução, permitindo fluxos de trabalho complexos de agendamento ou consulta de dados sem múltiplos *round-trips* com o usuário.16

## ---

**Capítulo 6: Estudo de Caso de Agentes de Codificação (Coding Agents)**

A aplicação mais madura dessas tecnologias ocorre no desenvolvimento de software. Ferramentas como Cursor, Windsurf e Cline exemplificam como diferentes estratégias de prompt e arquitetura convergem para criar "programadores pares" artificiais.

### **6.1 Cursor e a Integração Nativa**

O Cursor distingue-se por indexar o código local e usar RAG (Retrieval-Augmented Generation) para fornecer contexto relevante. Suas regras (.cursorrules) atuam como um sistema de alinhamento contínuo. A capacidade do Cursor de prever a próxima edição ("Tab" completion) baseia-se em modelos rápidos e locais, enquanto o chat ("Cmd+K") utiliza modelos maiores (Claude 3.5 Sonnet, GPT-4o) para raciocínio complexo. A orquestração aqui envolve decidir *quando* usar cada modelo para otimizar latência e custo.

### **6.2 Cline e a Autonomia de Código Aberto**

O Cline (anteriormente um projeto autônomo, agora integrado em várias ferramentas) foca em tarefas complexas em grandes bases de código, oferecendo "runtime awareness" (consciência de tempo de execução). Isso significa que o agente não apenas lê o código, mas pode executar terminais, rodar testes e ler os outputs para corrigir seus próprios erros. Essa arquitetura implementa o padrão *ReAct* (Reason \+ Act) de forma agressiva, permitindo loops de iteração autônomos que ferramentas puramente baseadas em autocompletar não conseguem realizar.31

### **6.3 Comparação de Estratégias de Agentes**

A análise comparativa 31 mostra que enquanto o **GitHub Copilot** foca na velocidade e integração fluida no fluxo de digitação (pair programmer), agentes como **Windsurf** e **Trae** (da ByteDance) introduzem modos de "agente completo" que assumem o controle do IDE para refatorações profundas. O **Trae**, por exemplo, utiliza input multimodal, permitindo que o desenvolvedor envie screenshots de uma UI para que o agente gere o código correspondente, unindo visão computacional com geração de código. Ferramentas como **v0** (Vercel) especializam-se na geração de componentes UI a partir de prompts, usando bibliotecas específicas (shadcn/ui) e frameworks (React) definidos implicitamente em seus system prompts, demonstrando o poder da especialização de domínio.

## ---

**Conclusão**

A engenharia de prompt amadureceu. Deixou de ser uma coleção de truques linguísticos para se tornar uma disciplina técnica que exige compreensão profunda da arquitetura de modelos (R1 vs V3), gestão rigorosa de contexto (System Instructions, Skills) e orquestração programática (DSPy, LCEL).

Para o profissional da área, a mensagem é clara: não basta saber "pedir". É necessário saber "configurar". A criação de um agente eficaz hoje envolve:

1. **Seleção do Modelo:** Escolher entre raciocínio profundo (R1/Qwen-Thinking) ou velocidade/criatividade (V3/GPT-4o) baseada na natureza da tarefa.  
2. **Arquitetura de Contexto:** Definir arquivos de regras (.cursorrules, SKILL.md) que atuem como a constituição do projeto.  
3. **Definição de Interface:** Criar esquemas de dados estritos (Strict Mode) para garantir a integridade da comunicação entre o modelo e os sistemas externos.  
4. **Orquestração:** Utilizar frameworks declarativos para construir fluxos de trabalho resilientes e auto-otimizáveis.

O futuro pertence aos sistemas que conseguem combinar a fluidez da linguagem natural com a rigidez e previsibilidade da engenharia de software tradicional.

---

**Nota sobre Fontes:** As informações técnicas e exemplos citados neste relatório baseiam-se na análise detalhada dos snippets de pesquisa fornecidos, incluindo documentações oficiais do GitHub, OpenAI, Google, Anthropic, DeepSeek e repositórios comunitários. Identificadores de fonte (ex: 4) rastreiam dados específicos apresentados.

#### **Trabalhos citados**

1. \[2402.07927\] A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications \- arXiv, acesso a janeiro 25, 2026, [https://arxiv.org/abs/2402.07927](https://arxiv.org/abs/2402.07927)  
2. The Prompt Report: A Systematic Survey of Prompt Engineering Techniques \- arXiv, acesso a janeiro 25, 2026, [https://arxiv.org/html/2406.06608v6](https://arxiv.org/html/2406.06608v6)  
3. The Prompt Report: A Systematic Survey of Prompting Techniques \- arXiv, acesso a janeiro 25, 2026, [https://arxiv.org/html/2406.06608v1](https://arxiv.org/html/2406.06608v1)  
4. Prompting DeepSeek R1 \- Together.ai Docs, acesso a janeiro 25, 2026, [https://docs.together.ai/docs/prompting-deepseek-r1](https://docs.together.ai/docs/prompting-deepseek-r1)  
5. Demystifying Chains, Trees, and Graphs of Thoughts \- arXiv, acesso a janeiro 25, 2026, [https://arxiv.org/html/2401.14295v3](https://arxiv.org/html/2401.14295v3)  
6. Tree of Thoughts: Deliberate Problem Solving with Large Language Models \- arXiv, acesso a janeiro 25, 2026, [https://arxiv.org/pdf/2305.10601](https://arxiv.org/pdf/2305.10601)  
7. Tree-of-Thought Approach \- Emergent Mind, acesso a janeiro 25, 2026, [https://www.emergentmind.com/topics/tree-of-thought-approach](https://www.emergentmind.com/topics/tree-of-thought-approach)  
8. Prompt Chaining \- Prompt Engineering Guide, acesso a janeiro 25, 2026, [https://www.promptingguide.ai/techniques/prompt\_chaining](https://www.promptingguide.ai/techniques/prompt_chaining)  
9. \[2210.03629\] ReAct: Synergizing Reasoning and Acting in Language Models \- arXiv, acesso a janeiro 25, 2026, [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)  
10. deepseek-ai/DeepSeek-V3-0324 \- Hugging Face, acesso a janeiro 25, 2026, [https://huggingface.co/deepseek-ai/DeepSeek-V3-0324](https://huggingface.co/deepseek-ai/DeepSeek-V3-0324)  
11. Qwen/Qwen3-8B \- Hugging Face, acesso a janeiro 25, 2026, [https://huggingface.co/Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B)  
12. Quickstart \- Qwen, acesso a janeiro 25, 2026, [https://qwen.readthedocs.io/en/latest/getting\_started/quickstart.html](https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html)  
13. Best practices with Gemini Live API | Generative AI on Vertex AI | Google Cloud Documentation, acesso a janeiro 25, 2026, [https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api/best-practices](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api/best-practices)  
14. Use system instructions | Generative AI on Vertex AI | Google Cloud Documentation, acesso a janeiro 25, 2026, [https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/system-instructions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/system-instructions)  
15. Prompt design strategies | Gemini API | Google AI for Developers, acesso a janeiro 25, 2026, [https://ai.google.dev/gemini-api/docs/prompting-strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)  
16. Function calling using the Gemini API | Firebase AI Logic \- Google, acesso a janeiro 25, 2026, [https://firebase.google.com/docs/ai-logic/function-calling](https://firebase.google.com/docs/ai-logic/function-calling)  
17. Function calling with the Gemini API | Google AI for Developers, acesso a janeiro 25, 2026, [https://ai.google.dev/gemini-api/docs/function-calling](https://ai.google.dev/gemini-api/docs/function-calling)  
18. Use Agent Skills in VS Code \- Visual Studio Code, acesso a janeiro 25, 2026, [https://code.visualstudio.com/docs/copilot/customization/agent-skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)  
19. awesome-cursorrules/rules/python-312-fastapi-best-practices ..., acesso a janeiro 25, 2026, [https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/python-312-fastapi-best-practices-cursorrules-prom/.cursorrules](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/python-312-fastapi-best-practices-cursorrules-prom/.cursorrules)  
20. PatrickJS/awesome-cursorrules: Configuration files that ... \- GitHub, acesso a janeiro 25, 2026, [https://github.com/PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)  
21. Introducing Agent Skills | Claude, acesso a janeiro 25, 2026, [https://claude.com/blog/skills](https://claude.com/blog/skills)  
22. anthropics/skills: Public repository for Agent Skills \- GitHub, acesso a janeiro 25, 2026, [https://github.com/anthropics/skills](https://github.com/anthropics/skills)  
23. Better Prompt Chaining Using LangChain Expression Language (LCEL) | by Glen Patzlaff, acesso a janeiro 25, 2026, [https://medium.com/@glenpatzlaff/better-prompt-chaining-using-langchain-expression-language-lcel-d51474b18d73](https://medium.com/@glenpatzlaff/better-prompt-chaining-using-langchain-expression-language-lcel-d51474b18d73)  
24. LangChain Expression Language, acesso a janeiro 25, 2026, [https://blog.langchain.com/langchain-expression-language/](https://blog.langchain.com/langchain-expression-language/)  
25. LangChain Expression Language Explained \- Pinecone, acesso a janeiro 25, 2026, [https://www.pinecone.io/learn/series/langchain/langchain-expression-language/](https://www.pinecone.io/learn/series/langchain/langchain-expression-language/)  
26. Programmatic Prompting: The Next Level of AI Engineering | by Sanjay Negi | Medium, acesso a janeiro 25, 2026, [https://medium.com/@sanjaynegi309/%EF%B8%8F-programmatic-prompting-the-next-level-of-ai-engineering-5a73d2ddc7f1](https://medium.com/@sanjaynegi309/%EF%B8%8F-programmatic-prompting-the-next-level-of-ai-engineering-5a73d2ddc7f1)  
27. Using DSPy to Enhance Prompt Engineering with OpenAI APIs \- DEV Community, acesso a janeiro 25, 2026, [https://dev.to/ashokan/a-beginner-friendly-tutorial-using-dspy-to-enhance-prompt-engineering-with-openai-apis-1nbn](https://dev.to/ashokan/a-beginner-friendly-tutorial-using-dspy-to-enhance-prompt-engineering-with-openai-apis-1nbn)  
28. Complete DSPy Course | Automatic and Programmatic Prompt Optimization \- YouTube, acesso a janeiro 25, 2026, [https://www.youtube.com/watch?v=fNRLeu-dd9M](https://www.youtube.com/watch?v=fNRLeu-dd9M)  
29. Structured model outputs | OpenAI API, acesso a janeiro 25, 2026, [https://platform.openai.com/docs/guides/structured-outputs](https://platform.openai.com/docs/guides/structured-outputs)  
30. Revisiting OpenAI Function Calling with Strict JSON Output | by Enrique Cano \- Medium, acesso a janeiro 25, 2026, [https://medium.com/@enriquecano12/revisiting-openai-function-calling-with-strict-json-output-c8311e3ed88e](https://medium.com/@enriquecano12/revisiting-openai-function-calling-with-strict-json-output-c8311e3ed88e)  
31. 20 Melhores Agentes de IA para Programação Que Você Precisa ..., acesso a janeiro 25, 2026, [https://apidog.com/pt/blog/ai-coding-agents-pt/](https://apidog.com/pt/blog/ai-coding-agents-pt/)