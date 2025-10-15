import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '../ui/form'
import { Input } from '../ui/input'
import { Button } from '../ui/button'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Loader2 } from 'lucide-react'
import { Textarea } from '../ui/textarea'
import { createCourseMutationFn } from '@/lib/api'
import { toast } from '@/hooks/use-toast'
interface CreateNewCourseDialogProps {
  isOpen: boolean
  onClose: () => void
}
const CreateNewCourseDialog = ({ isOpen, onClose }: CreateNewCourseDialogProps) => {
  const { mutate, isPending } = useMutation({
    mutationFn: createCourseMutationFn
  })
  const queryClient = useQueryClient()
  const formSchema = z.object({
    name: z.string().trim().min(1, {
      message: 'Course name is required'
    }),
    description: z.string().trim()
  })
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      description: ''
    }
  })
  const onSubmit = (values: z.infer<typeof formSchema>) => {
    if (isPending) return
    mutate(values, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['courses'] })
        onClose()
        form.reset()
      },
      onError: (error) => {
        toast({
          title: 'Error',
          description: error.message,
          variant: 'destructive'
        })
        form.reset()
      }
    })
  }
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className='sm:max-w-[600px] max-h-[80vh] flex flex-col'>
        <DialogHeader>
          <DialogTitle>Create New Course</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <div className='mb-4'>
              <FormField
                control={form.control}
                name='name'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className='dark:text-[#f1f7feb5] text-sm'>Course name</FormLabel>
                    <FormControl>
                      <Input placeholder='Business Analysis' className='!h-[48px]' {...field} />
                    </FormControl>
                    <FormDescription>This is the name of your course.</FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className='mb-4'>
              <FormField
                control={form.control}
                name='description'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className='dark:text-[#f1f7feb5] text-sm'>
                      Course description
                      <span className='text-xs font-extralight ml-2'>Optional</span>
                    </FormLabel>
                    <FormControl>
                      <Textarea rows={6} placeholder='Descritpion' {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <Button type='submit' disabled={isPending}>
              {isPending && <Loader2 className='animate-spin' />}
              <span>Create</span>
            </Button>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

export default CreateNewCourseDialog
