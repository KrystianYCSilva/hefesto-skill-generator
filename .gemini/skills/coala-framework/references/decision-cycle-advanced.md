# Decision Cycle Advanced

Implementações avançadas do ciclo de decisão CoALA.

## Ciclo com Metacognição

```python
class MetacognitiveDecisionCycle:
    """Ciclo de decisão com monitoramento próprio."""
    
    def __init__(self, agent):
        self.agent = agent
        self.iteration_count = 0
        self.max_iterations = 10
        self.stuck_threshold = 3
        self.stuck_counter = 0
        self.previous_state = None
    
    def run(self, goal: str) -> dict:
        """Executa ciclo com metacognição."""
        while not self._is_complete() and self.iteration_count < self.max_iterations:
            # Metacognição: verificar se está preso
            if self._is_stuck():
                self._handle_stuck_state()
            
            # Fase 1: PLAN
            plan = self._plan(goal)
            
            # Metacognição: avaliar plano
            if not self._is_plan_valid(plan):
                plan = self._revise_plan(plan)
            
            # Fase 2: EXECUTE
            action = self._select_action(plan)
            result = self._execute(action)
            
            # Fase 3: OBSERVE
            observation = self._observe(result)
            
            # Metacognição: verificar resultado
            if self._is_result_anomalous(observation):
                self._handle_anomaly(observation)
            
            # Fase 4: LEARN
            self._learn(action, result, observation)
            
            # Atualizar estado
            self._update_state()
            self.iteration_count += 1
        
        return self._generate_result()
    
    def _is_stuck(self) -> bool:
        """Detecta se agente está preso em loop."""
        current_state = self._get_state_hash()
        if current_state == self.previous_state:
            self.stuck_counter += 1
            return self.stuck_counter >= self.stuck_threshold
        else:
            self.stuck_counter = 0
            self.previous_state = current_state
            return False
    
    def _handle_stuck_state(self):
        """Estratégias para sair de estado preso."""
        strategies = [
            self._try_different_action,
            self._seek_external_help,
            self._reformulate_goal,
            self._reset_working_memory
        ]
        
        for strategy in strategies:
            try:
                strategy()
                break
            except:
                continue
    
    def _is_plan_valid(self, plan: list) -> bool:
        """Valida se plano é viável."""
        return len(plan) > 0 and all(
            self._can_execute_action(action) for action in plan[:3]
        )
    
    def _is_result_anomalous(self, observation: dict) -> bool:
        """Detecta resultados anômalos."""
        return (
            observation.get("success") is False and
            observation.get("unexpected", False)
        )
```

## Ciclo Hierárquico

```python
class HierarchicalDecisionCycle:
    """Ciclo com planejamento em múltiplos níveis."""
    
    LEVEL_STRATEGIC = 0
    LEVEL_TACTICAL = 1
    LEVEL_OPERATIONAL = 2
    
    def __init__(self):
        self.levels = {
            self.LEVEL_STRATEGIC: StrategicPlanner(),
            self.LEVEL_TACTICAL: TacticalPlanner(),
            self.LEVEL_OPERATIONAL: OperationalPlanner()
        }
        self.current_level = self.LEVEL_OPERATIONAL
    
    def run(self, goal: str) -> dict:
        """Executa ciclo hierárquico."""
        # Nível estratégico: definir plano macro
        strategic_plan = self.levels[self.LEVEL_STRATEGIC].plan(goal)
        
        for objective in strategic_plan:
            # Nível tático: definir abordagem
            tactical_plan = self.levels[self.LEVEL_TACTICAL].plan(objective)
            
            for subtask in tactical_plan:
                # Nível operacional: executar ações concretas
                self._execute_operational(subtask)
        
        return self._compile_results()
    
    def _execute_operational(self, subtask: str):
        """Executa ciclo operacional completo."""
        cycle = OperationalDecisionCycle()
        return cycle.run(subtask)


class StrategicPlanner:
    """Planejador de alto nível."""
    
    def plan(self, goal: str) -> list:
        """Decompõe objetivo em objetivos estratégicos."""
        # Usar LLM para decomposição estratégica
        prompt = f"""
        Objetivo: {goal}
        
        Decomponha em 3-5 objetivos estratégicos de alto nível.
        Cada objetivo deve ser alcançável em 5-10 passos.
        """
        
        response = llm.generate(prompt)
        return self._parse_objectives(response)


class TacticalPlanner:
    """Planejador de médio nível."""
    
    def plan(self, objective: str) -> list:
        """Define abordagem tática para objetivo."""
        prompt = f"""
        Objetivo estratégico: {objective}
        
        Defina 3-7 subtarefas táticas para alcançar este objetivo.
        Ordene por dependências e prioridade.
        """
        
        response = llm.generate(prompt)
        return self._parse_subtasks(response)


class OperationalPlanner:
    """Planejador de execução."""
    
    def plan(self, subtask: str) -> list:
        """Define ações operacionais concretas."""
        prompt = f"""
        Subtarefa: {subtask}
        
        Liste ações específicas e executáveis (API calls, queries, etc).
        Cada ação deve ser atômica e mensurável.
        """
        
        response = llm.generate(prompt)
        return self._parse_actions(response)
```

## Ciclo com Backtracking

```python
class BacktrackingDecisionCycle:
    """Ciclo com capacidade de retroceder."""
    
    def __init__(self):
        self.state_stack = []
        self.max_backtracks = 5
        self.backtrack_count = 0
    
    def run(self, goal: str) -> dict:
        """Executa ciclo com backtracking."""
        while not self._is_complete():
            # Salvar estado atual
            self._push_state()
            
            # Tentar executar
            try:
                result = self._execute_step()
                
                if self._is_success(result):
                    self._commit_step()
                else:
                    self._handle_failure(result)
            
            except Exception as e:
                self._handle_error(e)
        
        return self._get_final_result()
    
    def _push_state(self):
        """Salva estado atual na pilha."""
        state = {
            "working_memory": copy.deepcopy(self.working_memory),
            "action_history": self.action_history.copy(),
            "iteration": self.iteration_count
        }
        self.state_stack.append(state)
    
    def _backtrack(self, steps: int = 1) -> bool:
        """Retrocede n passos."""
        if len(self.state_stack) < steps or self.backtrack_count >= self.max_backtracks:
            return False
        
        # Descartar estados intermediários
        for _ in range(steps):
            self.state_stack.pop()
        
        # Restaurar estado
        previous_state = self.state_stack[-1]
        self.working_memory = previous_state["working_memory"]
        self.action_history = previous_state["action_history"]
        self.iteration_count = previous_state["iteration"]
        
        self.backtrack_count += 1
        return True
    
    def _handle_failure(self, result):
        """Processa falha e decide se faz backtracking."""
        # Analisar falha
        failure_analysis = self._analyze_failure(result)
        
        if failure_analysis["recoverable"]:
            if self._backtrack(failure_analysis["steps_back"]):
                # Tentar abordagem alternativa
                self._try_alternative(failure_analysis)
            else:
                # Não pode retroceder mais
                raise UnrecoverableError(failure_analysis)
        else:
            raise UnrecoverableError(failure_analysis)
    
    def _analyze_failure(self, result) -> dict:
        """Analisa falha e determina estratégia."""
        return {
            "recoverable": True,
            "steps_back": 1,
            "alternative_actions": []
        }
```

## Ciclo Multi-Agente

```python
class MultiAgentDecisionCycle:
    """Ciclo coordenando múltiplos agentes."""
    
    def __init__(self):
        self.agents = {}
        self.coordinator = Coordinator()
        self.shared_memory = SharedMemory()
    
    def register_agent(self, agent_id: str, agent):
        """Registra agente no sistema."""
        self.agents[agent_id] = agent
        agent.shared_memory = self.shared_memory
    
    def run(self, goal: str) -> dict:
        """Executa ciclo multi-agente."""
        # Decompor tarefa
        subtasks = self.coordinator.decompose(goal)
        
        # Distribuir para agentes
        assignments = self.coordinator.assign(subtasks, self.agents)
        
        # Executar em paralelo
        results = self._execute_parallel(assignments)
        
        # Integrar resultados
        return self.coordinator.integrate(results)
    
    def _execute_parallel(self, assignments: dict) -> dict:
        """Executa tarefas em paralelo."""
        import concurrent.futures
        
        results = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                agent_id: executor.submit(
                    self.agents[agent_id].run, 
                    subtask
                )
                for agent_id, subtask in assignments.items()
            }
            
            for agent_id, future in futures.items():
                results[agent_id] = future.result()
        
        return results


class Coordinator:
    """Coordenador de multi-agentes."""
    
    def decompose(self, goal: str) -> list:
        """Decompõe objetivo em sub-tarefas independentes."""
        prompt = f"""
        Objetivo: {goal}
        
        Decomponha em sub-tarefas que podem ser executadas em paralelo.
        Cada sub-tarefa deve ser independente e ter entregável claro.
        """
        
        response = llm.generate(prompt)
        return self._parse_subtasks(response)
    
    def assign(self, subtasks: list, agents: dict) -> dict:
        """Atribui sub-tarefas aos agentes mais adequados."""
        assignments = {}
        
        for subtask in subtasks:
            best_agent = self._select_best_agent(subtask, agents)
            assignments[best_agent] = subtask
        
        return assignments
    
    def integrate(self, results: dict) -> dict:
        """Integra resultados de múltiplos agentes."""
        prompt = f"""
        Resultados parciais: {results}
        
        Integre em um resultado coerente e completo.
        Resolva conflitos e preencha lacunas.
        """
        
        response = llm.generate(prompt)
        return {
            "integrated_result": response,
            "partial_results": results
        }
```

## Ciclo com Aprendizado por Reforço

```python
class RLDecisionCycle:
    """Ciclo com aprendizado por reforço."""
    
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.action_history = []
    
    def run(self, goal: str) -> dict:
        """Executa ciclo com RL."""
        state = self._get_state()
        total_reward = 0
        
        while not self._is_complete():
            # Selecionar ação (epsilon-greedy)
            action = self._select_action(state)
            
            # Executar
            result = self._execute(action)
            
            # Observar novo estado e recompensa
            new_state = self._get_state()
            reward = self._calculate_reward(result)
            total_reward += reward
            
            # Atualizar Q-table
            self._update_q_value(state, action, reward, new_state)
            
            state = new_state
            self.action_history.append((state, action, reward))
        
        return {
            "result": self._get_final_result(),
            "total_reward": total_reward,
            "iterations": len(self.action_history)
        }
    
    def _select_action(self, state: tuple) -> str:
        """Seleciona ação usando epsilon-greedy."""
        import random
        
        if random.random() < self.epsilon:
            # Exploração
            return random.choice(self._get_available_actions())
        else:
            # Exploração
            return self._get_best_action(state)
    
    def _get_best_action(self, state: tuple) -> str:
        """Retorna melhor ação para estado."""
        state_actions = self.q_table.get(state, {})
        
        if not state_actions:
            return random.choice(self._get_available_actions())
        
        return max(state_actions, key=state_actions.get)
    
    def _update_q_value(self, state: tuple, action: str, 
                        reward: float, new_state: tuple):
        """Atualiza valor Q usando equação de Bellman."""
        if state not in self.q_table:
            self.q_table[state] = {}
        
        old_value = self.q_table[state].get(action, 0)
        
        # Valor máximo do novo estado
        next_max = max(
            self.q_table.get(new_state, {}).values() or [0]
        )
        
        # Atualização Q-learning
        new_value = old_value + self.learning_rate * (
            reward + self.discount_factor * next_max - old_value
        )
        
        self.q_table[state][action] = new_value
    
    def _calculate_reward(self, result) -> float:
        """Calcula recompensa do resultado."""
        if result.get("success"):
            return 1.0
        elif result.get("partial_success"):
            return 0.5
        else:
            return -1.0
```

## Ciclo com Verificação de Segurança

```python
class SafeDecisionCycle:
    """Ciclo com verificações de segurança."""
    
    def __init__(self):
        self.safety_constraints = []
        self.risk_threshold = 0.3
    
    def add_constraint(self, constraint):
        """Adiciona restrição de segurança."""
        self.safety_constraints.append(constraint)
    
    def run(self, goal: str) -> dict:
        """Executa ciclo com verificações de segurança."""
        while not self._is_complete():
            # PLAN com verificação
            plan = self._plan(goal)
            
            if not self._verify_plan_safety(plan):
                plan = self._make_safe_plan(plan)
            
            # EXECUTE com monitoramento
            for action in plan:
                if not self._is_action_safe(action):
                    self._handle_unsafe_action(action)
                    continue
                
                result = self._execute_with_monitoring(action)
                
                # OBSERVE e verificar
                observation = self._observe(result)
                
                if self._detect_danger(observation):
                    self._emergency_stop()
                    return {"error": "Safety violation detected"}
                
                # LEARN
                self._learn(action, result, observation)
        
        return self._generate_result()
    
    def _verify_plan_safety(self, plan: list) -> bool:
        """Verifica se plano viola restrições."""
        for constraint in self.safety_constraints:
            if not constraint.check(plan):
                return False
        return True
    
    def _is_action_safe(self, action) -> bool:
        """Avalia risco de ação específica."""
        risk = self._calculate_risk(action)
        return risk < self.risk_threshold
    
    def _calculate_risk(self, action) -> float:
        """Calcula nível de risco da ação."""
        # Implementação específica por tipo de ação
        if action.type == "external":
            return 0.5  # Maior risco
        return 0.1  # Menor risco
    
    def _emergency_stop(self):
        """Para execução de emergência."""
        self._rollback_all()
        self._notify_operators()
```
