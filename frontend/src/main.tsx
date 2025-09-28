import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import '@/styles/globals.css'
import QueryProvider from './context/query-provider.tsx'
import { AuthContextProvider } from './context/auth-provider.tsx'
import { Worker } from '@react-pdf-viewer/core'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <QueryProvider>
    <AuthContextProvider>
      <Worker workerUrl='https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js'>
        <App />
      </Worker>
    </AuthContextProvider>
  </QueryProvider>
)
