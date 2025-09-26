import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import '@/styles/globals.css'
import QueryProvider from './context/query-provider.tsx'
import { AuthContextProvider } from './context/auth-provider.tsx'
import { Toaster } from './components/ui/toaster.tsx'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <QueryProvider>
      <AuthContextProvider>
        <App />
        <Toaster />
      </AuthContextProvider>
    </QueryProvider>
  </React.StrictMode>
)
