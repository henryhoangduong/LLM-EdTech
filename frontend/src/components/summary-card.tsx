import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ReactNode } from 'react'
import { Notebook } from 'lucide-react'

const SummaryCard = ({
  bg,
  title,
  desc,
  number,
  titleColor,
  icon
}: {
  bg?: string
  title: string
  desc: string
  number: string
  titleColor?: string
  icon?: ReactNode
}) => {
  return (
    <Card
      className='max-w-[350px] w-full p-3 px-5'
      style={{
        background: bg
      }}
    >
      <CardHeader className='p-0'>
        <div className='flex flex-row justify-between'>
          <div>
            {/* <CardTitle style={{ color: titleColor }}>{title}</CardTitle> */}
            <CardDescription>{desc}</CardDescription>
          </div>
          <span className='bg-[#F7F7F7] border p-2 rounded-xl'>{icon}</span>
        </div>
      </CardHeader>
      <CardContent className='p-0'>
        <div className='flex items-center w-full justify-between'>
          <span
            className='font-medium text-[40px]'
            style={{
              color: '#241F44'
            }}
          >
            {number}
          </span>
        </div>
      </CardContent>
    </Card>
  )
}

export default SummaryCard
