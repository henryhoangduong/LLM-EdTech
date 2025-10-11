import Loading from '@/components/loading'
import useAuth from '@/hooks/api/use-auth'
import AppLayout from '@/layout/app.layout'
import SignIn from '@/pages/auth/sigin.page'
import SignUp from '@/pages/auth/signup.page'
import ChatPage from '@/pages/course/chat.page'
import Course from '@/pages/course/course.page'
import Coureses from '@/pages/course/courses.page'
import NotFound from '@/pages/error/NotFound'
import Home from '@/pages/home.page'
import { BrowserRouter, Navigate, Outlet, Route, Routes } from 'react-router-dom'

const AUTH_ROUTES = {
  SIGN_IN: '/sign-in',
  SIGN_UP: '/sign-up'
}
const authenticationRoutePaths = [
  { path: AUTH_ROUTES.SIGN_IN, element: <SignIn /> },
  { path: AUTH_ROUTES.SIGN_UP, element: <SignUp /> }
]

const PROTECTED_ROUTES = {
  HOME: '/',
  COURSE: '/course/:id',
  COURSES: '/courses',
  CHAT: '/course/:id/chat'
}

const protectedRoutePaths = [
  { path: PROTECTED_ROUTES.HOME, element: <Home /> },
  {
    path: PROTECTED_ROUTES.COURSE,
    element: <Course />
  },
  {
    path: PROTECTED_ROUTES.COURSES,
    element: <Coureses />
  },
  {
    path: PROTECTED_ROUTES.CHAT,
    element: <ChatPage />
  }
]

const AuthRoute = () => {
  const { data: authData } = useAuth()
  const user = authData
  if (!user) return <Outlet />
  return <Navigate to={`/`} />
}
const ProtectedRoute = () => {
  const { data: authData, isLoading } = useAuth()
  const user = authData
  if (isLoading) {
    return <Loading />
  }
  return user ? <Outlet /> : <Navigate to={'/sign-in'} replace />
}
const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AuthRoute />}>
          {authenticationRoutePaths.map((route) => (
            <Route key={route.path} path={route.path} element={route.element} />
          ))}
        </Route>
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            {protectedRoutePaths.map((route) => (
              <Route key={route.path} path={route.path} element={route.element} />
            ))}
          </Route>
        </Route>
        <Route path='*' element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes
