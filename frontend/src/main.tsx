import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import '@/styles/globals.css'
import QueryProvider from './context/query-provider.tsx'
import { AuthContextProvider } from './context/auth-provider.tsx'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <QueryProvider>
    <AuthContextProvider>
      <App />
    </AuthContextProvider>
  </QueryProvider>
)
