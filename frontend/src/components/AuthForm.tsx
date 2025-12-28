'use client'

import { useState, FormEvent } from 'react'
import { motion } from 'framer-motion'
import { Loader2, BookOpen } from 'lucide-react'

interface AuthFormProps {
  mode: 'login' | 'register'
  onSubmit: (email: string, password: string) => Promise<void>
  isLoading?: boolean
}

export function AuthForm({ mode, onSubmit, isLoading = false }: AuthFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')

    if (!email || !password) {
      setError('Please fill in all fields')
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    try {
      await onSubmit(email, password)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred')
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-md"
    >
      <div className="border-2 border-black bg-white p-10 shadow-elegant-lg">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mb-4 flex justify-center">
            <div className="flex h-16 w-16 items-center justify-center border-2 border-black bg-black text-white">
              <BookOpen className="h-8 w-8" strokeWidth={2} />
            </div>
          </div>
          <h2 className="mb-2 text-3xl font-black text-black">
            {mode === 'login' ? 'Welcome Back' : 'Create Account'}
          </h2>
          <div className="mx-auto h-1 w-16 bg-black"></div>
          <p className="mt-4 text-sm font-medium text-gray-600">
            {mode === 'login'
              ? 'Sign in to access your query history'
              : 'Sign up to save your queries'}
          </p>
        </div>

        {error && (
          <div className="mb-6 border-2 border-red-500 bg-red-50 p-4">
            <p className="text-sm font-semibold text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="email"
              className="mb-2 block text-sm font-bold uppercase tracking-wider text-black"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
              className="w-full rounded-none border-2 border-black bg-white px-4 py-3 text-base font-medium text-black placeholder-gray-400 focus:border-black focus:outline-none focus:ring-0 disabled:bg-gray-100 disabled:opacity-50"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="mb-2 block text-sm font-bold uppercase tracking-wider text-black"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              className="w-full rounded-none border-2 border-black bg-white px-4 py-3 text-base font-medium text-black placeholder-gray-400 focus:border-black focus:outline-none focus:ring-0 disabled:bg-gray-100 disabled:opacity-50"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full rounded-none border-2 border-black bg-black px-6 py-4 text-base font-bold text-white transition-all duration-200 hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                <Loader2 className="h-5 w-5 animate-spin" strokeWidth={2.5} />
                <span>{mode === 'login' ? 'Signing in...' : 'Creating account...'}</span>
              </span>
            ) : (
              mode === 'login' ? 'Sign In' : 'Sign Up'
            )}
          </button>
        </form>
      </div>
    </motion.div>
  )
}
