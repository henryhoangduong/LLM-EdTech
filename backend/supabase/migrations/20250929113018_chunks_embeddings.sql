CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks_embeddings (
    id TEXT PRIMARY KEY,  -- Using string UUIDs as per LangChain convention
    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    data JSONB NOT NULL DEFAULT '{}'::jsonb,
    embedding vector(1536) NOT NULL,  -- OpenAI's default embedding size is 1536 dimensions
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_document FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks_embeddings(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_user_id ON chunks_embeddings(user_id);
CREATE INDEX IF NOT EXISTS idx_chunks_data ON chunks_embeddings USING GIN (data);

CREATE INDEX IF NOT EXISTS idx_chunks_embeddings_embedding_hnsw
  ON chunks_embeddings
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);


CREATE TRIGGER update_chunks_embeddings_updated_at
    BEFORE UPDATE ON chunks_embeddings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


ALTER TABLE chunks_embeddings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for chunk owner only" ON chunks_embeddings
    FOR SELECT USING (auth.role() = 'authenticated' AND user_id = auth.uid());

CREATE POLICY "Enable insert for chunk owner only" ON chunks_embeddings
    FOR INSERT WITH CHECK (auth.role() = 'authenticated' AND user_id = auth.uid());

CREATE POLICY "Enable update for chunk owner only" ON chunks_embeddings
    FOR UPDATE USING (auth.role() = 'authenticated' AND user_id = auth.uid());

CREATE POLICY "Enable delete for chunk owner only" ON chunks_embeddings
    FOR DELETE USING (auth.role() = 'authenticated' AND user_id = auth.uid());

CREATE OR REPLACE VIEW document_chunks AS
SELECT 
    c.id AS chunk_id,
    c.document_id,
    c.user_id,
    c.data->>'page_content' AS content,
    c.data->'metadata' AS metadata,
    d.data AS document_data,
    c.created_at,
    c.updated_at
FROM chunks_embeddings c
JOIN documents d ON c.document_id = d.id;

DO $$
BEGIN
    RAISE NOTICE 'Chunks embeddings table and related objects created successfully';
END $$; 