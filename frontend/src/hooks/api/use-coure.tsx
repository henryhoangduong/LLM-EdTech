import { useQuery } from '@tanstack/react-query'
import { getCourseByIdQueryFn } from '@/lib/api'
export const useCourse = (courseId: string) => {
  const query = useQuery({
    queryKey: ['course', courseId],
    queryFn: () => getCourseByIdQueryFn(courseId)
  })
  return query
}
