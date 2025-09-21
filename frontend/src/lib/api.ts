import { User } from '@/types/types'
import API from './axios-client'
//*********************************************************************
//***************************** AUTH **********************************
//*********************************************************************
export const loginMutationFn = async ({ email, password }: { email: string; password: string }): Promise<any> => {
  const data = { email, password }
  const response = await API.post('/auth/login', data)
  return response.data
}

export const signupMutationFn = async ({
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

export const logoutMutationFn = async () => {
  const response = await API.post('/auth/signout')
  return response.data
}

export const getCurrentUserQueryFn = async (): Promise<User> => {
  const response = await API.get(`/auth/currentUser`)
  return response.data
}

export const getCourseByIdQueryFn = async (id: string): Promise<any> => {
  const response = await API.get(`/course/${id}`)
  return response.data
}

export const createCourseMutationFn = async ({
  name,
  description
}: {
  name: string
  description?: string
}): Promise<any> => {
  const response = await API.post(`/course`, { name: name, description: description })
  return response.data
}

export const getCoursesQueryFn = async () => {
  const response = await API.get(`/course`)
  return response.data
}
