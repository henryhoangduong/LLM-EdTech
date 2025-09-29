INSERT INTO storage.buckets (id, name, public)
VALUES('henry-bucket','henry-bucket',false)
ON CONFLICT (id) DO NOTHING;

ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;