import { Routes, Route, Link } from 'react-router-dom'
import RecipeList from './components/RecipeList.jsx'
import RecipeDetail from './components/RecipeDetail.jsx'
import RecipeForm from './components/RecipeForm.jsx'

export default function App() {
  return (
    <div className="min-h-screen bg-crust">
      <header className="border-b border-line">
        <div className="max-w-4xl mx-auto px-6 py-6 flex items-baseline justify-between">
          <Link to="/">
            <h1 className="font-display text-3xl tracking-tight">
              Recipe Remix
            </h1>
            <p className="text-sm text-char/60 italic mt-0.5">
              swap what you can't eat, keep what you love
            </p>
          </Link>
          <Link
            to="/new"
            className="font-medium text-sm border border-char rounded-full px-4 py-2 hover:bg-char hover:text-crust transition-colors"
          >
            + Add a recipe
          </Link>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-10">
        <Routes>
          <Route path="/" element={<RecipeList />} />
          <Route path="/recipes/:id" element={<RecipeDetail />} />
          <Route path="/new" element={<RecipeForm />} />
        </Routes>
      </main>
    </div>
  )
}
