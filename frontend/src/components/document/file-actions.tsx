import { Button } from '@/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
// import { deleteFileMutationFn, embeddingDocumentByIdMutationFn, parseDocMutationFn } from '@/lib/api'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { EyeIcon, Loader2, SplinePointer, SquareSplitHorizontal, Trash2Icon } from 'lucide-react'
import { toast } from '@/hooks/use-toast'
import { useState } from 'react'
// import FileInformation from './file-information'
interface Props {
  doc_id: string
}
const FileActions = ({ doc_id }: Props) => {
  const [isOpen, setOpen] = useState(false)
  const [isFileInformationOpen, setIsFileInformationOpen] = useState<boolean>(false)
  const { mutate: embeddingMutate, isPending: isEmbedding } = useMutation({
    // mutationFn: embeddingDocumentByIdMutationFn
  })
  const { mutate: deleteMutate, isPending: isDeleting } = useMutation({
    // mutationFn: deleteFileMutationFn
  })
  const { mutate: parse, isPending: isParsing } = useMutation({
    // mutationFn: parseDocMutationFn
  })
  const handleEmbedding = () => {
    if (isEmbedding) return

    embeddingMutate(doc_id, {
      onSuccess: () => {
        toast({
          variant: 'default',
          title: 'Successsful',
          description: 'Document embedded'
        })
        queryClient.invalidateQueries({
          queryKey: ['ingestion-documents']
        })
      },
      onError: (error) => {
        toast({
          variant: 'destructive',
          title: 'Error',
          description: error.message
        })
      }
    })
  }
  const handleOpenCloseFileInformation = (open: boolean) => {
    setIsFileInformationOpen(open)
  }
  const queryClient = useQueryClient()
  const onDelete = () => {
    if (isDeleting) return
    deleteMutate(doc_id, {
      onSuccess: () => {
        toast({
          variant: 'default',
          description: `Document ${doc_id} deleted`
        })
        queryClient.invalidateQueries({
          queryKey: ['ingestion-documents']
        })
      },
      onError: () => {
        toast({
          variant: 'destructive',
          description: `Error deleting document ${doc_id}`
        })
      }
    })
  }
  return (
    <>
      <DropdownMenu open={isOpen} onOpenChange={setOpen}>
        <DropdownMenuTrigger asChild>
          <Button variant='outline'>Open</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className='w-56'>
          <DropdownMenuItem onClick={onDelete} disabled={isDeleting} onSelect={(e) => e.preventDefault()}>
            {isDeleting ? <Loader2 className='animate-spin' /> : <Trash2Icon />}
            Delete
          </DropdownMenuItem>
          <DropdownMenuItem onSelect={(e) => e.preventDefault()}>
            {' '}
            <SquareSplitHorizontal />
            Parse
          </DropdownMenuItem>
          <DropdownMenuItem onClick={handleEmbedding} onSelect={(e) => e.preventDefault()}>
            {isEmbedding ? <Loader2 className='animate-spin' /> : <SplinePointer />} Embedding
          </DropdownMenuItem>
          <DropdownMenuItem
            onClick={() => {
              handleOpenCloseFileInformation(true)
            }}
            onSelect={(e) => e.preventDefault()}
          >
            <EyeIcon />
            View
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      {/* <FileInformation
        open={isFileInformationOpen}
        handleChange={(open) => {
          setIsFileInformationOpen(open)
        }}
        doc_id={doc_id}
      /> */}
    </>
  )
}

export default FileActions
