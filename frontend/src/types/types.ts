export type User = {
  id: string
  name: string
  email: string
  profile_pic: string | null
}
export interface Document {
  id: string
  content: string
  metadata: Record<string, any>
}
export interface Documents {
  id: string
  documents: Document[]
  metadata: Metadata
}
export interface Metadata {
  filename: string
  type: string
  chunk_number?: number
  page_number?: number
  parsing_status?: string
  size?: string
  loader?: string
  parser?: string
  splitter?: string
  file_path: string
  folder_path?: string
  is_folder?: boolean
  enabled?: boolean
  uploadedAt?: string
}
