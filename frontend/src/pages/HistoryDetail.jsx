import { useEffect, useState } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'
import { historyAPI } from '../lib/api'

export default function HistoryDetail() {
  const { blogId } = useParams()
  const [blog, setBlog] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    if (!blogId) {
      setError('Blog ID is missing')
      setLoading(false)
      return
    }

    const loadBlog = async () => {
      try {
        const response = await historyAPI.getBlog(blogId)
        setBlog(response.data)
      } catch (err) {
        console.error('Failed to load blog:', err)
        setError('Unable to load this blog. It may have been deleted or belong to another user.')
      } finally {
        setLoading(false)
      }
    }

    loadBlog()
  }, [blogId])

  const renderSections = () => {
    if (!blog) return null
    return (blog.blog.sections || []).map((section, index) => (
      <section key={index} className="space-y-2">
        <h3 className="text-lg font-semibold text-gray-800">{section.heading}</h3>
        <p className="text-gray-600 whitespace-pre-line">{section.content}</p>
      </section>
    ))
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <Link to="/history" className="inline-flex items-center text-sm text-primary-600 hover:text-primary-500">
          <ArrowLeftIcon className="w-4 h-4 mr-1" />
          Back to history
        </Link>
        <button
          onClick={() => navigate(-1)}
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          (or go back)
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center py-10">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600" />
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 p-4 rounded-lg text-sm text-red-700">
          {error}
        </div>
      ) : blog ? (
        <article className="space-y-4">
          <header className="space-y-2">
            <p className="text-xs uppercase tracking-wide text-gray-500">{new Date(blog.generated_at).toLocaleString()}</p>
            <h1 className="text-3xl font-bold text-gray-900">{blog.blog.title}</h1>
            <p className="text-gray-600 text-sm">{blog.blog.meta_description}</p>
            {blog.blog.featured_image && (
              <img
                src={blog.blog.featured_image.url}
                alt={blog.blog.featured_image.alt_text || 'Featured'}
                className="w-full rounded-lg shadow-sm"
              />
            )}
          </header>

            <div className="space-y-3">
              {blog.source_url && (
                <p className="text-sm text-gray-500">
                  Source URL: 
                  <a
                    className="text-primary-600 hover:underline"
                    href={blog.source_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {blog.source_url}
                  </a>
                </p>
              )}
              <p className="text-sm text-gray-500">Word count: {blog.word_count}</p>
              <p className="text-sm text-gray-500">Processing time: {blog.processing_time}s</p>
            </div>

          <div className="space-y-6">
            {renderSections()}
          </div>

          <div className="space-y-2">
            <h2 className="text-xl font-semibold text-gray-900">Conclusion</h2>
            <p className="text-gray-600 whitespace-pre-line">{blog.blog.conclusion}</p>
          </div>

          <div className="space-y-2">
            <h2 className="text-xl font-semibold text-gray-900">Call to Action</h2>
            <p className="text-gray-600 whitespace-pre-line">{blog.blog.cta}</p>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="p-4 border border-gray-100 rounded-lg bg-gray-50">
              <p className="text-sm font-medium text-gray-600">Primary Keywords</p>
              <div className="flex flex-wrap gap-2 mt-2">
                {blog.keywords?.primary_keywords?.map((keyword) => (
                  <span key={keyword} className="px-2 py-1 bg-white rounded-full text-xs text-gray-600 border border-gray-200">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
            <div className="p-4 border border-gray-100 rounded-lg bg-gray-50">
              <p className="text-sm font-medium text-gray-600">Secondary Keywords</p>
              <div className="flex flex-wrap gap-2 mt-2">
                {blog.keywords?.secondary_keywords?.map((keyword) => (
                  <span key={keyword} className="px-2 py-1 bg-white rounded-full text-xs text-gray-600 border border-gray-200">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </article>
      ) : (
        <div className="text-center text-gray-500">No blog found.</div>
      )}
    </div>
  )
}
