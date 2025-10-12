import React, { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getCoursesQueryFn } from '@/lib/api'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { columns, DataTable } from '@/components/course-table'
import { Loader2, PlusIcon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Course } from '@/types/types'
import CreateNewCourseDialog from '@/components/create-new-course-dialog'
const Coureses = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const handleModal = () => {
    setIsModalOpen(!isModalOpen)
  }
  const limit = 25
  const [page, setPage] = useState<number>(1)
  const [searchCourse, setSearchCourse] = useState<null | string>(null)
  const [courses, setCourses] = useState<null | Course[]>(null)
  const { data, isLoading } = useQuery({
    queryKey: ['courses', page, limit],
    queryFn: () => getCoursesQueryFn({ page, limit })
  })
  const handlePagination = (value: number) => {
    setPage(value)
  }
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchCourse(e.target.value)
  }
  useEffect(() => {
    if (searchCourse && data?.items) {
      const courses =
        data?.items.filter((course) => course.name.toLowerCase().includes(searchCourse.toLowerCase())) || null
      setCourses(courses)
    }
  }, [searchCourse, data?.items])
  useEffect(() => {
    if (data) {
      setCourses(data.items)
    }
  }, [data])
  return (
    <div className='w-full gap-5 flex flex-col p-5 '>
      <div className='flex flex-row w-full justify-between'>
        <h1 className='font-semibold text-3xl'>Courses 📣</h1>
        <Button onClick={handleModal} className='w-max'>
          <PlusIcon />
          <span>New Course</span>
        </Button>
      </div>

      <Card>
        <CardHeader className='flex flex-row items-center justify-between '>
          <Input className='w-[300px]' placeholder='Search Courses' onChange={handleSearch} />
        </CardHeader>
        <CardContent>
          {isLoading && <Loader2 className='animate-spin' />}
          {!isLoading && data && (
            <DataTable
              columns={columns}
              data={courses || []}
              page={data?.page || 1}
              pageSize={data?.page_size || 10}
              totalPages={data?.pages || 1}
              onPageChange={handlePagination}
            />
          )}
        </CardContent>
      </Card>
      <CreateNewCourseDialog isOpen={isModalOpen} onClose={handleModal} />
    </div>
  )
}

export default Coureses
