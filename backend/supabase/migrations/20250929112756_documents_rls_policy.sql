ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for document owner only" ON documents
    FOR SELECT USING (auth.role() = 'authenticated' AND user_id = auth.uid());

CREATE POLICY "Enable insert for document owner only" ON documents
    FOR INSERT WITH CHECK (auth.role() = 'authenticated' AND user_id = auth.uid());

CREATE POLICY "Enable update for document owner only" ON documents
    FOR UPDATE USING (auth.role() = 'authenticated' AND user_id = auth.uid());

CREATE POLICY "Enable delete for document owner only" ON documents
    FOR DELETE USING (auth.role() = 'authenticated' AND user_id = auth.uid());