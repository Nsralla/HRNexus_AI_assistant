-- =========================================
-- HR Assistant LLM - Simple Schema Migration
-- =========================================
-- PostgreSQL with ChromaDB for vector storage

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -------------------------
-- Table: companies
-- -------------------------
CREATE TABLE companies (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- -------------------------
-- Table: users
-- -------------------------
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'employee' CHECK (role IN ('admin', 'hr_manager', 'employee')),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(company_id, email)
);

-- -------------------------
-- Table: chats
-- -------------------------
CREATE TABLE chats (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  title VARCHAR(500) DEFAULT 'New Conversation',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chats_user ON chats(user_id);
CREATE INDEX idx_chats_company ON chats(company_id);

-- -------------------------
-- Table: messages
-- -------------------------
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_chat ON messages(chat_id);

-- -------------------------
-- Table: documents
-- -------------------------
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  title VARCHAR(500) NOT NULL,
  file_path VARCHAR(1000) NOT NULL,
  file_type VARCHAR(50) NOT NULL,
  uploaded_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  uploaded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_documents_company ON documents(company_id);

-- -------------------------
-- Table: document_chunks
-- -------------------------
-- Note: Embeddings stored in ChromaDB, this tracks metadata only
CREATE TABLE document_chunks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index INT NOT NULL,
  content TEXT NOT NULL,
  chroma_id VARCHAR(255) NOT NULL, -- Reference to ChromaDB document ID
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chunks_document ON document_chunks(document_id);
CREATE INDEX idx_chunks_chroma ON document_chunks(chroma_id);

-- -------------------------
-- Seed data (optional)
-- -------------------------
INSERT INTO companies (id, name)
VALUES ('00000000-0000-0000-0000-000000000001', 'Demo Company');

COMMIT;
