'use client'

import { motion } from 'framer-motion'
import { QueryResponse } from '@/lib/api'
import { VerseCard } from './VerseCard'
import { CheckCircle, XCircle } from 'lucide-react'

interface AnswerDisplayProps {
  response: QueryResponse | null
  isLoading?: boolean
}

export function AnswerDisplay({ response, isLoading }: AnswerDisplayProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="text-center">
          <motion.div
            className="mx-auto mb-4 h-12 w-12 border-4 border-gray-200 border-t-black"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          />
          <p className="text-sm font-semibold text-gray-600">
            Searching the Quran and generating answer...
          </p>
        </div>
      </div>
    )
  }

  if (!response) {
    return null
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Answer Section */}
      <div className="border-2 border-black bg-white p-8">
        <div className="mb-6 flex items-center gap-3 border-b-2 border-gray-200 pb-4">
          {response.has_answer ? (
            <div className="flex h-10 w-10 items-center justify-center border-2 border-black bg-black text-white">
              <CheckCircle className="h-5 w-5" strokeWidth={2.5} />
            </div>
          ) : (
            <div className="flex h-10 w-10 items-center justify-center border-2 border-gray-400 bg-gray-100 text-gray-400">
              <XCircle className="h-5 w-5" strokeWidth={2.5} />
            </div>
          )}
          <h2 className="text-2xl font-black text-black">Answer</h2>
        </div>
        <p className="whitespace-pre-wrap leading-relaxed text-gray-700">
          {response.answer}
        </p>
        {response.processing_time && (
          <div className="mt-6 border-t-2 border-gray-200 pt-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
              Generated in {response.processing_time.toFixed(2)}s
            </p>
          </div>
        )}
      </div>

      {/* Citations Section */}
      {response.citations && response.citations.length > 0 && (
        <div>
          <div className="mb-6 flex items-center gap-3">
            <div className="h-1 w-12 bg-black"></div>
            <h3 className="text-xl font-black uppercase tracking-wider text-black">
              Supporting Verses ({response.citations.length})
            </h3>
          </div>
          <div className="grid gap-6 md:grid-cols-2">
            {response.citations.map((verse, index) => (
              <VerseCard key={`${verse.surah_number}-${verse.ayah_number}`} verse={verse} index={index} />
            ))}
          </div>
        </div>
      )}
    </motion.div>
  )
}
