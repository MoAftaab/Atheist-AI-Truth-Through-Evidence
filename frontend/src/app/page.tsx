'use client'

import Link from 'next/link'
import { Header } from '@/components/Header'
import { motion } from 'framer-motion'
import { BookOpen, Shield, Zap, Search, Sparkles } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <Header />

      <main>
        {/* Hero Section with Calligraphy-inspired Design */}
        <section className="relative overflow-hidden bg-white py-24">
          {/* Decorative Pattern */}
          <div className="absolute inset-0 opacity-[0.02] pattern-dots pattern-size"></div>
          
          <div className="container relative mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="mx-auto max-w-5xl text-center"
            >
              {/* Decorative Element */}
              <div className="mb-8 flex justify-center">
                <div className="relative">
                  <BookOpen className="h-16 w-16 text-black" strokeWidth={1.5} />
                  <div className="absolute -top-2 -right-2 h-4 w-4 rounded-full bg-black"></div>
                </div>
              </div>

              <h1 className="mb-6 text-6xl font-black tracking-tight text-black md:text-7xl">
                Ask Questions About
                <br />
                <span className="relative inline-block">
                  <span className="gradient-text">the Quran</span>
                  <span className="calligraphy-line"></span>
                </span>
              </h1>
              
              <p className="mb-12 text-xl font-light leading-relaxed text-gray-700 md:text-2xl">
                Get accurate, citation-locked answers directly from the Quran.
                <br className="hidden md:block" />
                <span className="text-gray-500">No interpretations. No external commentary. Just the source.</span>
              </p>
              
              <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Link
                  href="/qa"
                  className="group relative overflow-hidden rounded-none bg-black px-10 py-4 text-lg font-semibold text-white transition-all duration-300 hover:bg-gray-900 hover:shadow-elegant-lg"
                >
                  <span className="relative z-10">Ask a Question</span>
                </Link>
                <Link
                  href="/register"
                  className="group relative overflow-hidden rounded-none border-2 border-black bg-white px-10 py-4 text-lg font-semibold text-black transition-all duration-300 hover:border-black hover:shadow-elegant-lg"
                >
                  <span className="relative z-10 group-hover:text-white">Sign Up Free</span>
                  <div className="absolute inset-0 -translate-x-full bg-black transition-transform duration-300 group-hover:translate-x-0"></div>
                </Link>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Features Section - Minimalist Black & White */}
        <section className="bg-gray-50 py-24">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="mx-auto max-w-6xl"
            >
              <div className="mb-16 text-center">
            <h2 className="mb-4 text-4xl font-black text-black">
              Why Atheist AI?
            </h2>
                <div className="mx-auto h-1 w-24 bg-black"></div>
              </div>
              
              <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
                {[
                  {
                    icon: Shield,
                    title: 'Citation-Locked',
                    description: 'Every answer is directly supported by Quranic verses. No hallucinations, no invented explanations.',
                  },
                  {
                    icon: Zap,
                    title: 'Fast & Accurate',
                    description: 'Semantic search powered by FAISS finds relevant verses in milliseconds.',
                  },
                  {
                    icon: Search,
                    title: 'Semantic Search',
                    description: 'Ask questions in natural language. Our AI understands context and meaning.',
                  },
                  {
                    icon: BookOpen,
                    title: 'Source Only',
                    description: 'Answers come exclusively from the Quran itself—no external commentary or interpretation.',
                  },
                ].map((feature, index) => (
                  <motion.div
                    key={feature.title}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                    className="group relative border-2 border-black bg-white p-8 transition-all duration-300 hover:shadow-elegant-lg"
                  >
                    <div className="mb-6 flex h-14 w-14 items-center justify-center border-2 border-black bg-black text-white transition-transform duration-300 group-hover:scale-110">
                      <feature.icon className="h-7 w-7" strokeWidth={2} />
                    </div>
                    <h3 className="mb-3 text-xl font-bold text-black">
                      {feature.title}
                    </h3>
                    <p className="text-sm leading-relaxed text-gray-600">
                      {feature.description}
                    </p>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </section>

        {/* How It Works - Clean Steps */}
        <section className="bg-white py-24">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="mx-auto max-w-4xl"
            >
              <div className="mb-16 text-center">
                <h2 className="mb-4 text-4xl font-black text-black">
                  How It Works
                </h2>
                <div className="mx-auto h-1 w-24 bg-black"></div>
              </div>
              
              <div className="space-y-12">
                {[
                  {
                    step: '01',
                    title: 'Ask Your Question',
                    description: 'Type your question in natural language. Our system understands context and meaning.',
                  },
                  {
                    step: '02',
                    title: 'Semantic Search',
                    description: 'FAISS-powered search finds the most relevant Quranic verses using advanced embeddings.',
                  },
                  {
                    step: '03',
                    title: 'Citation-Locked Answer',
                    description: 'Get an answer generated exclusively from the retrieved verses, with full citations.',
                  },
                ].map((item, index) => (
                  <motion.div
                    key={item.step}
                    initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.2 }}
                    className="flex items-start gap-8 border-b-2 border-gray-200 pb-12 last:border-0"
                  >
                    <div className="flex-shrink-0">
                      <div className="flex h-20 w-20 items-center justify-center border-2 border-black bg-black text-2xl font-black text-white">
                        {item.step}
                      </div>
                    </div>
                    <div className="flex-1">
                      <h3 className="mb-3 text-2xl font-bold text-black">
                        {item.title}
                      </h3>
                      <p className="text-gray-600 leading-relaxed">
                        {item.description}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </section>

        {/* CTA Section - Bold Black */}
        <section className="bg-black py-24 text-white">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="mx-auto max-w-3xl text-center"
            >
              <Sparkles className="mx-auto mb-6 h-12 w-12 text-white" strokeWidth={1.5} />
              <h2 className="mb-6 text-5xl font-black">
                Ready to Explore the Quran?
              </h2>
              <p className="mb-10 text-xl font-light text-gray-300">
                Start asking questions and get citation-locked answers today.
              </p>
              <Link
                href="/qa"
                className="inline-block rounded-none border-2 border-white bg-white px-12 py-4 text-lg font-bold text-black transition-all duration-300 hover:bg-transparent hover:text-white"
              >
                Get Started
              </Link>
            </motion.div>
          </div>
        </section>
      </main>

      <footer className="border-t-2 border-black bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-4xl">
            {/* Main Footer Content */}
            <div className="mb-8 grid gap-8 md:grid-cols-2">
              <div>
                <div className="mb-4 flex items-center gap-3">
                  <div className="flex h-12 w-12 items-center justify-center border-2 border-black bg-black text-white">
                    <BookOpen className="h-6 w-6" strokeWidth={2} />
                  </div>
                  <span className="text-2xl font-black text-black">Atheist AI</span>
                </div>
                <p className="text-sm font-medium text-gray-600 leading-relaxed">
                  Citation-locked Question Answering system that answers user questions only using the Quran itself, without hallucination or external commentary.
                </p>
              </div>
              
              <div>
                <h3 className="mb-4 text-sm font-black uppercase tracking-wider text-black">
                  Connect
                </h3>
                <div className="space-y-3">
                  <a
                    href="https://www.linkedin.com/in/mohammad-aftaab-b49a5624a/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="group flex items-center gap-3 text-sm font-semibold text-black transition-colors hover:text-gray-600"
                  >
                    <div className="flex h-8 w-8 items-center justify-center border-2 border-black bg-white transition-all duration-200 group-hover:bg-black group-hover:text-white">
                      <span className="text-xs font-black">in</span>
                    </div>
                    <span>LinkedIn</span>
                  </a>
                  <a
                    href="https://github.com/MoAftaab"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="group flex items-center gap-3 text-sm font-semibold text-black transition-colors hover:text-gray-600"
                  >
                    <div className="flex h-8 w-8 items-center justify-center border-2 border-black bg-white transition-all duration-200 group-hover:bg-black group-hover:text-white">
                      <span className="text-xs font-black">GH</span>
                    </div>
                    <span>GitHub</span>
                  </a>
                </div>
              </div>
            </div>
            
            {/* Divider */}
            <div className="my-8 h-px bg-gray-200"></div>
            
            {/* Copyright */}
            <div className="flex flex-col items-center justify-between gap-4 text-center md:flex-row">
              <p className="text-xs font-medium text-gray-600">
                © 2024 Atheist AI. Built with truth preservation in mind.
              </p>
              <p className="text-xs font-medium text-gray-600">
                Developed by{' '}
                <a
                  href="https://github.com/MoAftaab"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-bold text-black underline-offset-2 hover:underline"
                >
                  Mohammad Aftaab
                </a>
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
