import './styles/globals.css'
import AppRoutes from './routes'
import { Toaster } from '@/components/ui/sonner'
import { pdfjs } from 'react-pdf'
pdfjs.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.js'

function App() {
  return (
    <>
      <AppRoutes />
      <Toaster />
    </>
  )
}

export default App
