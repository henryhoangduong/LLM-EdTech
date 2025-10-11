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

export type Course = {
  id: string
  name: string
  created_at: string
}

export type getCoursesQueryFnResponse = {
  items: Course[]
  page: number
  page_size: number
  total: number
  pages: number
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  streaming?: boolean
  state?: {
    sources?: Array<{
      file_name: string
      content?: string
      page?: number
      relevance?: number
    }>
    followUpQuestions?: string[]
  }
  followUpQuestions?: string[]
}
