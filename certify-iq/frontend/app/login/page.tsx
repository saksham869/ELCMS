'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()

  const handleLogin = () => {
    if (password === 'certifyiq2026') {
      document.cookie = 'certifyiq-auth=true; path=/; max-age=86400'
      router.push('/')
    } else {
      setError('Invalid password')
    }
  }

  return (
    <div className="min-h-screen bg-[#030712] flex items-center justify-center">
      <div className="bg-[#0d1117] border border-[#21262d] rounded-2xl p-8 w-full max-w-sm">
        <h1 className="text-[#f0f6fc] text-xl font-semibold mb-1">
          certify<span className="text-[#1f6feb]">IQ</span>
        </h1>
        <p className="text-[#6e7681] text-sm mb-6">Workforce Certification Intelligence</p>

        <label className="text-[#8b949e] text-xs uppercase tracking-widest mb-2 block">
          Demo Password
        </label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleLogin()}
          placeholder="Enter password"
          className="w-full bg-[#161b22] border border-[#21262d] text-[#f0f6fc] rounded-xl px-3 py-2 text-sm focus:border-[#1f6feb] focus:outline-none mb-2"
        />
        {error && <p className="text-[#f85149] text-xs mb-2">{error}</p>}

        <button
          onClick={handleLogin}
          className="w-full bg-[#1f6feb] hover:bg-[#388bfd] text-white rounded-xl py-2 text-sm font-medium mt-2 transition-colors"
        >
          Enter →
        </button>

        <p className="text-[#6e7681] text-xs text-center mt-4">
          Demo password: <span className="text-[#8b949e] font-mono">certifyiq2026</span>
        </p>
      </div>
    </div>
  )
}