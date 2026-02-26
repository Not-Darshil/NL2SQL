import sqlparse
from typing import Optional, List
from app.services.llm_service import llm_service
from app.core.database import Base
from sqlalchemy import text

class NL2SQLAgent:
    def __init__(self):
        self.system_prompt = """
        You are a SQL expert for TableMind AI.
        Generate ONLY a valid PostgreSQL SELECT query based on the database schema provided.
        Rules:
        - ONLY SELECT queries are allowed.
        - NO DELETE, DROP, UPDATE, INSERT, or ALTER.
        - Use appropriate joins.
        - Return the query only, no explanation.
        """

    def _is_safe(self, sql: str) -> bool:
        """
        Simple validation to ensure only SELECT queries are executed.
        """
        parsed = sqlparse.parse(sql)
        for statement in parsed:
            if statement.get_type() != "SELECT":
                return False
        
        # Additional check for dangerous keywords in case parsing misses something
        forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "ALTER"]
        sql_upper = sql.upper()
        for f in forbidden:
            if f in sql_upper:
                return False
                
        return True

    def _get_schema_context(self) -> str:
        # In a real scenario, this would dynamically read the metadata.
        # For now, providing the core table structure from our design.
        return """
        Tables:
        - users (id, full_name, email, role, is_active)
        - menu_categories (id, name, description)
        - menu_items (id, category_id, name, description, price, is_vegetarian, is_spicy, is_available)
        - orders (id, user_id, status, total_amount, created_at)
        - order_items (id, order_id, menu_item_id, quantity, price_at_order, subtotal)
        - payments (id, order_id, payment_method, payment_status, total_amount)
        - chat_logs (id, user_id, message, sender, intent)
        """

    async def generate_sql(self, user_query: str) -> Optional[str]:
        schema = self._get_schema_context()
        prompt = f"Schema:\n{schema}\n\nUser Question: {user_query}\nSQL Query:"
        
        sql = await llm_service.generate_response(prompt, system_prompt=self.system_prompt, temperature=0.0)
        sql = sql.strip().replace("```sql", "").replace("```", "").strip()
        
        if self._is_safe(sql):
            return sql
        return None

nl2sql_agent = NL2SQLAgent()
