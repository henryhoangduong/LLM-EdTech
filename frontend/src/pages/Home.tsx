import { DataTable, Course } from '@/components/ClassTable'
import { columns } from '../components/ClassTable'
import SummaryCard from '@/components/SummaryCard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthContext } from '@/context/auth-provider'
import { Button } from '@/components/ui/button'
import { PlusIcon } from 'lucide-react'
import { useState } from 'react'
import CreateNewCourseDialog from '@/components/CreateNewCourseDialog'
import { useQuery } from '@tanstack/react-query'
import { getCoursesQueryFn } from '@/lib/api'

const Home = () => {
  const { user } = useAuthContext()
  const { data, isLoading } = useQuery({
    queryKey: ['course'],
    queryFn: getCoursesQueryFn
  })

  const [isNewCourseFormOpen, setIsNewCourseFormOpen] = useState(false)
  const handleModal = () => {
    setIsNewCourseFormOpen(!isNewCourseFormOpen)
  }
  return (
    <div className='w-full gap-5 flex flex-col  p-5'>
      <header className='p-4 w-full flex justify-between'>
        <p className='font-medium text-2xl'>👋 Welcome back {user?.name as string}!</p>
        <Button onClick={handleModal}>
          <PlusIcon />
          <span>New Course</span>
        </Button>
      </header>
      <Card className='w-full justify-between'>
        <CardHeader>
          <CardTitle>Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className='flex w-full justify-between'>
            <SummaryCard bg='#DDFCE6' titleColor='#3DDE4F' title='Lessons' desc='Lessons' number={'20'} />
            <SummaryCard bg='#FEE3E4' titleColor={'#F65A7F'} title='Assignments' desc='Assignments' number={'20'} />
            <SummaryCard bg='#FEF3DE' titleColor={'#FE9473'} title='Exercises' desc='Exercise' number={'20'} />
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>
            <p>Courses</p>
          </CardTitle>
        </CardHeader>
        <CardContent>{!isLoading && <DataTable columns={columns} data={data} />}</CardContent>
      </Card>
      <CreateNewCourseDialog isOpen={isNewCourseFormOpen} onClose={handleModal} />
    </div>
  )
}

export default Home
