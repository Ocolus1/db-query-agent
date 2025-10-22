"""Conversational layer for handling casual conversation and natural responses."""

import logging
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ConversationalLayer:
    """Handles casual conversation and generates natural responses."""
    
    def __init__(self):
        """Initialize conversational layer."""
        pass
    
    def handle_casual_conversation(self, query: str) -> Optional[str]:
        """
        Detect and handle casual conversation that doesn't require database queries.
        
        Args:
            query: User's message
            
        Returns:
            Casual response if detected, None if it's a database query
        """
        query_lower = query.lower().strip()
        
        # Greetings
        greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in query_lower for greeting in greetings):
            return "Hello! 👋 I'm your database assistant. I can help you query your database using natural language. Just ask me anything about your data!"
        
        # How are you
        if any(phrase in query_lower for phrase in ['how are you', 'how do you do', 'how are things']):
            return "I'm doing great, thank you for asking! 😊 I'm here to help you explore your database. What would you like to know about your data?"
        
        # What can you do / Help
        if any(phrase in query_lower for phrase in ['what can you do', 'what do you do', 'help me', 'help', 'capabilities']):
            return """I'm an AI database assistant! Here's what I can do:

📊 **Query your database** - Ask me questions in plain English
🔍 **Find data** - "Show me all active users"
📈 **Analyze data** - "What's the total revenue?"
💬 **Remember context** - I can handle follow-up questions
📋 **Explain queries** - I'll show you the SQL I generate

Try asking me something like:
- "How many users do we have?"
- "Show me the top 10 products"
- "What's the average order value?"

What would you like to know?"""
        
        # Time/Date
        if any(phrase in query_lower for phrase in ['what time', 'what is the time', 'current time', 'what date', 'what is the date', 'today']):
            now = datetime.now()
            return f"The current time is **{now.strftime('%I:%M %p')}** and today's date is **{now.strftime('%B %d, %Y')}**. 📅\n\nIs there anything about your database you'd like to know?"
        
        # Thank you
        if any(phrase in query_lower for phrase in ['thank you', 'thanks', 'thx', 'appreciate']):
            return "You're welcome! 😊 Feel free to ask me anything else about your database!"
        
        # Goodbye
        if any(phrase in query_lower for phrase in ['bye', 'goodbye', 'see you', 'see ya', 'farewell']):
            return "Goodbye! 👋 Come back anytime you need to query your database!"
        
        # Who are you
        if any(phrase in query_lower for phrase in ['who are you', 'what are you', 'your name']):
            return "I'm DB Query Agent, an AI-powered database assistant! 🤖 I help you query your database using natural language instead of SQL. Just ask me questions about your data and I'll handle the rest!"
        
        # Jokes
        if 'joke' in query_lower or 'funny' in query_lower:
            return "Why do programmers prefer dark mode? Because light attracts bugs! 😄\n\nNow, let's get back to your data - what would you like to know?"
        
        # If it's very short and doesn't look like a query, might be casual
        if len(query_lower.split()) <= 3 and not any(word in query_lower for word in ['show', 'get', 'find', 'list', 'count', 'how many', 'what', 'where', 'select']):
            return f"I'm not sure I understand '{query}'. Could you please ask me a question about your database? For example: 'How many users do we have?' or 'Show me all orders'."
        
        # Not a casual conversation - return None to trigger database query
        return None
    
    def generate_natural_response(self, query: str, result: Dict[str, Any]) -> str:
        """
        Generate a natural, conversational response based on query results.
        
        Args:
            query: Original user query
            result: Query result with SQL, data, etc.
            
        Returns:
            Natural language response
        """
        # Check if there's already a natural response
        if 'natural_response' in result and result['natural_response']:
            return result['natural_response']
        
        # Check if we have results
        if 'results' not in result or not result['results']:
            return "I executed your query, but it didn't return any results. The data you're looking for might not exist in the database."
        
        results_data = result['results']
        row_count = len(results_data)
        
        # For single row with single column (like COUNT, SUM, AVG queries)
        if row_count == 1 and len(results_data[0]) == 1:
            value = results_data[0][0]
            
            # Try to get column name
            if hasattr(results_data[0], '_fields'):
                col_name = results_data[0]._fields[0]
                
                # Make it more conversational based on column name
                if 'count' in col_name.lower() or 'total' in col_name.lower():
                    # Extract what we're counting from the query
                    query_lower = query.lower()
                    if 'user' in query_lower:
                        return f"You have **{value}** users in your database."
                    elif 'order' in query_lower:
                        return f"You have **{value}** orders in your database."
                    elif 'product' in query_lower:
                        return f"You have **{value}** products in your database."
                    else:
                        return f"The count is **{value}**."
                
                elif 'avg' in col_name.lower() or 'average' in col_name.lower():
                    return f"The average value is **{value}**."
                
                elif 'sum' in col_name.lower():
                    return f"The total sum is **{value}**."
                
                elif 'max' in col_name.lower():
                    return f"The maximum value is **{value}**."
                
                elif 'min' in col_name.lower():
                    return f"The minimum value is **{value}**."
                
                else:
                    return f"The **{col_name}** is **{value}**."
            else:
                return f"The result is **{value}**."
        
        # For multiple rows
        elif row_count > 1:
            # Check if it's a small result set (show preview)
            if row_count <= 5:
                return f"I found **{row_count}** results. Here's what I found:"
            else:
                return f"I found **{row_count}** results. You can view them in the details below."
        
        # For single row with multiple columns
        else:
            return f"I found 1 result with multiple fields. Check the details below to see all the information."
    
    def is_database_query(self, query: str) -> bool:
        """
        Determine if a query is intended for the database.
        
        Args:
            query: User's message
            
        Returns:
            True if it's a database query, False if casual conversation
        """
        # Check if casual conversation handler returns something
        casual_response = self.handle_casual_conversation(query)
        return casual_response is None
