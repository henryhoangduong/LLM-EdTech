import React, { useEffect, useState } from 'react'
import ChatFrame from '@/components/chat-frame'
import { MoreVertical, RotateCw, MessageSquare } from 'lucide-react'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator
} from '@/components/ui/dropdown-menu'
import { Message } from '@/types/types'
import { FileUploadModal } from '@/components/document/file-upload-document'
import { useToast } from '@/hooks/use-toast'
import { Toaster } from '@/components/ui/toaster'
import { motion } from 'framer-motion'

const STORAGE_KEY = 'chat_messages'

const ChatPage = () => {
  const [messages, setMessages] = useState<Message[]>(() => {
    const savedMessages = localStorage.getItem(STORAGE_KEY)
    return savedMessages ? JSON.parse(savedMessages) : []
  })

  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false)

  const handleClearMessages = () => {
    setMessages([])
    localStorage.removeItem(STORAGE_KEY)
  }

  const handleEndDiscussion = () => {
    handleClearMessages()
    window.parent.postMessage({ type: 'CLOSE_CHAT' }, '*')
  }

  const handleChatUpload = async (files: FileList) => {}

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className='p-4 md:p-6 h-full flex flex-col'
    >
      <motion.div
        className='bg-white shadow-xl flex flex-col h-full rounded-xl overflow-hidden border border-gray-100'
        initial={{ y: 20 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5, type: 'spring', stiffness: 100 }}
      >
        <div className='text-black py-3 px-4 flex items-center justify-between shrink-0 rounded-t-xl'>
          <div className='flex items-center gap-2'>
            <MessageSquare className='h-5 w-5' />
            <h1 className='text-xl text-black font-semibold'>BDA</h1>
            {messages.length > 0 && (
              <div className='ml-2 bg-white/20 text-white text-xs rounded-full px-2 py-0.5'>
                {messages.length} message{messages.length !== 1 ? 's' : ''}
              </div>
            )}
          </div>
          <div className='flex items-center gap-2'>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => {
                handleClearMessages()
                window.location.reload()
              }}
              className='hover:bg-white/20 p-2 rounded-full transition-colors duration-200'
            >
              <RotateCw className='h-5 w-5' />
            </motion.button>

            <DropdownMenu>
              <DropdownMenuTrigger className='hover:bg-white/20 p-2 rounded-full transition-colors duration-200'>
                <MoreVertical className='h-5 w-5' />
              </DropdownMenuTrigger>
              <DropdownMenuContent align='end' className='w-48'>
                <DropdownMenuItem onClick={handleClearMessages} className='cursor-pointer text-black'>
                  Clear Messages
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleEndDiscussion} className='cursor-pointer text-red-500'>
                  End Discussion
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
        <div className='flex-1 overflow-hidden relative'>
          <ChatFrame messages={messages} setMessages={setMessages} onUploadClick={() => setIsUploadModalOpen(true)} />
        </div>
        <FileUploadModal
          isOpen={isUploadModalOpen}
          onClose={() => setIsUploadModalOpen(false)}
          onUpload={handleChatUpload}
        />
      </motion.div>
    </motion.div>
  )
}

export default ChatPage
