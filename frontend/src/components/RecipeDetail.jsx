import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api.js'
import SubstitutionBadge from './SubstitutionBadge.jsx'

const DIETS = [
  { key: 'vegan', label: 'Vegan' },
  { key: 'vegetarian', label: 'Vegetarian' },
  { key: 'dairy_free', label: 'Dairy-free' },
  { key: 'gluten_free', label: 'Gluten-free' },
  { key: 'nut_free', label: 'Nut-free' },
]

export default function RecipeDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [recipe, setRecipe] = useState(null)
  const [diet, setDiet] = useState(null)
  const [remix, setRemix] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.getRecipe(id).then(setRecipe).catch((e) => setError(e.message))
  }, [id])

  async function applyDiet(dietKey) {
    setDiet(dietKey)
    if (!dietKey) {
      setRemix(null)
      return
    }
    const result = await api.remixRecipe(id, dietKey)
    setRemix(result)
  }

  async function handleDelete() {
    if (!confirm('Delete this recipe?')) return
    await api.deleteRecipe(id)
    navigate('/')
  }

  if (error) return <p className="text-rust">{error}</p>
  if (!recipe) return <p className="text-char/60">Loading…</p>

  const flaggedByName = {}
  if (remix) {
    for (const ing of remix.ingredients) {
      flaggedByName[ing.original] = ing
    }
  }

  return (
    <div>
      <div className="flex items-start justify-between">
        <div>
          <h2 className="font-display text-3xl mb-1">{recipe.title}</h2>
          <p className="text-char/60 mb-4">{recipe.description}</p>
        </div>
        <button
          onClick={handleDelete}
          className="text-xs text-char/40 hover:text-rust"
        >
          Delete
        </button>
      </div>

      <div className="mb-6">
        <p className="text-xs uppercase tracking-wide text-char/50 mb-2">
          Remix this recipe for…
        </p>
        <div className="flex flex-wrap gap-2">
          {DIETS.map((d) => (
            <button
              key={d.key}
              onClick={() => applyDiet(diet === d.key ? null : d.key)}
              className={`text-sm rounded-full px-3 py-1.5 border transition-colors ${
                diet === d.key
                  ? 'bg-spice text-white border-spice'
                  : 'border-line hover:border-spice'
              }`}
            >
              {d.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-8">
        <section>
          <h3 className="font-display text-lg mb-2 rule pt-3">Ingredients</h3>
          <ul className="space-y-2.5">
            {recipe.ingredients.map((ing, i) => {
              const flag = flaggedByName[ing.name]
              return (
                <li key={i}>
                  <div className="text-sm">
                    <span className="text-char/50 mr-1.5">{ing.quantity}</span>
                    <span
                      className={flag?.flagged ? 'line-through text-char/40' : ''}
                    >
                      {ing.name}
                    </span>
                  </div>
                  {flag?.flagged && !flag.suggestion && (
                    <p className="text-xs text-char/40 ml-4 mt-0.5 italic">
                      no known substitution yet — open an issue!
                    </p>
                  )}
                  {flag?.suggestion && (
                    <SubstitutionBadge suggestion={flag.suggestion} />
                  )}
                </li>
              )
            })}
          </ul>
        </section>

        <section>
          <h3 className="font-display text-lg mb-2 rule pt-3">Steps</h3>
          <ol className="space-y-2.5 text-sm list-decimal list-inside">
            {recipe.steps.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ol>
        </section>
      </div>
    </div>
  )
}
