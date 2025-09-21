import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL
const options = {
  baseURL,
  withCredentials: true,
  timeout: 10000
}
const API = axios.create(options)
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)
API.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const { data, status } = error.response
    if (data === 'Unauthorized' && status === 401) {
      window.location.href = '/'
    }
    const customError = {
      ...error,
      errorCode: data?.errorCode || 'UNKNOWN_ERROR'
    }
    return Promise.reject(customError)
  }
)

export default API
