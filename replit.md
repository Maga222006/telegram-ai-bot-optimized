# replit.md

## Overview

This is a Telegram bot application built with Python that serves as an AI assistant with multi-agent capabilities. The application integrates with various external services and provides users with intelligent responses through a sophisticated agent system. The bot handles text, voice, and image inputs, and can perform various tasks including web searches, GitHub repository creation, weather information, and financial data retrieval.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Aiogram (Python Telegram Bot framework)
- **Agent System**: LangGraph with multi-agent architecture using supervisor pattern
- **Database**: PostgreSQL with SQLAlchemy ORM for async operations
- **Connection Management**: Custom connection pooling system for optimized database performance
- **AI/ML**: Integration with multiple LLM providers (Groq, OpenAI) for different capabilities

### Database Design
- **ORM**: SQLAlchemy with async support
- **Connection Pool**: Custom-built centralized connection pool manager
- **Schema**: Two main tables - `users` (user profiles and locations) and `user_config` (API keys and configuration)
- **External Storage**: PostgreSQL store for agent memory and checkpoints

### Multi-Agent System
- **Supervisor Agent**: Orchestrates task delegation between specialized agents
- **Coding Agent**: Handles code generation and programming tasks
- **Research Agent**: Performs web searches and information gathering
- **Memory System**: Short-term and long-term memory with semantic storage

## Key Components

### Bot Interface (`bot/`)
- **Handlers**: Message processing for text, voice, images, and location
- **Keyboards**: Interactive reply keyboards for user configuration
- **FSM**: Finite State Machine for configuration flows

### Agent System (`agents/`)
- **Multi-Agent Coordinator**: Supervisor pattern for agent orchestration
- **Specialized Tools**: Web search, GitHub integration, weather API, finance data
- **Memory Management**: Semantic memory storage with PostgreSQL backend

### Database Layer (`database/`)
- **Connection Pool**: Centralized connection management for optimal performance
- **Models**: SQLAlchemy models for users and configuration
- **Operations**: Async CRUD operations for all database interactions

### Media Processing (`media/`)
- **Speech-to-Text**: Voice message transcription using OpenAI API
- **Text-to-Speech**: Response audio generation using gTTS
- **Image Processing**: Image analysis and description using vision models

## Data Flow

1. **User Input**: Messages received through Telegram bot interface
2. **Preprocessing**: Voice/image converted to text, location data processed
3. **Agent Processing**: Supervisor agent routes tasks to appropriate specialized agents
4. **Tool Execution**: Agents use tools (web search, APIs, etc.) to gather information
5. **Memory Storage**: Relevant information stored in PostgreSQL for future reference
6. **Response Generation**: LLM generates contextual responses based on gathered data
7. **Output**: Responses sent back to user via Telegram (text, voice, or multimedia)

## External Dependencies

### AI/ML Services
- **Groq**: Primary LLM provider for agent reasoning and text generation
- **OpenAI**: Speech-to-text, image processing, and backup text generation
- **Hugging Face**: Sentence transformers for semantic embeddings

### External APIs
- **Telegram Bot API**: Core bot functionality
- **GitHub API**: Repository creation and management
- **OpenWeatherMap**: Weather information retrieval
- **Yahoo Finance**: Financial data and news
- **Tavily**: Web search capabilities
- **Wikipedia**: Knowledge base access

### Infrastructure
- **PostgreSQL**: Primary database for user data and agent memory
- **gTTS**: Text-to-speech conversion
- **Geopy**: Geocoding and location services

## Deployment Strategy

### Development Environment
- **Local PostgreSQL**: Database running on localhost
- **Environment Variables**: Configuration through `.env` file
- **Token Management**: Hardcoded bot token (should be externalized for production)

### Production Considerations
- **Database Connection**: Optimized connection pooling for high concurrency
- **Error Handling**: Comprehensive error handling throughout the application
- **Logging**: Structured logging for monitoring and debugging
- **Resource Management**: Proper cleanup of database connections and temporary files

### Scaling Approach
- **Connection Pooling**: Designed to handle multiple concurrent users efficiently
- **Agent Memory**: Persistent storage allows for stateful conversations
- **Modular Design**: Easy to add new agents and tools as needed
- **API Rate Limiting**: Built-in considerations for external API usage limits

### Security Features
- **User Data Protection**: Secure storage of user configurations and API keys
- **Database Security**: Async operations with proper transaction handling
- **Input Validation**: Comprehensive validation of user inputs and external data