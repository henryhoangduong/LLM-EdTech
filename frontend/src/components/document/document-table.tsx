import React, { useEffect, useState } from 'react'
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Card, CardHeader } from '../ui/card'
// import { embeddingDocumentByIdMutationFn, ingestionQueryFn, parseDocMutationFn } from '@/lib/api'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import FileActions from './file-actions'
import { Switch } from '../ui/switch'
import { FileText, Loader, Loader2 } from 'lucide-react'
// import ParsingStatus from './parsing-status'
import { toast } from '@/hooks/use-toast'
import { Input } from '../ui/input'
import { Document, HenryDoc } from '@/types/types'
import { ingestionQueryFn } from '@/lib/api'
import PreviewModal from './preview-modal'
interface Props {
  uploadButton?: React.ReactNode
}

const RenderItem = ({
  item,
  index,
  handleEmbedding,
  handlePreview
}: {
  item: HenryDoc
  index: number
  handleEmbedding: (id: string) => void
  handlePreview: (docuent: HenryDoc) => void
}) => {
  const date = new Date(item.metadata.uploadedAt || '')
  const day = date.getDate()
  const month = date.getMonth() + 1
  const year = date.getFullYear()

  return (
    <TableRow key={index}>
      <TableCell className='flex flex-row items-center gap-2 font-medium text-left cursor-pointer hover:underline'>
        <FileText className='w-[10px]' />
        <span
          className='w-[150px] truncate'
          onClick={() => {
            handlePreview(item)
          }}
        >
          {item.metadata.filename.charAt(0).toUpperCase() + item.metadata.filename.slice(1)}
        </span>
      </TableCell>
      <TableCell className='text-center'>{item.metadata.chunk_number}</TableCell>
      <TableCell className='text-center'>{`${day}/${month}/${year}`}</TableCell>
      <TableCell className='text-center'>
        <Switch className='cursor-not-allowed' checked={item.metadata.enabled} />
      </TableCell>
      <TableCell className='text-center'>{/* <ParsingStatus document_id={item.id} /> */}</TableCell>
      <TableCell className='text-center'>
        <FileActions doc_id={item.id} />
      </TableCell>
    </TableRow>
  )
}

const DocumentTable = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['ingestion-documents'],
    queryFn: ingestionQueryFn
  })
  const [selectedDocument, setSelectedDocument] = useState<HenryDoc | null>(null)
  const handlePreview = (document: HenryDoc) => {
    setSelectedDocument(document)
  }
  // const { mutate, isPending } = useMutation({
  //   mutationFn: embeddingDocumentByIdMutationFn
  // })

  const queryClient = useQueryClient()
  const handleEmbedding = (value: string) => {
    // if (isPending) return
    // mutate(value, {
    //   onSuccess: () => {
    //     toast({
    //       variant: 'default',
    //       title: 'Successsful',
    //       description: 'Document embedded'
    //     })
    //     queryClient.invalidateQueries({
    //       queryKey: ['ingestion-documents']
    //     })
    //   },
    //   onError: (error) => {
    //     toast({
    //       variant: 'destructive',
    //       title: 'Error',
    //       description: error.message
    //     })
    //   }
    // })
  }

  return (
    <div>
      <Table>
        <TableCaption>A list of your documents</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className='w-[100px] text-left'>Name</TableHead>
            <TableHead className='text-center'>Chunk numbers</TableHead>
            <TableHead className='text-center'>Upload Date</TableHead>
            <TableHead className='text-center'>Enable</TableHead>
            <TableHead className='text-center'>Parsing Status</TableHead>
            <TableHead className='text-center'>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading && (
            <div className='w-full flex items-center justify-center '>
              <Loader2 className='animate-spin' />
            </div>
          )}
          {data?.map((item, index) => (
            <RenderItem item={item} index={index} handleEmbedding={handleEmbedding} handlePreview={handlePreview} />
          ))}
        </TableBody>
      </Table>
      <PreviewModal
        isOpen={!!selectedDocument}
        onClose={() => setSelectedDocument(null)}
        document={selectedDocument}
        // onUpdate={(updatedDoc) => {
        //   handleDocumentUpdate(updatedDoc)
        //   setSelectedDocument(updatedDoc)
        // }}
      />
    </div>
    //  <Card className='p-4'>
    // <CardHeader className='p-4 flex flex-row items-center'>
    // <div className='w-[30%]'>
    //          <Input type='text' className='pl-10 pr-20 sm:text-sm sm:leading-5' placeholder='Search documents...' />
    // </div>
    // </CardHeader>

    // </Card>
  )
}

export default DocumentTable
