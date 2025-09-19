import AppLayout from '@/layout/app.layout'
import SignIn from '@/pages/auth/SignIn'
import SignUp from '@/pages/auth/SignUp'
import NotFound from '@/pages/error/NotFound'
import Home from '@/pages/Home'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

const AUTH_ROUTES = {
  SIGN_IN: '/sign-in',
  SIGN_UP: '/sign-up'
}
const authenticationRoutePaths = [
  { path: AUTH_ROUTES.SIGN_IN, element: <SignIn /> },
  { path: AUTH_ROUTES.SIGN_UP, element: <SignUp /> }
]
const PROTECTED_ROUTES = {
  HOME: '/'
}

const protectedRoutePaths = [{ path: PROTECTED_ROUTES.HOME, element: <Home /> }]

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        {authenticationRoutePaths.map((route) => (
          <Route key={route.path} path={route.path} element={route.element} />
        ))}
        <Route element={<AppLayout />}>
          {protectedRoutePaths.map((route) => (
            <Route key={route.path} path={route.path} element={route.element} />
          ))}
        </Route>
        <Route path='*' element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes
