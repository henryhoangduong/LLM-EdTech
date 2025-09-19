import { User } from '@/types/types'
import { createContext, useContext } from 'react'
import React from 'react'
type AuthContextType = {
  user: User
}
const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthContextProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return <AuthContext.Provider value={undefined}>{children}</AuthContext.Provider>
}

export const useAuthContext = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useCurrentUserContext must be used within a AuthProvider')
  }
  return context
}
