CREATE INDEX IF NOT EXISTS idx_documents_data ON documents USING GIN (data);
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);