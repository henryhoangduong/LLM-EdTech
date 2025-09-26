import AnalyticSection from '@/components/document/analytic-section'
import { PlusIcon } from 'lucide-react'
import { FileUploadModal } from '@/components/document/file-upload-document'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from '@/hooks/use-toast'
import DocumentTable from '@/components/document/document-table'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useCourse } from '@/hooks/api/use-coure'
import { useParams } from 'react-router-dom'

const Course = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const handleModal = () => {
    setIsModalOpen(!isModalOpen)
  }

  const { mutate, isPending } = useMutation({
    // mutationFn: ingestionMutationFn
  })
  const queryClient = useQueryClient()
  const { id } = useParams<{ id: string }>()
  const onSubmit = async (values: FileList) => {
    if (isPending) return
    mutate(values, {
      onSuccess: () => {
        toast({
          variant: 'default',
          title: 'Success',
          description: 'File uploaded'
        })
        handleModal()
        queryClient.invalidateQueries({ queryKey: ['ingestion-documents'] })
      },
      onError: (error) => {
        toast({
          variant: 'destructive',
          title: 'Error',
          description: `Error uploading: ${error}`
        })
      }
    })
  }
  const course = useCourse(id || '')
  return (
    <div className='w-full gap-5 flex flex-col  p-5'>
      <header className='w-full flex justify-between'>
        <p className='font-medium text-2xl'>Documents</p>
        <div className='gap-2 flex'>
          <Button>Chat</Button>
          <Button onClick={handleModal} className='w-max ml-auto'>
            <PlusIcon />
            <span>Upload Document</span>{' '}
          </Button>
        </div>
      </header>
      <div className='flex flex-col gap-6 '>
        <AnalyticSection />
        <Card>
          <CardHeader>
            <Tabs defaultValue='document' className='w-full'>
              <TabsList>
                <TabsTrigger value='document'>Document</TabsTrigger>
                <TabsTrigger value='exercise'>Exercise</TabsTrigger>
              </TabsList>
              <TabsContent value='document'>
                <DocumentTable />
              </TabsContent>
              <TabsContent value='exercise'></TabsContent>
            </Tabs>
          </CardHeader>
          <CardContent></CardContent>
        </Card>
      </div>
      <FileUploadModal isOpen={isModalOpen} onClose={handleModal} isUploading={isPending} onUpload={onSubmit} />
    </div>
  )
}

export default Course
