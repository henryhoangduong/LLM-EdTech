import { DataTable } from '@/components/course-table'
import { columns } from '../components/course-table'
import SummaryCard from '@/components/summary-card'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthContext } from '@/context/auth-provider'
import { Button } from '@/components/ui/button'
import { Loader2, PlusIcon } from 'lucide-react'
import { useState } from 'react'
import CreateNewCourseDialog from '@/components/create-new-course-dialog'
import { useQuery } from '@tanstack/react-query'
import { getCoursesQueryFn } from '@/lib/api'
import { Notebook, Scroll, Landmark } from 'lucide-react'

const Home = () => {
  const { user } = useAuthContext()
  const [page, setPage] = useState(1)
  const limit = 5
  const { data, isLoading } = useQuery({
    queryKey: ['courses', page, limit],
    queryFn: () => getCoursesQueryFn({ page, limit })
  })

  const [isNewCourseFormOpen, setIsNewCourseFormOpen] = useState(false)

  const handleModal = () => {
    setIsNewCourseFormOpen(!isNewCourseFormOpen)
  }
  const handlePagination = (value: number) => {
    setPage(value)
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
            <SummaryCard title='Lessons' desc='Lessons' number={'20'} icon={<Notebook size={16} />} />
            <SummaryCard title='Assignments' desc='Assignments' number={'20'} icon={<Scroll size={16} />} />
            <SummaryCard title='Exercises' desc='Exercise' number={'20'} icon={<Landmark size={16} />} />
          </div>
        </CardContent>
      </Card>
      <div className='w-full flex gap-5'>
        <div className='w-2/3'>
          <Card>
            <CardHeader>
              <CardTitle>
                <p>Courses</p>
              </CardTitle>
            </CardHeader>
            <CardContent className='flex flex-col justify-center items-center'>
              {isLoading && <Loader2 className='animate-spin' />}

              {!isLoading && data && (
                <div className='w-full'>
                  <DataTable
                    columns={columns}
                    data={data?.items || []}
                    page={data?.page || 1}
                    pageSize={data?.page_size || 10}
                    totalPages={data?.pages || 1}
                    onPageChange={handlePagination}
                  />
                </div>
              )}
            </CardContent>
          </Card>
        </div>
        <div className='flex-1'>
          <Card>
            <CardHeader>
              <CardTitle>
                <p>Recent Classes</p>
              </CardTitle>
              <CardDescription>Recent classes that you have joined</CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>

      <CreateNewCourseDialog isOpen={isNewCourseFormOpen} onClose={handleModal} />
    </div>
  )
}

export default Home
