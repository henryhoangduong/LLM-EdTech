import { getCoursesQueryFnResponse, HenryDoc, User } from '@/types/types'
import API from './axios-client'

//*********************************************************************
//***************************** AUTH **********************************
//*********************************************************************
const loginMutationFn = async ({ email, password }: { email: string; password: string }): Promise<any> => {
  const data = { email, password }
  const response = await API.post('/auth/login', data)
  return response.data
}

const signupMutationFn = async ({
  email,
  password,
  name
}: {
  email: string
  password: string
  name: string
}): Promise<any> => {
  const response = await API.post('/auth/signup', { email, password, name })
  return response.data
}

const logoutMutationFn = async () => {
  const response = await API.post('/auth/signout')
  return response.data
}

const getCurrentUserQueryFn = async (): Promise<User> => {
  const response = await API.get(`/auth/currentUser`)
  return response.data
}

//*********************************************************************
//***************************** COURSE ********************************
//*********************************************************************
const getCourseByIdQueryFn = async (id: string): Promise<any> => {
  const response = await API.get(`/course/${id}`)
  return response.data
}

const createCourseMutationFn = async ({ name, description }: { name: string; description?: string }): Promise<any> => {
  const response = await API.post(`/course`, { name: name, description: description })
  return response.data
}

const getCoursesQueryFn = async ({
  page = 1,
  limit = 10
}: {
  page?: number
  limit?: number
}): Promise<getCoursesQueryFnResponse> => {
  const response = await API.get(`/course`, {
    params: { page, limit }
  })
  return response.data
}

//*********************************************************************
//***************************** INGESTION *****************************
//*********************************************************************
const ingestionMutationFn = async (files: File[]) => {
  const form = new FormData()
  Array.from(files).forEach((file) => {
    form.append('files', file)
  })
  const response = await API.post('/ingestion', form)
  return response.data
}

const ingestionQueryFn = async (): Promise<HenryDoc[]> => {
  const res = await API.get('ingestion')
  return res.data
}

//*********************************************************************
//***************************** CHAT **********************************
//*********************************************************************
const sendMessage = async (message: string) => {
  try {
    const baseURL = import.meta.env.VITE_API_BASE_URL
    const response = await fetch(`${baseURL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message
      })
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}

const handleChatStream = async (
  response: Response,
  onChunk: (content: string, state: any) => void,
  onComplete: () => void
): Promise<void> => {
  const reader = response.body?.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  console.log('🔄 Starting stream handling...')

  try {
    while (reader) {
      const { value, done } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      buffer += chunk
      // Split buffer by double newlines and process complete messages
      const messages = buffer.split('\n\n')
      buffer = messages.pop() || '' // Keep the last incomplete chunk in buffer

      for (const message of messages) {
        if (!message.trim()) continue

        try {
          // Remove 'data: ' prefix if it exists
          const jsonStr = message.replace(/^data: /, '')
          // console.log('📦 Raw chunk:', jsonStr)

          const data = JSON.parse(jsonStr)
          console.log('🔍 Parsed data:', data)

          if (data.error) {
            console.error('❌ Stream error:', data.error)
            continue
          }

          // Pass both content and state to the callback
          if (data.content !== undefined) {
            // console.log('📝 Content update:', { content: data.content, state: data.state })
            onChunk(data.content, data.state)
          } else if (data.state) {
            // console.log('🔄 State-only update:', data.state)
            onChunk('', data.state)
          }
        } catch (e) {
          console.error('❌ Error parsing stream chunk:', e)
        }
      }
    }
  } finally {
    console.log('✅ Stream handling complete')
    reader?.releaseLock()
    onComplete()
  }
}
export {
  loginMutationFn,
  signupMutationFn,
  logoutMutationFn,
  getCurrentUserQueryFn,
  getCourseByIdQueryFn,
  createCourseMutationFn,
  getCoursesQueryFn,
  ingestionMutationFn,
  ingestionQueryFn,
  sendMessage,
  handleChatStream
}
