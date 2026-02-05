# Memory Implementation - Detailed Guide

Implementações completas dos três tipos de memória de longo prazo em CoALA.

---

## Episodic Memory

Armazena experiências passadas do agente.

### Implementação com Vector DB

```python
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer

class EpisodicMemory:
    """
    Memória episódica usando embeddings para recuperação semântica.
    """
    
    def __init__(self, vector_db_client, embedding_model='all-MiniLM-L6-v2'):
        self.db = vector_db_client
        self.encoder = SentenceTransformer(embedding_model)
        self.collection_name = "episodic_memories"
        self._ensure_collection()
    
    def store_experience(self, 
                        action: str, 
                        result: Any, 
                        outcome: str,
                        lesson: Optional[str] = None,
                        metadata: Optional[Dict] = None) -> str:
        """
        Armazena uma experiência na memória episódica.
        
        Args:
            action: Descrição da ação tomada
            result: Resultado da ação
            outcome: 'success' ou 'failure'
            lesson: Lição aprendida (opcional)
            metadata: Metadados adicionais
        
        Returns:
            ID da experiência armazenada
        """
        experience = {
            "id": f"exp_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "result": str(result)[:1000],  # Limitar tamanho
            "outcome": outcome,
            "lesson": lesson or "",
            "metadata": metadata or {},
            "access_count": 0,
            "success_weight": 1.0 if outcome == "success" else 0.5
        }
        
        # Criar embedding
        text_to_embed = f"{action} {result} {lesson or ''}"
        embedding = self.encoder.encode(text_to_embed).tolist()
        
        # Armazenar no vector DB
        self.db.upsert(
            collection_name=self.collection_name,
            ids=[experience["id"]],
            embeddings=[embedding],
            metadatas=[experience]
        )
        
        return experience["id"]
    
    def retrieve_similar_experiences(self, 
                                   query: str, 
                                   k: int = 5,
                                   outcome_filter: Optional[str] = None) -> List[Dict]:
        """
        Recupera experiências similares à query.
        
        Args:
            query: Situação atual para buscar experiências similares
            k: Número de resultados
            outcome_filter: Filtrar por 'success' ou 'failure'
        
        Returns:
            Lista de experiências ordenadas por relevância
        """
        # Criar embedding da query
        query_embedding = self.encoder.encode(query).tolist()
        
        # Buscar no vector DB
        results = self.db.query(
            collection_name=self.collection_name,
            query_embeddings=[query_embedding],
            n_results=k*2,  # Buscar mais para filtrar
            include=["metadatas", "distances"]
        )
        
        experiences = []
        for metadata, distance in zip(results["metadatas"][0], 
                                     results["distances"][0]):
            # Aplicar filtro de outcome se especificado
            if outcome_filter and metadata["outcome"] != outcome_filter:
                continue
            
            # Calcular score composto (similaridade + recency + success)
            age_days = (datetime.now() - datetime.fromisoformat(metadata["timestamp"])).days
            recency_score = 0.95 ** age_days
            similarity_score = 1 - distance  # Converter distância para similaridade
            
            composite_score = (
                similarity_score * 0.5 +
                recency_score * 0.3 +
                metadata["success_weight"] * 0.2
            )
            
            metadata["score"] = composite_score
            experiences.append(metadata)
        
        # Ordenar por score e retornar top-k
        experiences.sort(key=lambda x: x["score"], reverse=True)
        
        # Atualizar access_count
        for exp in experiences[:k]:
            self._increment_access_count(exp["id"])
        
        return experiences[:k]
    
    def get_successful_patterns(self, action_type: str, k: int = 3) -> List[Dict]:
        """
        Recupera padrões de ações bem-sucedidas de um tipo específico.
        """
        return self.retrieve_similar_experiences(
            query=action_type,
            k=k,
            outcome_filter="success"
        )
    
    def _ensure_collection(self):
        """Garante que a coleção existe no vector DB."""
        try:
            self.db.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception:
            pass  # Coleção já existe
    
    def _increment_access_count(self, experience_id: str):
        """Incrementa contador de acesso para uma experiência."""
        # Implementação depende do vector DB usado
        pass
```

### Uso Prático

```python
# Inicializar
episodic = EpisodicMemory(vector_db_client=pinecone_client)

# Armazenar experiência
episodic.store_experience(
    action="chamar API de clima com cidade='São Paulo'",
    result="{'temperatura': 25, 'umidade': 60}",
    outcome="success",
    lesson="API responde rapidamente para capitais",
    metadata={"api": "weather", "cidade": "São Paulo"}
)

# Recuperar experiências similares
similares = episodic.retrieve_similar_experiences(
    query="preciso buscar clima de Rio de Janeiro",
    k=3
)
# Retorna: experiências com APIs de clima, priorizando sucessos recentes
```

---

## Semantic Memory

Armazena fatos e conhecimento sobre o mundo.

### Implementação

```python
class SemanticMemory:
    """
    Memória semântica para fatos e conhecimento.
    """
    
    def __init__(self, vector_db_client, embedding_model='all-MiniLM-L6-v2'):
        self.db = vector_db_client
        self.encoder = SentenceTransformer(embedding_model)
        self.collection_name = "semantic_memories"
        self._ensure_collection()
    
    def store_fact(self, 
                  fact: str, 
                  category: str = "general",
                  confidence: float = 1.0,
                  source: Optional[str] = None) -> str:
        """
        Armazena um fato na memória semântica.
        
        Args:
            fact: O fato a ser armazenado
            category: Categoria (ex: 'api', 'domain', 'constraint')
            confidence: Nível de confiança (0.0 a 1.0)
            source: Fonte do fato
        """
        fact_entry = {
            "id": f"fact_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "fact": fact,
            "category": category,
            "confidence": confidence,
            "source": source or "inferred",
            "access_count": 0,
            "verification_status": "unverified"
        }
        
        # Criar embedding
        embedding = self.encoder.encode(fact).tolist()
        
        # Armazenar
        self.db.upsert(
            collection_name=self.collection_name,
            ids=[fact_entry["id"]],
            embeddings=[embedding],
            metadatas=[fact_entry]
        )
        
        return fact_entry["id"]
    
    def query_knowledge(self, 
                       query: str, 
                       k: int = 5,
                       category_filter: Optional[str] = None,
                       min_confidence: float = 0.5) -> List[str]:
        """
        Busca fatos relevantes à query.
        
        Returns:
            Lista de fatos ordenados por relevância
        """
        query_embedding = self.encoder.encode(query).tolist()
        
        results = self.db.query(
            collection_name=self.collection_name,
            query_embeddings=[query_embedding],
            n_results=k*2,
            include=["metadatas", "distances"]
        )
        
        facts = []
        for metadata, distance in zip(results["metadatas"][0], 
                                     results["distances"][0]):
            # Aplicar filtros
            if metadata["confidence"] < min_confidence:
                continue
            if category_filter and metadata["category"] != category_filter:
                continue
            
            similarity = 1 - distance
            facts.append({
                "fact": metadata["fact"],
                "confidence": metadata["confidence"],
                "category": metadata["category"],
                "similarity": similarity,
                "score": similarity * metadata["confidence"]
            })
        
        # Ordenar por score combinado
        facts.sort(key=lambda x: x["score"], reverse=True)
        
        return [f["fact"] for f in facts[:k]]
    
    def get_facts_by_category(self, category: str) -> List[Dict]:
        """Recupera todos os fatos de uma categoria."""
        return self.db.get(
            collection_name=self.collection_name,
            where={"category": category}
        )["metadatas"]
    
    def update_confidence(self, fact_id: str, new_confidence: float):
        """Atualiza confiança de um fato baseado em novas evidências."""
        self.db.update(
            collection_name=self.collection_name,
            ids=[fact_id],
            metadatas={"confidence": new_confidence}
        )
```

### Uso Prático

```python
semantic = SemanticMemory(vector_db_client)

# Armazenar fatos sobre APIs
semantic.store_fact(
    fact="API de clima OpenWeather requer chave de API",
    category="api",
    confidence=1.0,
    source="documentacao"
)

semantic.store_fact(
    fact="Limite de rate: 60 chamadas/minuto para plano gratuito",
    category="api",
    confidence=0.95,
    source="documentacao"
)

# Consultar
facts = semantic.query_knowledge(
    query="quais são as limitações da API de clima?",
    category_filter="api",
    k=3
)
# Retorna: fatos sobre limitações e autenticação
```

---

## Procedural Memory

Armazena procedimentos e "como fazer".

### Implementação

```python
class ProceduralMemory:
    """
    Memória procedimental para armazenar workflows e procedimentos.
    """
    
    def __init__(self, vector_db_client, embedding_model='all-MiniLM-L6-v2'):
        self.db = vector_db_client
        self.encoder = SentenceTransformer(embedding_model)
        self.collection_name = "procedural_memories"
        self._ensure_collection()
    
    def store_procedure(self,
                       name: str,
                       steps: List[str],
                       preconditions: Optional[List[str]] = None,
                       expected_outcome: Optional[str] = None,
                       success_rate: float = 0.0) -> str:
        """
        Armazena um procedimento.
        
        Args:
            name: Nome identificador do procedimento
            steps: Lista de passos sequenciais
            preconditions: Condições necessárias para aplicar
            expected_outcome: Resultado esperado
            success_rate: Taxa de sucesso histórica (0.0 a 1.0)
        """
        procedure = {
            "id": f"proc_{name}_{datetime.now().timestamp()}",
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "steps": steps,
            "preconditions": preconditions or [],
            "expected_outcome": expected_outcome or "",
            "success_rate": success_rate,
            "usage_count": 0,
            "version": 1
        }
        
        # Criar embedding combinando nome, steps e preconditions
        text = f"{name} {' '.join(steps)} {' '.join(preconditions or [])}"
        embedding = self.encoder.encode(text).tolist()
        
        self.db.upsert(
            collection_name=self.collection_name,
            ids=[procedure["id"]],
            embeddings=[embedding],
            metadatas=[procedure]
        )
        
        return procedure["id"]
    
    def retrieve_procedure(self, 
                          task_description: str,
                          k: int = 3,
                          check_preconditions: bool = True,
                          context: Optional[Dict] = None) -> List[Dict]:
        """
        Recupera procedimentos adequados para a tarefa.
        
        Args:
            task_description: Descrição da tarefa a ser realizada
            k: Número de procedimentos a retornar
            check_preconditions: Se deve verificar precondições
            context: Contexto atual para verificar precondições
        """
        query_embedding = self.encoder.encode(task_description).tolist()
        
        results = self.db.query(
            collection_name=self.collection_name,
            query_embeddings=[query_embedding],
            n_results=k*3,  # Buscar mais para filtrar
            include=["metadatas", "distances"]
        )
        
        procedures = []
        for metadata, distance in zip(results["metadatas"][0],
                                     results["distances"][0]):
            # Verificar precondições se necessário
            if check_preconditions and context:
                if not self._check_preconditions(metadata["preconditions"], context):
                    continue
            
            similarity = 1 - distance
            # Score considera similaridade e success_rate
            score = similarity * 0.7 + metadata["success_rate"] * 0.3
            
            metadata["relevance_score"] = score
            procedures.append(metadata)
        
        procedures.sort(key=lambda x: x["relevance_score"], reverse=True)
        return procedures[:k]
    
    def update_success_rate(self, procedure_id: str, success: bool):
        """Atualiza taxa de sucesso após execução."""
        procedure = self.db.get(
            collection_name=self.collection_name,
            ids=[procedure_id]
        )["metadatas"][0]
        
        current_rate = procedure["success_rate"]
        usage_count = procedure["usage_count"] + 1
        
        # Atualização exponencial
        new_rate = current_rate + (1.0 if success else 0.0 - current_rate) / usage_count
        
        self.db.update(
            collection_name=self.collection_name,
            ids=[procedure_id],
            metadatas={
                "success_rate": new_rate,
                "usage_count": usage_count
            }
        )
    
    def _check_preconditions(self, preconditions: List[str], context: Dict) -> bool:
        """Verifica se precondições são atendidas no contexto atual."""
        for precondition in preconditions:
            # Lógica simplificada - em produção usar parser mais sofisticado
            if precondition not in str(context):
                return False
        return True
```

### Uso Prático

```python
procedural = ProceduralMemory(vector_db_client)

# Armazenar procedimento de debugging
procedural.store_procedure(
    name="debug_null_pointer_exception",
    steps=[
        "1. Identificar linha do stack trace",
        "2. Verificar inicialização de variáveis na linha",
        "3. Adicionar null checks se necessário",
        "4. Testar a correção"
    ],
    preconditions=["error_type is NullPointerException"],
    expected_outcome="Erro resolvido sem null pointer",
    success_rate=0.85
)

# Recuperar procedimento para tarefa
context = {"error_type": "NullPointerException", "stack_trace": "..."}
procedures = procedural.retrieve_procedure(
    task_description="resolver null pointer exception",
    context=context,
    k=2
)
# Retorna: procedimentos de debugging adequados ao contexto
```

---

## Working Memory

Implementação da memória de curto prazo.

```python
class WorkingMemory:
    """
    Memória de trabalho - equivalente ao contexto do LLM.
    """
    
    def __init__(self, max_tokens=8000):
        self.max_tokens = max_tokens
        self.current_input = None
        self.active_goals = []
        self.intermediate_results = {}
        self.retrieved_cache = {}
        self.conversation_history = []
        self._token_count = 0
    
    def add_intermediate_result(self, key: str, value: Any):
        """Adiciona resultado intermediário."""
        self.intermediate_results[key] = value
        self._update_token_count()
        
        # Se exceder limite, fazer pruning
        if self._token_count > self.max_tokens * 0.9:
            self._prune_least_relevant()
    
    def retrieve_from_cache(self, key: str) -> Optional[Any]:
        """Recupera do cache de memória."""
        return self.retrieved_cache.get(key)
    
    def cache_retrieval(self, key: str, value: Any):
        """Armazena resultado de retrieval no cache."""
        self.retrieved_cache[key] = value
    
    def add_to_history(self, role: str, content: str):
        """Adiciona à história da conversa."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self._update_token_count()
    
    def get_context_for_llm(self) -> str:
        """Compila contexto para prompt do LLM."""
        context_parts = []
        
        # Input atual
        if self.current_input:
            context_parts.append(f"Input: {self.current_input}")
        
        # Objetivos
        if self.active_goals:
            context_parts.append(f"Goals: {', '.join(self.active_goals)}")
        
        # Resultados intermediários relevantes
        if self.intermediate_results:
            context_parts.append("Intermediate Results:")
            for key, value in self.intermediate_results.items():
                context_parts.append(f"  - {key}: {str(value)[:200]}")
        
        # Cache de memória
        if self.retrieved_cache:
            context_parts.append("Retrieved Memories:")
            for key, value in self.retrieved_cache.items():
                context_parts.append(f"  - {key}: {str(value)[:200]}")
        
        return "\n".join(context_parts)
    
    def clear(self):
        """Limpa memória de trabalho."""
        self.__init__(self.max_tokens)
    
    def _update_token_count(self):
        """Estima contagem de tokens."""
        # Estimativa simplificada: ~4 chars por token
        total_chars = len(str(self.__dict__))
        self._token_count = total_chars // 4
    
    def _prune_least_relevant(self):
        """Remove itens menos relevantes quando atinge limite."""
        # Remover itens mais antigos da história
        if len(self.conversation_history) > 5:
            self.conversation_history = self.conversation_history[-5:]
        
        # Limpar resultados intermediários antigos
        if len(self.intermediate_results) > 10:
            keys = list(self.intermediate_results.keys())
            for key in keys[:-10]:
                del self.intermediate_results[key]
```

---

## Integração Completa

Exemplo de uso integrado de todas as memórias:

```python
class IntegratedMemorySystem:
    def __init__(self, vector_db_client):
        self.working = WorkingMemory(max_tokens=6000)
        self.episodic = EpisodicMemory(vector_db_client)
        self.semantic = SemanticMemory(vector_db_client)
        self.procedural = ProceduralMemory(vector_db_client)
    
    def prepare_context(self, user_input: str, goal: str = None):
        """Prepara contexto completo para o LLM."""
        # Setup working memory
        self.working.current_input = user_input
        if goal:
            self.working.active_goals.append(goal)
        
        # Recuperar memórias relevantes
        similar_experiences = self.episodic.retrieve_similar_experiences(
            user_input, k=3
        )
        relevant_facts = self.semantic.query_knowledge(user_input, k=5)
        applicable_procedures = self.procedural.retrieve_procedure(
            user_input, k=2
        )
        
        # Armazenar no cache
        self.working.cache_retrieval("experiences", similar_experiences)
        self.working.cache_retrieval("facts", relevant_facts)
        self.working.cache_retrieval("procedures", applicable_procedures)
        
        # Retornar contexto formatado
        return self.working.get_context_for_llm()
    
    def learn_from_interaction(self, action, result, success: bool):
        """Aprende com interação."""
        # Episódico: armazenar experiência
        self.episodic.store_experience(
            action=str(action),
            result=str(result),
            outcome="success" if success else "failure"
        )
        
        # Semântico: extrair e armazenar fatos (se sucesso)
        if success:
            facts = self._extract_facts(result)
            for fact in facts:
                self.semantic.store_fact(fact)
```

---

## Otimizações

### 1. Caching de Embeddings

```python
from functools import lru_cache

class CachedEmbeddingEncoder:
    def __init__(self, model_name):
        self.encoder = SentenceTransformer(model_name)
        self._cache = {}
    
    def encode(self, text: str) -> np.ndarray:
        if text in self._cache:
            return self._cache[text]
        
        embedding = self.encoder.encode(text)
        self._cache[text] = embedding
        
        # Limitar tamanho do cache
        if len(self._cache) > 1000:
            self._cache.pop(next(iter(self._cache)))
        
        return embedding
```

### 2. Batch Processing

```python
def store_multiple_experiences(self, experiences: List[Dict]):
    """Armazena múltiplas experiências em batch."""
    ids = []
    embeddings = []
    metadatas = []
    
    for exp in experiences:
        text = f"{exp['action']} {exp['result']}"
        embedding = self.encoder.encode(text).tolist()
        
        ids.append(exp['id'])
        embeddings.append(embedding)
        metadatas.append(exp)
    
    # Upsert em batch (mais eficiente)
    self.db.upsert(
        collection_name=self.collection_name,
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )
```

### 3. Garbage Collection

```python
def periodic_cleanup(self, days_threshold: int = 30):
    """Remove memórias antigas e pouco acessadas."""
    cutoff = datetime.now() - timedelta(days=days_threshold)
    
    all_memories = self.db.get(collection_name=self.collection_name)
    
    to_delete = []
    for metadata in all_memories["metadatas"]:
        created = datetime.fromisoformat(metadata["timestamp"])
        
        # Remover se antiga E pouco acessada
        if created < cutoff and metadata.get("access_count", 0) < 3:
            to_delete.append(metadata["id"])
    
    if to_delete:
        self.db.delete(
            collection_name=self.collection_name,
            ids=to_delete
        )
```
