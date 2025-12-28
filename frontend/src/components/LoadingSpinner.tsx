'use client'

import { motion } from 'framer-motion'

export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center p-12">
      <div className="text-center">
        <motion.div
          className="mx-auto mb-4 h-12 w-12 border-4 border-gray-200 border-t-black"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        />
        <p className="text-sm font-semibold text-gray-600">Loading...</p>
      </div>
    </div>
  )
}
