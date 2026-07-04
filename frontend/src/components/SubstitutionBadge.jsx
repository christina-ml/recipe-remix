import { useState } from 'react'
import { api } from '../api.js'

/**
 * The signature visual of the app: an ingredient shown as if a cook
 * scribbled a correction in the margin of a recipe card — the original
 * struck through, an arrow to the replacement, and a handwritten-style
 * note about what changes.
 */
export default function SubstitutionBadge({ suggestion }) {
  const [score, setScore] = useState(suggestion.score)
  const [voted, setVoted] = useState(false)

  async function vote(value) {
    if (voted) return
    try {
      const updated = await api.voteSubstitution(suggestion.id, value)
      setScore(updated.score)
      setVoted(true)
    } catch {
      // Voting is a nice-to-have; a failed vote shouldn't break the page.
    }
  }

  return (
    <div className="mt-1.5 ml-4 pl-3 border-l-2 border-spice/40 text-sm">
      <span className="text-char/40 line-through mr-1.5">{suggestion.original}</span>
      <span className="text-spice mr-1.5">→</span>
      <span className="font-medium">{suggestion.substitute}</span>
      <span className="text-char/50 ml-1.5">({suggestion.ratio})</span>
      {suggestion.note && (
        <p className="italic text-char/50 mt-0.5">{suggestion.note}</p>
      )}
      <div className="flex items-center gap-2 mt-1 text-xs text-char/50">
        <button
          onClick={() => vote(1)}
          disabled={voted}
          className="hover:text-sage disabled:opacity-40"
          aria-label="This substitution worked"
        >
          ▲
        </button>
        <span>{score}</span>
        <button
          onClick={() => vote(-1)}
          disabled={voted}
          className="hover:text-rust disabled:opacity-40"
          aria-label="This substitution didn't work"
        >
          ▼
        </button>
      </div>
    </div>
  )
}
