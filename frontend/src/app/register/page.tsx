'use client'

import { useRouter } from 'next/navigation'
import { Header } from '@/components/Header'
import { AuthForm } from '@/components/AuthForm'
import { useAuth } from '@/lib/auth'
import { useState } from 'react'

export default function RegisterPage() {
  const router = useRouter()
  const { register } = useAuth()
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      await register(email, password)
      router.push('/qa')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-gray-50 px-4 py-12">
        <AuthForm mode="register" onSubmit={handleSubmit} isLoading={isLoading} />
      </main>
    </div>
  )
}
