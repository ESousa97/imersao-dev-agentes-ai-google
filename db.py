# -*- coding: utf-8 -*-
"""
Módulo de Banco de Dados - Persistência híbrida SQLite + Chroma
"""

import sqlite3
import json
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from models import MemoryItem, Reflection, Nudge

class DatabaseManager:
    def __init__(self, db_path: str = "./agent_memory.db", chroma_path: str = "./chroma_mem", api_key: str = None):
        self.db_path = db_path
        self.chroma_path = chroma_path
        self.api_key = api_key
        
        # Inicializa SQLite
        self._init_sqlite()
        
        # Inicializa Chroma para embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", 
            google_api_key=api_key
        )
        self.vectorstore = Chroma(
            collection_name="memories",
            embedding_function=self.embeddings,
            persist_directory=chroma_path
        )

    def _init_sqlite(self):
        """Inicializa as tabelas SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de memórias
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP,
            source_kind TEXT,
            source_tags TEXT,
            importance INTEGER,
            sentiment TEXT,
            summary TEXT,
            deadlines TEXT,
            memory_data TEXT
        )
        """)
        
        # Tabela de reflexões
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reflections (
            id TEXT PRIMARY KEY,
            generated_at TIMESTAMP,
            triggers TEXT,
            reflection_data TEXT
        )
        """)
        
        # Tabela de nudges
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS nudges (
            id TEXT PRIMARY KEY,
            generated_at TIMESTAMP,
            type TEXT,
            message TEXT,
            memory_ids TEXT,
            priority INTEGER,
            is_read BOOLEAN
        )
        """)
        
        conn.commit()
        conn.close()

    def salvar_memoria(self, memory_item: Dict) -> str:
        """Salva uma memória no SQLite e Chroma"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Converte datetime para string se necessário
        created_at = memory_item["meta"]["created_at"]
        if isinstance(created_at, datetime):
            created_at = created_at.isoformat()
        
        # Salva no SQLite
        cursor.execute("""
        INSERT OR REPLACE INTO memories 
        (id, created_at, source_kind, source_tags, importance, sentiment, summary, deadlines, memory_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            memory_item["id"],
            created_at,
            memory_item["meta"]["kind"],
            json.dumps(memory_item["meta"]["tags"]),
            memory_item["importance"],
            memory_item["sentiment"],
            memory_item["summary"],
            json.dumps(memory_item["deadlines"]),
            json.dumps(memory_item, default=str)  # Adiciona default=str para serializar datetime
        ))
        
        conn.commit()
        conn.close()
        
        # Prepara texto para embedding
        text_for_embed = "\n".join([
            memory_item.get("summary", ""),
            *memory_item.get("facts", []),
            *memory_item.get("goals", []),
            *memory_item.get("decisions", []),
            *memory_item.get("blockers", []),
            *memory_item.get("questions", [])
        ])
        
        # Salva no Chroma se há conteúdo
        if text_for_embed.strip():
            metadata = {
                "id": memory_item["id"],
                "tags": json.dumps(memory_item["meta"]["tags"]),
                "kind": memory_item["meta"]["kind"],
                "importance": memory_item["importance"],
                "sentiment": memory_item["sentiment"],
                "created_at": created_at  # Usa a versão string do created_at
            }
            
            self.vectorstore.add_texts([text_for_embed], metadatas=[metadata])
        
        return memory_item["id"]

    def buscar_memorias_semantica(self, query: str, k: int = 10) -> List[Dict]:
        """Busca semântica usando Chroma"""
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            
            # Recupera dados completos do SQLite usando os IDs
            memory_ids = [doc.metadata.get("id") for doc in docs if doc.metadata.get("id")]
            
            if not memory_ids:
                return []
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            placeholders = ",".join(["?" for _ in memory_ids])
            cursor.execute(f"""
            SELECT memory_data FROM memories WHERE id IN ({placeholders})
            ORDER BY importance DESC, created_at DESC
            """, memory_ids)
            
            results = []
            for row in cursor.fetchall():
                try:
                    memory_data = json.loads(row[0])
                    results.append(memory_data)
                except json.JSONDecodeError:
                    continue
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"Erro na busca semântica: {e}")
            return []

    def buscar_memorias_filtros(self, 
                               tags: List[str] = None, 
                               kind: str = None,
                               importance_min: int = 1,
                               days_back: int = 30,
                               limit: int = 50) -> List[Dict]:
        """Busca com filtros específicos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT memory_data FROM memories WHERE 1=1"
        params = []
        
        if days_back:
            cutoff_date = datetime.now() - timedelta(days=days_back)
            query += " AND created_at >= ?"
            params.append(cutoff_date.isoformat())
        
        if kind:
            query += " AND source_kind = ?"
            params.append(kind)
            
        if importance_min > 1:
            query += " AND importance >= ?"
            params.append(importance_min)
        
        if tags:
            # Busca por tags (busca JSON contains)
            for tag in tags:
                query += " AND source_tags LIKE ?"
                params.append(f'%"{tag}"%')
        
        query += " ORDER BY importance DESC, created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        
        results = []
        for row in cursor.fetchall():
            try:
                memory_data = json.loads(row[0])
                results.append(memory_data)
            except json.JSONDecodeError:
                continue
        
        conn.close()
        return results

    def buscar_memoria_por_id(self, memory_id: str) -> Optional[Dict]:
        """Busca uma memória específica por ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT memory_data FROM memories WHERE id = ?", (memory_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            try:
                return json.loads(row[0])
            except json.JSONDecodeError:
                return None
        return None

    def salvar_reflexao(self, reflection: Dict) -> str:
        """Salva uma reflexão"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT OR REPLACE INTO reflections (id, generated_at, triggers, reflection_data)
        VALUES (?, ?, ?, ?)
        """, (
            reflection["id"],
            reflection["generated_at"],
            json.dumps(reflection["triggers"]),
            json.dumps(reflection)
        ))
        
        conn.commit()
        conn.close()
        
        return reflection["id"]

    def salvar_nudge(self, nudge: Dict) -> str:
        """Salva um nudge"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT OR REPLACE INTO nudges 
        (id, generated_at, type, message, memory_ids, priority, is_read)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            nudge["id"],
            nudge["generated_at"],
            nudge["type"],
            nudge["message"],
            json.dumps(nudge["memory_ids"]),
            nudge["priority"],
            nudge["is_read"]
        ))
        
        conn.commit()
        conn.close()
        
        return nudge["id"]

    def buscar_nudges_nao_lidos(self) -> List[Dict]:
        """Busca nudges não lidos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, generated_at, type, message, memory_ids, priority, is_read
        FROM nudges 
        WHERE is_read = 0 
        ORDER BY priority DESC, generated_at DESC
        """)
        
        nudges = []
        for row in cursor.fetchall():
            nudges.append({
                "id": row[0],
                "generated_at": row[1],
                "type": row[2],
                "message": row[3],
                "memory_ids": json.loads(row[4]),
                "priority": row[5],
                "is_read": bool(row[6])
            })
        
        conn.close()
        return nudges

    def marcar_nudge_lido(self, nudge_id: str):
        """Marca um nudge como lido"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE nudges SET is_read = 1 WHERE id = ?", (nudge_id,))
        
        conn.commit()
        conn.close()

    def listar_tags(self) -> List[str]:
        """Lista todas as tags únicas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT source_tags FROM memories")
        
        all_tags = set()
        for row in cursor.fetchall():
            try:
                tags = json.loads(row[0])
                all_tags.update(tags)
            except (json.JSONDecodeError, TypeError):
                continue
        
        conn.close()
        return sorted(list(all_tags))

    def estatisticas(self) -> Dict:
        """Retorna estatísticas básicas do banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Contagem por tipo
        cursor.execute("SELECT source_kind, COUNT(*) FROM memories GROUP BY source_kind")
        tipos = dict(cursor.fetchall())
        
        # Contagem por importância
        cursor.execute("SELECT importance, COUNT(*) FROM memories GROUP BY importance")
        importancias = dict(cursor.fetchall())
        
        # Total de memórias
        cursor.execute("SELECT COUNT(*) FROM memories")
        total_memories = cursor.fetchone()[0]
        
        # Nudges não lidos
        cursor.execute("SELECT COUNT(*) FROM nudges WHERE is_read = 0")
        nudges_nao_lidos = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_memories": total_memories,
            "by_type": tipos,
            "by_importance": importancias,
            "unread_nudges": nudges_nao_lidos,
            "total_tags": len(self.listar_tags())
        }
