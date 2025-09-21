import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ReactNode } from 'react'

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
      className='max-w-[350px] w-full'
      style={{
        background: bg
      }}
    >
      <CardHeader>
        <CardTitle style={{ color: titleColor }}>{title}</CardTitle>
        <CardDescription>{desc}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className='flex items-center w-full justify-between'>
          <span
            className='font-bold text-[40px]'
            style={{
              color: '#241F44'
            }}
          >
            {number}
          </span>
          {icon}
        </div>
      </CardContent>
      {/* <CardFooter>
        <p>Card Footer</p>
      </CardFooter> */}
    </Card>
  )
}

export default SummaryCard
