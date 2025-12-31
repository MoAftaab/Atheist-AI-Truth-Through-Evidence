'use client'

import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import { useRouter } from 'next/navigation'
import { BookOpen, LogOut, User, History } from 'lucide-react'

export function Header() {
  const { user, logout, isAuthenticated } = useAuth()
  const router = useRouter()

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  return (
    <header className="sticky top-0 z-50 border-b-2 border-black bg-white">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="flex h-10 w-10 items-center justify-center border-2 border-black bg-black text-white transition-transform duration-200 group-hover:scale-110">
            <BookOpen className="h-6 w-6" strokeWidth={2} />
          </div>
          <span className="text-xl font-black text-black">Atheist AI</span>
        </Link>

        <nav className="flex items-center gap-4">
          <Link
            href="/qa"
            className="text-sm font-semibold text-black transition-colors hover:text-gray-600"
          >
            Ask Question
          </Link>

          {isAuthenticated ? (
            <>
              <Link
                href="/history"
                className="flex items-center gap-2 text-sm font-semibold text-black transition-colors hover:text-gray-600"
              >
                <History className="h-4 w-4" strokeWidth={2} />
                <span>History</span>
              </Link>
              <div className="flex items-center gap-3 border-l-2 border-gray-200 pl-4">
                <div className="flex items-center gap-2 text-sm font-medium text-gray-700">
                  <User className="h-4 w-4" strokeWidth={2} />
                  <span className="max-w-[150px] truncate">{user?.email}</span>
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-2 rounded-none border-2 border-black bg-white px-4 py-2 text-sm font-semibold text-black transition-all duration-200 hover:bg-black hover:text-white"
                >
                  <LogOut className="h-4 w-4" strokeWidth={2} />
                  <span>Logout</span>
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-3 border-l-2 border-gray-200 pl-4">
              <Link
                href="/login"
                className="text-sm font-semibold text-black transition-colors hover:text-gray-600"
              >
                Login
              </Link>
              <Link
                href="/register"
                className="rounded-none border-2 border-black bg-black px-6 py-2 text-sm font-semibold text-white transition-all duration-200 hover:bg-gray-900"
              >
                Sign Up
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  )
}
