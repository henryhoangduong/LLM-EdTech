import { useState } from 'react'
import { Link } from 'react-router-dom'
import { EllipsisIcon, Loader, LogOut, SettingsIcon } from 'lucide-react'
import {
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarGroupContent,
  SidebarGroup,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
  SidebarRail,
  useSidebar
} from '@/components/ui/sidebar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import Logo from '../logo/logo'
import { AvatarImage } from '@radix-ui/react-avatar'
import { LayoutDashboard } from 'lucide-react'
import LogoutDialog from './logout-dialog'
import { useAuthContext } from '@/context/auth-provider'
const Asidebar = () => {
  const { open } = useSidebar()
  const { user, isLoading } = useAuthContext()
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Sidebar collapsible='icon'>
        <SidebarHeader className='!py-0 dark:bg-background'>
          <div className='flex h-[48px] items-center justify-start w-full px-1 border-b'>
            <Logo />
            {open && (
              <Link to='' className='hidden md:flex ml-2 items-center gap-2 self-center font-medium'>
                BDA
              </Link>
            )}
          </div>
        </SidebarHeader>
        <SidebarContent className='!mt-0 dark:bg-background'>
          <SidebarGroup className='!py-0'>
            <SidebarGroupContent>
              <SidebarMenu className='mt-5'>
                <SidebarMenuItem>
                  <SidebarMenuButton>
                    <LayoutDashboard />
                    <Link to='/'>Dashboard</Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
                <SidebarMenuItem>
                  <SidebarMenuButton>
                    <SettingsIcon />
                    <Link to={'/settings'}>Settings</Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
        <SidebarFooter className='dark:bg-background'>
          <SidebarMenu>
            <SidebarMenuItem>
              {isLoading ? (
                <Loader size='24px' className='place-self-center self-center animate-spin' />
              ) : (
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <SidebarMenuButton
                      size='lg'
                      className='data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground'
                    >
                      <Avatar className='h-8 w-8 rounded-full'>
                        <AvatarImage src={user?.profile_pic || ''} />
                        <AvatarFallback className='rounded-full border border-gray-500'>
                          {user?.name && user?.name && user?.name.split(' ')[0].charAt(0)}
                          {user?.name && user?.name.split(' ')[1].charAt(0)}
                          {!user?.name && 'N'}
                        </AvatarFallback>
                      </Avatar>
                      <div className='grid flex-1 text-left text-sm leading-tight'>
                        <span className='truncate font-semibold'>{user?.name || 'User Name'} </span>
                        <span className='truncate text-xs'>{user?.email}</span>
                      </div>
                      <EllipsisIcon className='ml-auto size-4' />
                    </SidebarMenuButton>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent
                    className='w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg'
                    side={'bottom'}
                    align='start'
                    sideOffset={4}
                  >
                    <DropdownMenuGroup></DropdownMenuGroup>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={() => setIsOpen(true)}>
                      <LogOut />
                      Log out
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              )}
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarFooter>
        <SidebarRail />
      </Sidebar>
      <LogoutDialog isOpen={isOpen} setIsOpen={setIsOpen} />
    </>
  )
}

export default Asidebar
