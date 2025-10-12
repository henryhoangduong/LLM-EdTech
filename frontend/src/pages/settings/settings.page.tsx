import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import useAuth from '@/hooks/api/use-auth'
import Loading from '@/components/loading'
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import z from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Button } from '@/components/ui/button'
const SettingsPage = () => {
  const user = useAuth()

  const formSchema = z.object({
    email: z.string().trim().email('Invalid email address'),
    name: z.string().min(1, { message: 'Name too short' })
  })
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: user.data?.email,
      name: user.data?.name
    }
  })
  const onSubmit = () => {}
  if (user.isLoading) {
    return <Loading />
  }
  return (
    <div className='flex flex-col p-10 items-start gap-2 '>
      <div className='flex flex-row items-center  gap-5'>
        <Avatar className='w-[100px] h-[100px]'>
          <AvatarImage src={user.data?.profile_pic || ''} alt='@shadcn' />
          <AvatarFallback className='text-2xl'>CN</AvatarFallback>
        </Avatar>
        <div className='flex flex-col gap-2'>
          <span className='text-2xl font-semibold'>Account Setting</span>
          <span className='text-muted-foreground'>Mange your account and preferences</span>
        </div>
      </div>
      <div>
        <Form {...form}>
          <form action='' className='w-[60vw] grid grid-cols-2 gap-4'>
            <div>
              <FormField
                control={form.control}
                name='email'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className='dark:text-[#f1f7feb5] text-sm'>Email</FormLabel>
                    <FormControl>
                      <Input placeholder='m@example.com' className='!h-[48px]' {...field} />
                    </FormControl>
                  </FormItem>
                )}
              />
            </div>
            <div>
              <FormField
                control={form.control}
                name='name'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className='dark:text-[#f1f7feb5] text-sm'>Name</FormLabel>
                    <FormControl>
                      <Input placeholder='David Johnson' className='!h-[48px]' {...field} />
                    </FormControl>
                  </FormItem>
                )}
              />
            </div>{' '}
          </form>{' '}
          <Button className='mt-10 right-0'>Save</Button>
        </Form>
      </div>
    </div>
  )
}

export default SettingsPage
