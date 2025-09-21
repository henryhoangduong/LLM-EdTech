import useAuth from '@/hooks/api/use-auth'
import { User } from '@/types/types'
import { createContext, useContext } from 'react'
import React from 'react'
type AuthContextType = {
  user?: User
  isLoading: boolean
}
const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthContextProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { data: authData, error: authError, isLoading, isFetching, refetch: refetchAuth } = useAuth()

  return <AuthContext.Provider value={{ user: authData, isLoading }}>{children}</AuthContext.Provider>
}

export const useAuthContext = () => {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useCurrentUserContext must be used within a AuthProvider')
  }
  return context
}
