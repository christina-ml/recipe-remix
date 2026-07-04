import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api.js'

export default function RecipeList() {
  const [recipes, setRecipes] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api
      .listRecipes()
      .then(setRecipes)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-char/60">Loading recipes…</p>

  if (error) {
    return (
      <p className="text-rust">
        Couldn't reach the API ({error}). Is the backend running on port 8000?
      </p>
    )
  }

  if (recipes.length === 0) {
    return (
      <div className="text-center py-16">
        <p className="font-display text-xl mb-2">No recipes yet.</p>
        <p className="text-char/60 mb-6">
          Add the first one, or run the seed script to load a starter set.
        </p>
        <Link
          to="/new"
          className="inline-block bg-char text-crust rounded-full px-5 py-2 text-sm font-medium"
        >
          Add a recipe
        </Link>
      </div>
    )
  }

  return (
    <div className="grid sm:grid-cols-2 gap-5">
      {recipes.map((r) => (
        <Link
          key={r.id}
          to={`/recipes/${r.id}`}
          className="block bg-white/60 border border-line rounded-lg p-5 hover:border-spice transition-colors"
        >
          <h2 className="font-display text-xl mb-1">{r.title}</h2>
          <p className="text-sm text-char/60 mb-3">{r.description}</p>
          <div className="flex flex-wrap gap-1.5">
            {r.tags.map((t) => (
              <span
                key={t}
                className="text-xs uppercase tracking-wide bg-sage/10 text-sage px-2 py-0.5 rounded-full"
              >
                {t}
              </span>
            ))}
          </div>
        </Link>
      ))}
    </div>
  )
}
