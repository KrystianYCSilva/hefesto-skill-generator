# Integration Examples

Exemplos práticos de integração CoALA com diferentes contextos.

## Exemplo 1: Agente de Debugging

```python
class DebuggingAgent(CoALAAgent):
    """Agente especializado em debugging usando CoALA."""
    
    def __init__(self):
        super().__init__(llm_client=openai_client)
        self._setup_procedures()
    
    def _setup_procedures(self):
        """Configura procedimentos de debugging."""
        procedures = [
            {
                "name": "debug_null_pointer",
                "steps": [
                    "Identificar linha no stack trace",
                    "Verificar inicialização de variáveis",
                    "Adicionar null checks",
                    "Testar correção"
                ],
                "preconditions": ["NullPointerException"],
                "success_rate": 0.9
            },
            {
                "name": "debug_type_error",
                "steps": [
                    "Verificar tipos esperados vs recebidos",
                    "Checar conversões de tipo",
                    "Validar input data"
                ],
                "preconditions": ["TypeError", "ClassCastException"],
                "success_rate": 0.85
            },
            {
                "name": "debug_performance",
                "steps": [
                    "Identificar hotspots com profiler",
                    "Analisar complexidade algorítmica",
                    "Considerar caching",
                    "Avaliar lazy loading"
                ],
                "preconditions": ["slow_execution", "timeout"],
                "success_rate": 0.8
            }
        ]
        
        for proc in procedures:
            self.procedural.store_procedure(**proc)
    
    def debug(self, error_log: str, code_context: str = None) -> dict:
        """Processo completo de debugging."""
        # Setup
        self.working_memory.current_input = error_log
        self.working_memory.active_goals.append("Resolver erro")
        
        if code_context:
            self.working_memory.add_intermediate_result(
                "code_context", code_context
            )
        
        # Recuperar experiências similares
        similar_errors = self.episodic.retrieve_similar_experiences(
            error_log, k=3
        )
        self.working_memory.cache_retrieval(
            "similar_errors", similar_errors
        )
        
        # Identificar tipo de erro
        error_type = self._classify_error(error_log)
        
        # Recuperar procedimento adequado
        procedure = self.procedural.retrieve_procedure(
            f"debug {error_type}",
            context={"error_type": error_type},
            k=1
        )
        
        if procedure:
            return self._follow_procedure(procedure[0], error_log)
        else:
            return self._explore_solution(error_log)
    
    def _classify_error(self, error_log: str) -> str:
        """Classifica tipo de erro."""
        if "NullPointer" in error_log or "NoneType" in error_log:
            return "null_pointer"
        elif "TypeError" in error_log or "ClassCast" in error_log:
            return "type_error"
        elif "timeout" in error_log.lower() or "slow" in error_log.lower():
            return "performance"
        else:
            return "generic"
    
    def _follow_procedure(self, procedure: dict, error_log: str) -> dict:
        """Segue procedimento de debugging."""
        results = []
        
        for step in procedure["steps"]:
            # Executar passo
            step_result = self._execute_step(step, error_log)
            results.append({"step": step, "result": step_result})
            
            # Verificar sucesso
            if step_result.get("resolved"):
                break
        
        # Aprender com experiência
        success = any(r.get("resolved") for r in results)
        self._learn_debugging_experience(
            error_log, procedure["name"], success
        )
        
        return {
            "success": success,
            "procedure": procedure["name"],
            "steps_executed": results,
            "solution": results[-1] if success else None
        }
```

## Exemplo 2: Agente de Pesquisa

```python
class ResearchAgent(CoALAAgent):
    """Agente de pesquisa acadêmica com CoALA."""
    
    def __init__(self):
        super().__init__(llm_client=openai_client)
        self.register_tool("web_search", WebSearchTool())
        self.register_tool("paper_analyzer", PaperAnalyzerTool())
        self.register_tool("citation_graph", CitationGraphTool())
    
    def research(self, topic: str, depth: int = 3) -> dict:
        """Executa pesquisa completa sobre tópico."""
        self.working_memory.current_input = topic
        self.working_memory.active_goals.append(
            f"Pesquisar: {topic} (profundidade {depth})"
        )
        
        # Verificar conhecimento existente
        existing_knowledge = self.semantic.query_knowledge(topic, k=5)
        
        if existing_knowledge:
            self.working_memory.cache_retrieval(
                "existing_knowledge", existing_knowledge
            )
        
        # Buscar papers relevantes
        papers = self._search_papers(topic)
        
        # Analisar papers
        analysis_results = []
        for paper in papers[:depth]:
            analysis = self._analyze_paper(paper)
            analysis_results.append(analysis)
            
            # Extrair fatos
            self._extract_and_store_facts(analysis)
        
        # Sintetizar resultados
        synthesis = self._synthesize_findings(analysis_results)
        
        # Armazenar experiência
        self.episodic.store_experience(
            action=f"research({topic})",
            result=f"Encontrados {len(papers)} papers",
            outcome="success",
            lesson=f"Principais achados: {synthesis['key_findings']}"
        )
        
        return {
            "topic": topic,
            "papers_analyzed": len(analysis_results),
            "synthesis": synthesis,
            "facts_learned": len(analysis_results) * 3  # Estimativa
        }
    
    def _search_papers(self, query: str) -> list:
        """Busca papers relevantes."""
        result = self.execute_external_action(
            "tool_use",
            {"tool": "web_search", "query": f"{query} paper arxiv"}
        )
        return result.get("papers", [])
    
    def _analyze_paper(self, paper: dict) -> dict:
        """Analisa paper individual."""
        return self.execute_external_action(
            "tool_use",
            {"tool": "paper_analyzer", "paper": paper}
        )
    
    def _extract_and_store_facts(self, analysis: dict):
        """Extrai e armazena fatos do paper."""
        facts = analysis.get("key_contributions", [])
        
        for fact in facts:
            self.semantic.store_fact(
                fact=fact,
                category="research",
                confidence=0.8,
                source=analysis.get("paper_id")
            )
    
    def _synthesize_findings(self, analyses: list) -> dict:
        """Sintetiza achados de múltiplos papers."""
        prompt = f"""
        Análises de papers: {analyses}
        
        Sintetize em:
        1. Key findings principais
        2. Tendências identificadas
        3. Lacunas na pesquisa
        4. Direções futuras
        """
        
        response = self.llm.generate(prompt)
        return self._parse_synthesis(response)
```

## Exemplo 3: Agente de Análise de Dados

```python
class DataAnalysisAgent(CoALAAgent):
    """Agente para análise exploratória de dados."""
    
    def __init__(self):
        super().__init__(llm_client=openai_client)
        self.register_tool("pandas", PandasTool())
        self.register_tool("visualizer", VisualizationTool())
        self.register_tool("statistical", StatisticalTool())
    
    def analyze(self, dataset_path: str, objective: str) -> dict:
        """Executa análise completa de dados."""
        self.working_memory.current_input = dataset_path
        self.working_memory.active_goals.append(objective)
        
        # Carregar dados
        df = self._load_data(dataset_path)
        
        # Perfil inicial
        profile = self._profile_data(df)
        self.working_memory.add_intermediate_result("profile", profile)
        
        # Determinar análises necessárias
        analyses = self._plan_analyses(profile, objective)
        
        # Executar análises
        results = []
        for analysis in analyses:
            result = self._execute_analysis(df, analysis)
            results.append(result)
            
            # Extrair insights
            insights = self._extract_insights(result)
            for insight in insights:
                self.semantic.store_fact(
                    fact=insight,
                    category="data_insight",
                    confidence=0.9
                )
        
        # Gerar visualizações
        visualizations = self._create_visualizations(df, results)
        
        # Compilar relatório
        report = self._compile_report(results, visualizations)
        
        # Aprender
        self.episodic.store_experience(
            action=f"analyze({dataset_path})",
            result=f"Análises: {len(results)}, Insights: {len(insights)}",
            outcome="success"
        )
        
        return report
    
    def _plan_analyses(self, profile: dict, objective: str) -> list:
        """Planeja quais análises executar."""
        prompt = f"""
        Perfil dos dados: {profile}
        Objetivo: {objective}
        
        Quais análises estatísticas e exploratórias devem ser feitas?
        Considere: distribuições, correlações, outliers, tendências.
        """
        
        response = self.llm.generate(prompt)
        return self._parse_analysis_plan(response)
    
    def _execute_analysis(self, df, analysis_config: dict) -> dict:
        """Executa análise específica."""
        analysis_type = analysis_config["type"]
        
        if analysis_type == "distribution":
            return self._analyze_distribution(df, analysis_config)
        elif analysis_type == "correlation":
            return self._analyze_correlations(df, analysis_config)
        elif analysis_type == "outlier":
            return self._detect_outliers(df, analysis_config)
        # ... mais tipos
    
    def _extract_insights(self, result: dict) -> list:
        """Extrai insights dos resultados."""
        prompt = f"""
        Resultado da análise: {result}
        
        Extraia 2-3 insights acionáveis em formato conciso.
        """
        
        response = self.llm.generate(prompt)
        return response.split('\n')
```

## Exemplo 4: Agente de Atendimento ao Cliente

```python
class CustomerServiceAgent(CoALAAgent):
    """Agente de atendimento com memória de interações."""
    
    def __init__(self):
        super().__init__(llm_client=openai_client)
        self.register_tool("crm", CRMIntegration())
        self.register_tool("knowledge_base", KnowledgeBaseTool())
    
    def handle_inquiry(self, customer_id: str, inquiry: str) -> dict:
        """Processa solicitação de cliente."""
        # Carregar histórico do cliente
        customer_history = self._load_customer_history(customer_id)
        self.working_memory.cache_retrieval(
            "customer_history", customer_history
        )
        
        # Classificar intenção
        intent = self._classify_intent(inquiry)
        
        # Verificar interações similares passadas
        similar_cases = self.episodic.retrieve_similar_experiences(
            f"{intent}: {inquiry}",
            k=3,
            outcome_filter="success"
        )
        
        if similar_cases:
            # Usar solução anterior adaptada
            response = self._adapt_solution(
                similar_cases[0], inquiry
            )
        else:
            # Resolver com base em conhecimento
            kb_articles = self.semantic.query_knowledge(
                inquiry, category="support", k=3
            )
            response = self._generate_response(kb_articles, inquiry)
        
        # Registrar interação
        self.episodic.store_experience(
            action=f"handle({intent})",
            result=response,
            outcome="pending",  # Atualizado após feedback
            lesson=""
        )
        
        return {
            "response": response,
            "intent": intent,
            "similar_cases": len(similar_cases),
            "kb_references": len(kb_articles)
        }
    
    def _load_customer_history(self, customer_id: str) -> dict:
        """Carrega histórico do cliente."""
        return self.execute_external_action(
            "tool_use",
            {"tool": "crm", "action": "get_history", "id": customer_id}
        )
    
    def _classify_intent(self, inquiry: str) -> str:
        """Classifica intenção da solicitação."""
        intents = [
            "billing_question",
            "technical_support",
            "product_inquiry",
            "complaint",
            "feature_request"
        ]
        
        prompt = f"""
        Solicitação: {inquiry}
        
        Classifique em uma das intenções: {intents}
        """
        
        response = self.llm.generate(prompt)
        return response.strip().lower()
    
    def _adapt_solution(self, similar_case: dict, current_inquiry: str) -> str:
        """Adapta solução anterior para caso atual."""
        prompt = f"""
        Caso similar anterior: {similar_case}
        Nova solicitação: {current_inquiry}
        
        Adapte a solução anterior para esta nova situação.
        Personalize mantendo a eficácia.
        """
        
        return self.llm.generate(prompt)
    
    def process_feedback(self, interaction_id: str, feedback: dict):
        """Processa feedback do cliente."""
        satisfaction = feedback.get("satisfaction", 0)
        
        # Atualizar experiência
        outcome = "success" if satisfaction > 3 else "failure"
        
        # Atualizar memória
        self.episodic.update_experience_outcome(
            interaction_id, outcome
        )
        
        # Extrair lições
        if outcome == "failure":
            lesson = self._extract_lesson(feedback)
            self.episodic.update_experience_lesson(
                interaction_id, lesson
            )
```

## Exemplo 5: Integração com Sistemas Legados

```python
class LegacySystemAgent(CoALAAgent):
    """Agente para interação com sistemas legados."""
    
    def __init__(self):
        super().__init__(llm_client=openai_client)
        self.procedures = self._load_legacy_procedures()
    
    def _load_legacy_procedures(self) -> list:
        """Carrega procedimentos de sistemas legados."""
        return [
            {
                "name": "sap_user_creation",
                "steps": [
                    "Acessar transação SU01",
                    "Preencher dados básicos",
                    "Atribuir perfis",
                    "Salvar e ativar"
                ],
                "system": "SAP"
            },
            {
                "name": "mainframe_query",
                "steps": [
                    "Conectar via 3270",
                    "Navegar para CICS",
                    "Executar transação",
                    "Extrair relatório"
                ],
                "system": "Mainframe"
            }
        ]
    
    def execute_legacy_task(self, task_description: str) -> dict:
        """Executa tarefa em sistema legado."""
        # Identificar sistema e procedimento
        procedure = self._identify_procedure(task_description)
        
        if not procedure:
            return {"error": "Procedimento não encontrado"}
        
        # Recuperar detalhes do sistema
        system_info = self.semantic.query_knowledge(
            procedure["system"],
            category="legacy_systems",
            k=5
        )
        
        # Preparar execução
        self.working_memory.cache_retrieval(
            "system_info", system_info
        )
        
        # Executar passos
        results = []
        for step in procedure["steps"]:
            result = self._execute_legacy_step(
                step, procedure["system"], system_info
            )
            results.append(result)
            
            if not result.get("success"):
                # Tentar recuperação
                recovery = self._attempt_recovery(
                    step, result, procedure
                )
                if recovery:
                    results.append(recovery)
        
        # Aprender
        success = all(r.get("success") for r in results)
        self.episodic.store_experience(
            action=task_description,
            result=str(results),
            outcome="success" if success else "failure"
        )
        
        return {
            "procedure": procedure["name"],
            "system": procedure["system"],
            "success": success,
            "steps": results
        }
```
