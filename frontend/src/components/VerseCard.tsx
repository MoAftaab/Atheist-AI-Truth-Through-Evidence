'use client'

import { motion } from 'framer-motion'
import { VerseCitation } from '@/lib/api'
import { BookOpen } from 'lucide-react'

interface VerseCardProps {
  verse: VerseCitation
  index: number
}

export function VerseCard({ verse, index }: VerseCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="border-2 border-black bg-white p-6 transition-all duration-300 hover:shadow-elegant-lg"
    >
      <div className="mb-4 flex items-center justify-between border-b-2 border-gray-200 pb-3">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center border-2 border-black bg-black text-white">
            <BookOpen className="h-5 w-5" strokeWidth={2} />
          </div>
          <h3 className="text-lg font-black text-black">
            {verse.surah_name_english}
          </h3>
        </div>
        <div className="text-xs font-bold uppercase tracking-wider text-gray-500">
          {verse.surah_number}:{verse.ayah_number}
        </div>
      </div>

      <div className="mb-4 border-2 border-gray-200 bg-gray-50 p-5">
        <p className="arabic-text text-right text-black">
          {verse.text_simple}
        </p>
      </div>

      <div className="border-t-2 border-gray-200 pt-4">
        <p className="mb-3 leading-relaxed text-gray-700">
          {verse.translation_en_yusufali}
        </p>
        {verse.score && (
          <div className="text-xs font-semibold uppercase tracking-wider text-gray-500">
            Relevance: {Math.round(verse.score * 100)}%
          </div>
        )}
      </div>
    </motion.div>
  )
}
