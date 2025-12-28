'use client'

import { useState, useRef, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Header } from '@/components/Header'
import { QueryInput } from '@/components/QueryInput'
import { queryApi, QueryRequest } from '@/lib/api'
import { motion, AnimatePresence } from 'framer-motion'
import { MessageSquare, Sparkles } from 'lucide-react'

interface Message {
  id: string
  type: 'user' | 'assistant' | 'loading'
  content: string
  timestamp: Date
  citations?: any[]
}

export default function QAPage() {
  const [queryRequest, setQueryRequest] = useState<QueryRequest | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const { data, isLoading, error } = useQuery({
    queryKey: ['query', queryRequest],
    queryFn: () => queryApi.query(queryRequest!),
    enabled: !!queryRequest,
  })

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, data, isLoading])

  // Update messages when new query/response arrives
  useEffect(() => {
    if (queryRequest) {
      // Add user message
      const userMessage: Message = {
        id: Date.now().toString(),
        type: 'user',
        content: queryRequest.query,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, userMessage])
    }
  }, [queryRequest])

  useEffect(() => {
    if (data && !isLoading) {
      // Add assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        citations: data.citations,
      }
      setMessages((prev) => {
        // Remove loading message if exists
        const filtered = prev.filter((m) => m.type !== 'loading')
        return [...filtered, assistantMessage]
      })
    }
  }, [data, isLoading])

  const handleQuery = (query: string) => {
    setQueryRequest({
      query,
      k: 5,
      score_threshold: 0.5,
      window: 1,
    })
    
    // Add loading message
    const loadingMessage: Message = {
      id: `loading-${Date.now()}`,
      type: 'loading',
      content: 'Searching the Quran...',
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, loadingMessage])
  }

  return (
    <div className="flex h-screen flex-col bg-white">
      <Header />

      <main className="flex flex-1 flex-col overflow-hidden">
        {/* Chat Header */}
        <div className="border-b-2 border-black bg-white px-4 py-6">
          <div className="container mx-auto">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center border-2 border-black bg-black text-white">
                <MessageSquare className="h-6 w-6" strokeWidth={2} />
              </div>
              <div>
                <h1 className="text-2xl font-black text-black">Atheist AI Q&A</h1>
                <p className="text-sm text-gray-600">Ask questions, get citation-locked answers</p>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Messages Area */}
        <div className="flex-1 overflow-y-auto bg-gray-50">
          <div className="container mx-auto px-4 py-8">
            {messages.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex h-full flex-col items-center justify-center text-center"
              >
                <div className="mb-6 flex h-20 w-20 items-center justify-center border-2 border-black bg-black text-white">
                  <Sparkles className="h-10 w-10" strokeWidth={1.5} />
                </div>
                <h2 className="mb-4 text-3xl font-black text-black">
                  Start a Conversation
                </h2>
                <p className="max-w-md text-gray-600">
                  Ask any question about the Quran and receive answers directly from the source, with full citations.
                </p>
              </motion.div>
            ) : (
              <div className="mx-auto max-w-4xl space-y-6">
                <AnimatePresence>
                  {messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0 }}
                      className={`flex gap-4 ${
                        message.type === 'user' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      {message.type !== 'user' && (
                        <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center border-2 border-black bg-black text-white">
                          <MessageSquare className="h-5 w-5" strokeWidth={2} />
                        </div>
                      )}
                      
                      <div
                        className={`max-w-[80%] rounded-none border-2 p-6 ${
                          message.type === 'user'
                            ? 'border-black bg-black text-white'
                            : 'border-black bg-white text-black'
                        }`}
                      >
                        {message.type === 'loading' ? (
                          <div className="flex items-center gap-3">
                            <div className="h-5 w-5 animate-spin rounded-full border-2 border-black border-t-transparent"></div>
                            <span className="text-sm font-medium">Searching the Quran and generating answer...</span>
                          </div>
                        ) : (
                          <>
                            <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                            {message.citations && message.citations.length > 0 && (
                              <div className="mt-6 space-y-4 border-t-2 border-gray-200 pt-6">
                                <h4 className="text-sm font-bold uppercase tracking-wider text-gray-600">
                                  Supporting Verses ({message.citations.length})
                                </h4>
                                <div className="space-y-4">
                                  {message.citations.map((verse: any, index: number) => (
                                    <div
                                      key={`${verse.surah_number}-${verse.ayah_number}`}
                                      className="border-2 border-gray-200 bg-gray-50 p-4"
                                    >
                                      <div className="mb-3 flex items-center justify-between">
                                        <span className="text-sm font-bold text-black">
                                          {verse.surah_name_english}
                                        </span>
                                        <span className="text-xs text-gray-500">
                                          Surah {verse.surah_number}, Ayah {verse.ayah_number}
                                        </span>
                                      </div>
                                      <div className="mb-3 rounded bg-white p-4">
                                        <p className="arabic-text text-right">{verse.text_simple}</p>
                                      </div>
                                      <p className="text-sm leading-relaxed text-gray-700">
                                        {verse.translation_en_yusufali}
                                      </p>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </>
                        )}
                      </div>
                      
                      {message.type === 'user' && (
                        <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center border-2 border-black bg-white text-black">
                          <span className="text-sm font-bold">U</span>
                        </div>
                      )}
                    </motion.div>
                  ))}
                </AnimatePresence>
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="border-t-2 border-red-500 bg-red-50 px-4 py-4">
            <div className="container mx-auto">
              <p className="text-sm font-medium text-red-800">
                {(error as any)?.response?.data?.detail || 'An error occurred'}
              </p>
            </div>
          </div>
        )}

        {/* Input Area - Fixed at Bottom */}
        <div className="border-t-2 border-black bg-white px-4 py-6">
          <div className="container mx-auto max-w-4xl">
            <QueryInput onSubmit={handleQuery} isLoading={isLoading} />
          </div>
        </div>
      </main>
    </div>
  )
}
