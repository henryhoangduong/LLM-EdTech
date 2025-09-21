import { DataTable, ClassRoom } from '@/components/ClassTable'
import { columns } from '../components/ClassTable'
import SummaryCard from '@/components/SummaryCard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthContext } from '@/context/auth-provider'
function getData(): ClassRoom[] {
  return [
    {
      id: '728ed52f',
      name: 'Business Data Analysis',
      date: 'pending'
    },
    {
      id: '728ed52f',
      name: 'Data Structure And Algorithm',
      date: 'pending'
    }
  ]
}
const Home = () => {
  const data = getData()
  const { user } = useAuthContext()

  return (
    <div className='w-full gap-5 flex flex-col  p-5'>
      <header className='p-4 w-full'>
        <p className='font-medium text-2xl'>👋 Welcome back {user?.name as string}!</p>
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
        <CardContent>
          <DataTable columns={columns} data={data} />
        </CardContent>
      </Card>
    </div>
  )
}

export default Home
