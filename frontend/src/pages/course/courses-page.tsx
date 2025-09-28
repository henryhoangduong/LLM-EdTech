import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getCoursesQueryFn } from '@/lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { columns, DataTable } from '@/components/course-table'

const Coureses = () => {
  const limit = 20
  const [page, setPage] = useState<number>(1)
  const { data, isLoading } = useQuery({
    queryKey: ['courses', page, limit],
    queryFn: () => getCoursesQueryFn({ page, limit })
  })
  const handlePagination = (value: number) => {
    setPage(value)
  }

  return (
    <div className='w-full gap-5 flex flex-col  p-5'>
      <Card>
        <CardHeader>
          <CardTitle>
            <p>Courses</p>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {!isLoading && (
            <DataTable
              columns={columns}
              data={data?.items || []}
              page={data?.page || 1}
              pageSize={data?.page_size || 10}
              totalPages={data?.pages || 1}
              onPageChange={handlePagination}
            />
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default Coureses
