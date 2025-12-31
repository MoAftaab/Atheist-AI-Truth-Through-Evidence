/**
 * API client functions for backend communication.
 */

import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://atheist-ai-truth-through-evidence.onrender.com'

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests if available
apiClient.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
  }
  return config
})

// Types
export interface User {
  id: number
  email: string
  created_at: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface VerseCitation {
  surah_number: number
  surah_name_english: string
  ayah_number: number
  text_simple: string
  translation_en_yusufali: string
  score: number
  context?: Array<{
    surah_number: number
    surah_name_english: string
    ayah_number: number
    text_simple: string
    translation_en_yusufali: string
  }>
}

export interface QueryRequest {
  query: string
  k?: number
  score_threshold?: number | null
  window?: number
}

export interface QueryResponse {
  query: string
  answer: string
  citations: VerseCitation[]
  has_answer: boolean
  processing_time?: number
}

export interface QueryHistoryItem {
  id: number
  query: string
  answer: string
  citations: string | null
  created_at: string
}

// Auth API
export const authApi = {
  register: async (email: string, password: string): Promise<User> => {
    const response = await apiClient.post('/auth/register', { email, password })
    return response.data
  },

  login: async (email: string, password: string): Promise<Token> => {
    const response = await apiClient.post('/auth/login', { email, password })
    const token = response.data.access_token
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token)
    }
    return response.data
  },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token')
    }
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me')
    return response.data
  },
}

// Query API
export const queryApi = {
  query: async (request: QueryRequest): Promise<QueryResponse> => {
    const response = await apiClient.post('/queries/query', request)
    return response.data
  },

  getHistory: async (skip = 0, limit = 50): Promise<QueryHistoryItem[]> => {
    const response = await apiClient.get('/queries/history', {
      params: { skip, limit },
    })
    return response.data
  },
}



