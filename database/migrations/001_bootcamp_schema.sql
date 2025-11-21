-- =========================================
-- HR Assistant - Bootcamp Schema
-- =========================================
-- Simple multi-tenant schema for bootcamp project
-- Use with Supabase/Neon + ChromaDB

-- Enable UUID extension
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

-- -------------------------
-- Table: messages
-- -------------------------
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_chat ON messages(chat_id);

-- -------------------------
-- Table: message_feedback
-- -------------------------
CREATE TABLE message_feedback (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  rating INT NOT NULL CHECK (rating IN (-1, 1)),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(message_id)
);

-- -------------------------
-- Table: documents
-- -------------------------
-- Stores file metadata only
-- Actual files: uploads/ folder or Supabase Storage
-- Embeddings: ChromaDB
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename VARCHAR(500) NOT NULL,
  file_path VARCHAR(1000) NOT NULL,
  file_type VARCHAR(50) NOT NULL,
  file_size BIGINT NOT NULL,
  uploaded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_documents_company ON documents(company_id);
CREATE INDEX idx_documents_user ON documents(user_id);

-- -------------------------
-- Seed data (optional)
-- -------------------------
INSERT INTO companies (id, name)
VALUES ('00000000-0000-0000-0000-000000000001', 'Demo Company');

COMMIT;
