import Loading from '@/components/Loading'
import useAuth from '@/hooks/api/use-auth'
import AppLayout from '@/layout/app.layout'
import SignIn from '@/pages/auth/SignIn'
import SignUp from '@/pages/auth/SignUp'
import Course from '@/pages/Course'
import NotFound from '@/pages/error/NotFound'
import Home from '@/pages/Home'
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
  COURSE: '/course/:id'
}

const protectedRoutePaths = [
  { path: PROTECTED_ROUTES.HOME, element: <Home /> },
  {
    path: PROTECTED_ROUTES.COURSE,
    element: <Course />
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
