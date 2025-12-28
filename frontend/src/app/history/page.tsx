'use client'

import { useQuery } from '@tanstack/react-query'
import { Header } from '@/components/Header'
import { queryApi } from '@/lib/api'
import { useAuth } from '@/lib/auth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { LoadingSpinner } from '@/components/LoadingSpinner'
import { motion } from 'framer-motion'
import { Clock, History as HistoryIcon } from 'lucide-react'

export default function HistoryPage() {
  const { isAuthenticated, loading: authLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, authLoading, router])

  const { data: history, isLoading } = useQuery({
    queryKey: ['queryHistory'],
    queryFn: () => queryApi.getHistory(),
    enabled: isAuthenticated,
  })

  if (authLoading || isLoading) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <main className="container mx-auto px-4 py-12">
          <LoadingSpinner />
        </main>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="container mx-auto px-4 py-12">
        <div className="mx-auto max-w-4xl">
          {/* Header */}
          <div className="mb-12 border-b-2 border-black pb-6">
            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 items-center justify-center border-2 border-black bg-black text-white">
                <HistoryIcon className="h-7 w-7" strokeWidth={2} />
              </div>
              <div>
                <h1 className="text-4xl font-black text-black">Query History</h1>
                <p className="mt-1 text-sm font-medium text-gray-600">
                  Your past questions and answers
                </p>
              </div>
            </div>
          </div>

          {!history || history.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="border-2 border-gray-200 bg-gray-50 p-16 text-center"
            >
              <HistoryIcon className="mx-auto mb-4 h-16 w-16 text-gray-400" strokeWidth={1.5} />
              <p className="text-lg font-medium text-gray-600">
                No queries yet. Start asking questions to see your history here.
              </p>
            </motion.div>
          ) : (
            <div className="space-y-6">
              {history.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="border-2 border-black bg-white p-8 transition-all duration-300 hover:shadow-elegant-lg"
                >
                  <div className="mb-4 flex items-center justify-between border-b-2 border-gray-200 pb-3">
                    <h3 className="text-xl font-black text-black">
                      {item.query}
                    </h3>
                    <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500">
                      <Clock className="h-4 w-4" strokeWidth={2} />
                      <span>
                        {new Date(item.created_at).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                        })}
                      </span>
                    </div>
                  </div>
                  <p className="leading-relaxed text-gray-700">
                    {item.answer}
                  </p>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
