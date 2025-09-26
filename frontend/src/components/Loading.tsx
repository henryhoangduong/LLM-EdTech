import { AudioWaveform } from 'lucide-react'
const Loading = () => {
  return (
    <div className='h-screen w-screen flex flex-col justify-center items-center '>
      <AudioWaveform className='animate-pulse duration-700 relative' size={80} />
    </div>
  )
}

export default Loading
