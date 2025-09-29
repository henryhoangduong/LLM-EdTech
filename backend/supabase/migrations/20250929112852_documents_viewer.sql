CREATE OR REPLACE VIEW document_details AS
SELECT 
    id,
    user_id,
    data->'metadata'->>'filename' AS filename,
    data->'metadata'->>'type' AS file_type,
    (data->'metadata'->>'enabled')::boolean AS enabled,
    data->'metadata'->>'size' AS size,
    data->'metadata'->>'loader' AS loader,
    data->'metadata'->>'parser' AS parser,
    data->'metadata'->>'splitter' AS splitter,
    data->'metadata'->>'uploadedAt' AS uploaded_at,
    data->'metadata'->>'file_path' AS file_path,
    data->'metadata'->>'parsing_status' AS parsing_status,
    data->'metadata'->>'parsed_at' AS parsed_at,
    created_at,
    updated_at
FROM documents;
DO $$
BEGIN
    RAISE NOTICE 'Documents table and related objects created successfully';
END $$; 