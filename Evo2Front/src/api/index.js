import axios from 'axios'

const baseURL = 'https://cau-evo2-api.shennong.cc/'

const api = axios.create({
  baseURL: baseURL,
  timeout: 30000,
})

export default api
export { baseURL }