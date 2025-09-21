import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import '@/styles/globals.css'
import QueryProvider from './context/query-provider.tsx'
import { AuthContextProvider } from './context/auth-provider.tsx'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <QueryProvider>
      <AuthContextProvider>
        <App />
      </AuthContextProvider>
    </QueryProvider>
  </React.StrictMode>
)
