# Action Space Patterns

Padrões e exemplos para implementação do espaço de ações em CoALA.

## Ações Internas

### Reasoning (Raciocínio)

```python
class ReasoningAction:
    """Ação interna de raciocínio deliberativo."""
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def analyze(self, context: dict, question: str) -> dict:
        """Análise profunda de uma situação."""
        prompt = f"""
        Contexto: {context}
        Questão: {question}
        
        Analise profundamente e retorne:
        1. Pontos principais
        2. Suposições
        3. Possíveis abordagens
        4. Recomendação
        """
        
        response = self.llm.generate(prompt)
        return self._parse_analysis(response)
    
    def plan(self, goal: str, available_actions: list) -> list:
        """Planejamento de sequência de ações."""
        prompt = f"""
        Objetivo: {goal}
        Ações disponíveis: {available_actions}
        
        Crie um plano passo a passo para atingir o objetivo.
        Retorne como lista ordenada de ações.
        """
        
        response = self.llm.generate(prompt)
        return self._parse_plan(response)
    
    def decide(self, options: list, criteria: dict) -> dict:
        """Tomada de decisão entre opções."""
        prompt = f"""
        Opções: {options}
        Critérios: {criteria}
        
        Avalie cada opção segundo os critérios e escolha a melhor.
        Retorne: escolha e justificativa.
        """
        
        response = self.llm.generate(prompt)
        return self._parse_decision(response)
    
    def _parse_analysis(self, response):
        # Parser de resposta
        return {"analysis": response}
    
    def _parse_plan(self, response):
        # Extrair lista de ações
        return [line.strip() for line in response.split('\n') if line.strip()]
    
    def _parse_decision(self, response):
        # Extrair decisão
        return {"decision": response, "confidence": 0.8}
```

### Retrieval (Recuperação)

```python
class RetrievalAction:
    """Ação interna de recuperação de memória."""
    
    def __init__(self, memory_system):
        self.memory = memory_system
    
    def retrieve_context(self, query: str, memory_types: list = None) -> dict:
        """Recupera contexto relevante de múltiplas memórias."""
        context = {}
        
        if "episodic" in memory_types:
            context["experiences"] = self.memory.episodic.retrieve_similar(
                query, k=3
            )
        
        if "semantic" in memory_types:
            context["facts"] = self.memory.semantic.query_knowledge(
                query, k=5
            )
        
        if "procedural" in memory_types:
            context["procedures"] = self.memory.procedural.retrieve(
                query, k=2
            )
        
        return context
    
    def retrieve_similar_experiences(self, situation: str) -> list:
        """Busca experiências passadas similares."""
        return self.memory.episodic.retrieve_similar_experiences(
            situation, k=3, outcome_filter="success"
        )
    
    def query_facts(self, topic: str, category: str = None) -> list:
        """Consulta fatos sobre um tópico."""
        return self.memory.semantic.query_knowledge(
            topic, k=5, category_filter=category
        )
    
    def get_procedure(self, task: str) -> dict:
        """Recupera procedimento para tarefa."""
        procedures = self.memory.procedural.retrieve_procedure(task, k=1)
        return procedures[0] if procedures else None
```

### Learning (Aprendizado)

```python
class LearningAction:
    """Ação interna de atualização de memórias."""
    
    def __init__(self, memory_system):
        self.memory = memory_system
    
    def learn_from_experience(self, action, result, outcome: str):
        """Armazena nova experiência."""
        lesson = self._extract_lesson(action, result, outcome)
        
        self.memory.episodic.store_experience(
            action=str(action),
            result=str(result),
            outcome=outcome,
            lesson=lesson
        )
    
    def extract_facts(self, content: str, confidence: float = 0.8) -> list:
        """Extrai fatos de conteúdo."""
        # Usar LLM para extrair fatos estruturados
        facts = self._parse_facts(content)
        
        for fact in facts:
            self.memory.semantic.store_fact(
                fact=fact["statement"],
                category=fact["category"],
                confidence=confidence
            )
        
        return facts
    
    def update_procedure_success(self, procedure_id: str, success: bool):
        """Atualiza taxa de sucesso de procedimento."""
        self.memory.procedural.update_success_rate(
            procedure_id, success
        )
    
    def _extract_lesson(self, action, result, outcome):
        """Extrai lição aprendida da experiência."""
        return f"Action {action} resulted in {outcome}"
    
    def _parse_facts(self, content):
        """Parser de fatos."""
        return [{"statement": content, "category": "general"}]
```

## Ações Externas

### Tool Use

```python
class ToolUseAction:
    """Ação externa de uso de ferramentas."""
    
    def __init__(self, tool_registry):
        self.tools = tool_registry
        self.execution_history = []
    
    def execute_tool(self, tool_name: str, parameters: dict) -> dict:
        """Executa uma ferramenta disponível."""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
        
        tool = self.tools[tool_name]
        
        try:
            result = tool.execute(**parameters)
            
            self.execution_history.append({
                "tool": tool_name,
                "params": parameters,
                "result": result,
                "timestamp": datetime.now()
            })
            
            return {
                "success": True,
                "result": result
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_available_tools(self) -> list:
        """Lista ferramentas disponíveis."""
        return [
            {"name": name, "description": tool.description}
            for name, tool in self.tools.items()
        ]
    
    def validate_parameters(self, tool_name: str, parameters: dict) -> bool:
        """Valida parâmetros para ferramenta."""
        tool = self.tools.get(tool_name)
        if not tool:
            return False
        
        return tool.validate_params(parameters)


# Exemplo de registro de ferramentas
tool_registry = {
    "web_search": WebSearchTool(),
    "calculator": CalculatorTool(),
    "file_reader": FileReaderTool(),
    "api_caller": APICallerTool()
}
```

### Communication

```python
class CommunicationAction:
    """Ação externa de comunicação."""
    
    def __init__(self):
        self.message_history = []
    
    def send_message(self, recipient: str, content: str, 
                     channel: str = "default") -> dict:
        """Envia mensagem para destinatário."""
        message = {
            "id": f"msg_{datetime.now().timestamp()}",
            "recipient": recipient,
            "content": content,
            "channel": channel,
            "timestamp": datetime.now(),
            "status": "sent"
        }
        
        self.message_history.append(message)
        
        return {
            "success": True,
            "message_id": message["id"]
        }
    
    def respond_to_user(self, response: str, format: str = "text") -> dict:
        """Responde ao usuário final."""
        formatted_response = self._format_response(response, format)
        
        return {
            "type": "user_response",
            "content": formatted_response,
            "format": format,
            "timestamp": datetime.now()
        }
    
    def request_clarification(self, question: str) -> dict:
        """Solicita esclarecimento ao usuário."""
        return {
            "type": "clarification_request",
            "question": question,
            "timestamp": datetime.now()
        }
    
    def notify(self, event: str, severity: str = "info") -> dict:
        """Envia notificação."""
        return {
            "type": "notification",
            "event": event,
            "severity": severity,
            "timestamp": datetime.now()
        }
    
    def _format_response(self, content, format):
        if format == "json":
            return json.dumps(content)
        elif format == "markdown":
            return f"```\n{content}\n```"
        return str(content)
```

## Padrões de Design

### Action Factory

```python
class ActionFactory:
    """Factory para criação de ações."""
    
    _actions = {
        "reasoning": ReasoningAction,
        "retrieval": RetrievalAction,
        "learning": LearningAction,
        "tool_use": ToolUseAction,
        "communication": CommunicationAction
    }
    
    @classmethod
    def create_action(cls, action_type: str, **dependencies):
        """Cria instância de ação."""
        action_class = cls._actions.get(action_type)
        if not action_class:
            raise ValueError(f"Unknown action type: {action_type}")
        
        return action_class(**dependencies)
    
    @classmethod
    def register_action(cls, action_type: str, action_class):
        """Registra novo tipo de ação."""
        cls._actions[action_type] = action_class
```

### Action Queue

```python
from collections import deque

class ActionQueue:
    """Fila de ações priorizada."""
    
    def __init__(self):
        self.queue = deque()
        self.priorities = {
            "critical": 0,
            "high": 1,
            "normal": 2,
            "low": 3
        }
    
    def enqueue(self, action, priority: str = "normal"):
        """Adiciona ação à fila."""
        item = {
            "action": action,
            "priority": self.priorities.get(priority, 2),
            "timestamp": datetime.now()
        }
        
        # Inserir na posição correta baseada em prioridade
        inserted = False
        for i, existing in enumerate(self.queue):
            if existing["priority"] > item["priority"]:
                self.queue.insert(i, item)
                inserted = True
                break
        
        if not inserted:
            self.queue.append(item)
    
    def dequeue(self):
        """Remove e retorna próxima ação."""
        if self.queue:
            return self.queue.popleft()["action"]
        return None
    
    def peek(self):
        """Visualiza próxima ação sem remover."""
        if self.queue:
            return self.queue[0]["action"]
        return None
    
    def is_empty(self) -> bool:
        """Verifica se fila está vazia."""
        return len(self.queue) == 0
```

## Melhores Práticas

1. **Sempre valide ações antes de executar**
2. **Prefira ações internas sobre externas**
3. **Registre todas as execuções para aprendizado**
4. **Implemente timeout para ações externas**
5. **Use retry com backoff para falhas transientes**

```python
# Exemplo: Action com timeout e retry
class ResilientAction:
    def execute_with_retry(self, action, max_retries=3, timeout=30):
        for attempt in range(max_retries):
            try:
                return self._execute_with_timeout(action, timeout)
            except TimeoutError:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
```
