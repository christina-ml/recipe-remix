const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed: ${res.status}`)
  }
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  listRecipes: () => request('/recipes/'),
  getRecipe: (id) => request(`/recipes/${id}`),
  createRecipe: (recipe) =>
    request('/recipes/', { method: 'POST', body: JSON.stringify(recipe) }),
  deleteRecipe: (id) => request(`/recipes/${id}`, { method: 'DELETE' }),
  remixRecipe: (id, diet) =>
    request(`/recipes/${id}/remix`, {
      method: 'POST',
      body: JSON.stringify({ diet }),
    }),
  voteSubstitution: (id, value) =>
    request(`/substitutions/${id}/vote`, {
      method: 'POST',
      body: JSON.stringify({ value }),
    }),
}
