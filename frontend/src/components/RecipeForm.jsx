import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api.js'

export default function RecipeForm() {
  const navigate = useNavigate()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [tags, setTags] = useState('')
  const [ingredients, setIngredients] = useState([{ name: '', quantity: '' }])
  const [steps, setSteps] = useState([''])
  const [error, setError] = useState(null)

  function updateIngredient(i, field, value) {
    const next = [...ingredients]
    next[i][field] = value
    setIngredients(next)
  }

  function updateStep(i, value) {
    const next = [...steps]
    next[i] = value
    setSteps(next)
  }

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      const recipe = await api.createRecipe({
        title,
        description,
        tags: tags.split(',').map((t) => t.trim()).filter(Boolean),
        ingredients: ingredients.filter((i) => i.name.trim()),
        steps: steps.filter((s) => s.trim()),
      })
      navigate(`/recipes/${recipe.id}`)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-xl">
      <h2 className="font-display text-2xl mb-6">Add a recipe</h2>

      {error && <p className="text-rust mb-4 text-sm">{error}</p>}

      <label className="block mb-4">
        <span className="text-xs uppercase tracking-wide text-char/50">Title</span>
        <input
          required
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full mt-1 border border-line rounded-md px-3 py-2 bg-white/60"
        />
      </label>

      <label className="block mb-4">
        <span className="text-xs uppercase tracking-wide text-char/50">Description</span>
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full mt-1 border border-line rounded-md px-3 py-2 bg-white/60"
        />
      </label>

      <label className="block mb-4">
        <span className="text-xs uppercase tracking-wide text-char/50">
          Tags (comma-separated)
        </span>
        <input
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          placeholder="dessert, quick"
          className="w-full mt-1 border border-line rounded-md px-3 py-2 bg-white/60"
        />
      </label>

      <div className="mb-4">
        <span className="text-xs uppercase tracking-wide text-char/50">Ingredients</span>
        {ingredients.map((ing, i) => (
          <div key={i} className="flex gap-2 mt-2">
            <input
              placeholder="quantity"
              value={ing.quantity}
              onChange={(e) => updateIngredient(i, 'quantity', e.target.value)}
              className="w-24 border border-line rounded-md px-2 py-1.5 bg-white/60 text-sm"
            />
            <input
              placeholder="ingredient name"
              value={ing.name}
              onChange={(e) => updateIngredient(i, 'name', e.target.value)}
              className="flex-1 border border-line rounded-md px-2 py-1.5 bg-white/60 text-sm"
            />
          </div>
        ))}
        <button
          type="button"
          onClick={() => setIngredients([...ingredients, { name: '', quantity: '' }])}
          className="text-sm text-spice mt-2"
        >
          + add ingredient
        </button>
      </div>

      <div className="mb-6">
        <span className="text-xs uppercase tracking-wide text-char/50">Steps</span>
        {steps.map((s, i) => (
          <div key={i} className="mt-2">
            <input
              placeholder={`Step ${i + 1}`}
              value={s}
              onChange={(e) => updateStep(i, e.target.value)}
              className="w-full border border-line rounded-md px-2 py-1.5 bg-white/60 text-sm"
            />
          </div>
        ))}
        <button
          type="button"
          onClick={() => setSteps([...steps, ''])}
          className="text-sm text-spice mt-2"
        >
          + add step
        </button>
      </div>

      <button
        type="submit"
        className="bg-char text-crust rounded-full px-5 py-2 text-sm font-medium"
      >
        Save recipe
      </button>
    </form>
  )
}
