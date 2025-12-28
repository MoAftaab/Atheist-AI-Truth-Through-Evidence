'use client'

import { useState, FormEvent } from 'react'
import { Send, Loader2 } from 'lucide-react'

interface QueryInputProps {
  onSubmit: (query: string) => void
  isLoading?: boolean
  disabled?: boolean
}

export function QueryInput({ onSubmit, isLoading = false, disabled = false }: QueryInputProps) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (query.trim() && !isLoading && !disabled) {
      onSubmit(query.trim())
      setQuery('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative flex items-center gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the Quran..."
          disabled={isLoading || disabled}
          className="flex-1 rounded-none border-2 border-black bg-white px-6 py-4 text-base font-medium text-black placeholder-gray-400 focus:border-black focus:outline-none focus:ring-0 disabled:bg-gray-100 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!query.trim() || isLoading || disabled}
          className="flex h-[56px] w-[56px] items-center justify-center border-2 border-black bg-black text-white transition-all duration-200 hover:bg-gray-900 disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:bg-black"
        >
          {isLoading ? (
            <Loader2 className="h-5 w-5 animate-spin" strokeWidth={2.5} />
          ) : (
            <Send className="h-5 w-5" strokeWidth={2.5} />
          )}
        </button>
      </div>
    </form>
  )
}
