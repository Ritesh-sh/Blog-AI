import { useState } from 'react'
import { blogAPI } from '../lib/api'
import toast from 'react-hot-toast'
import ReactMarkdown from 'react-markdown'

const TONES = ['Professional', 'Casual', 'Technical', 'Conversational']

export default function Generate() {
  const [url, setUrl] = useState('')
  const [tone, setTone] = useState('Professional')
  const [wordCount, setWordCount] = useState(800)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleGenerate = async (e) => {
    e.preventDefault()
    
    if (!url.trim()) {
      toast.error('Please enter a URL')
      return
    }

    setLoading(true)
    setResult(null)

    try {
      const response = await blogAPI.generate(url, tone.toLowerCase(), wordCount)
      setResult(response.data)
      toast.success('Blog generated successfully!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to generate blog')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Generate Blog</h1>
        <p className="text-gray-600 mt-1">Create SEO-optimized content from any URL</p>
      </div>

      {/* Form */}
      <div className="card">
        <form onSubmit={handleGenerate} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Website URL
            </label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="input-field"
              placeholder="https://example.com/article"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Writing Tone
              </label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="input-field"
              >
                {TONES.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Word Count: {wordCount}
              </label>
              <input
                type="range"
                min="300"
                max="2000"
                step="100"
                value={wordCount}
                onChange={(e) => setWordCount(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>300</span>
                <span>2000</span>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full py-3 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Generating... (this may take a minute)
              </>
            ) : (
              <>
                🚀 Generate Blog
              </>
            )}
          </button>
        </form>
      </div>

      {/* Result */}
      {result && (
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            {result.blog?.title || 'Generated Blog'}
          </h2>
          
          {/* Meta Description */}
          {result.blog?.meta_description && (
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6 rounded-r-lg">
              <p className="text-sm font-medium text-blue-700">Meta Description</p>
              <p className="text-blue-900">{result.blog.meta_description}</p>
            </div>
          )}

          {/* Featured Image */}
          {result.blog?.featured_image?.url && (
            <img
              src={result.blog.featured_image.url}
              alt={result.blog.featured_image.alt_text || result.blog.title}
              className="w-full h-64 object-cover rounded-lg mb-6"
            />
          )}

          {/* Introduction */}
          <div className="prose max-w-none mb-6">
            <h3 className="text-xl font-semibold text-gray-900">Introduction</h3>
            <p className="text-gray-700 leading-relaxed">{result.blog?.introduction}</p>
          </div>

          {/* Sections */}
          {result.blog?.sections?.map((section, index) => (
            <div key={index} className="prose max-w-none mb-6">
              <h3 className="text-xl font-semibold text-gray-900">{section.heading}</h3>
              <p className="text-gray-700 leading-relaxed">{section.content}</p>
            </div>
          ))}

          {/* Conclusion */}
          <div className="prose max-w-none mb-6">
            <h3 className="text-xl font-semibold text-gray-900">Conclusion</h3>
            <p className="text-gray-700 leading-relaxed">{result.blog?.conclusion}</p>
          </div>

          {/* CTA */}
          {result.blog?.cta && (
            <div className="bg-gradient-to-r from-primary-500 to-primary-600 text-white p-6 rounded-lg text-center">
              <p className="text-lg font-semibold">{result.blog.cta}</p>
            </div>
          )}

          {/* Stats */}
          <div className="mt-6 pt-6 border-t border-gray-200 flex flex-wrap gap-4 text-sm text-gray-600">
            <span><strong>Tags:</strong> {result.blog?.tags?.join(', ')}</span>
            <span><strong>Word Count:</strong> {result.word_count}</span>
            <span><strong>Processing Time:</strong> {result.processing_time}s</span>
          </div>
        </div>
      )}
    </div>
  )
}
