'use client'
import { useEffect, useState } from 'react'
import { api } from '../api'

/** Company name configured on the server (COMPANY_NAME). Empty string when none: screens fall back to a neutral wording. */
let cached: Promise<string> | null = null
const load = () => (cached ??= api<{ company: string }>('/brand').then(b => b.company || '').catch(() => ''))

export function useCompany(): string {
  const [company, setCompany] = useState('')
  useEffect(() => { load().then(setCompany) }, [])
  return company
}
