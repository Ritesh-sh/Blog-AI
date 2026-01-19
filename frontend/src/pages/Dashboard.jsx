import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { blogAPI, historyAPI } from '../lib/api'
import { SparklesIcon, ClockIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline'

export default function Dashboard() {
  const [apiStatus, setApiStatus] = useState('checking')
  const [recentBlogs, setRecentBlogs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkApiHealth()
    loadRecentBlogs()
  }, [])

  const checkApiHealth = async () => {
    try {
      await blogAPI.health()
      setApiStatus('healthy')
    } catch {
      setApiStatus('unhealthy')
    }
  }

  const loadRecentBlogs = async () => {
    try {
      const response = await historyAPI.getHistory(5)
      setRecentBlogs(response.data || [])
    } catch (error) {
      console.error('Failed to load history:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Welcome to AI Blog Generator</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* API Status */}
        <div className="card">
          <div className="flex items-center">
            {apiStatus === 'healthy' ? (
              <CheckCircleIcon className="w-10 h-10 text-green-500" />
            ) : apiStatus === 'unhealthy' ? (
              <XCircleIcon className="w-10 h-10 text-red-500" />
            ) : (
              <div className="w-10 h-10 border-4 border-gray-200 border-t-primary-600 rounded-full animate-spin" />
            )}
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">API Status</p>
              <p className="text-lg font-semibold text-gray-900 capitalize">{apiStatus}</p>
            </div>
          </div>
        </div>

        {/* Quick Generate */}
        <div className="card bg-gradient-to-r from-primary-500 to-primary-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-primary-100 text-sm font-medium">Ready to create?</p>
              <p className="text-xl font-bold mt-1">Generate Blog</p>
            </div>
            <SparklesIcon className="w-12 h-12 text-primary-200" />
          </div>
          <Link 
            to="/generate" 
            className="mt-4 inline-block bg-white text-primary-600 px-4 py-2 rounded-lg font-medium hover:bg-primary-50 transition-colors"
          >
            Start Now →
          </Link>
        </div>

        {/* History Count */}
        <div className="card">
          <div className="flex items-center">
            <ClockIcon className="w-10 h-10 text-gray-400" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Recent Blogs</p>
              <p className="text-lg font-semibold text-gray-900">{recentBlogs.length} generated</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
        
        {loading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
        ) : recentBlogs.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <SparklesIcon className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No blogs generated yet</p>
            <Link to="/generate" className="text-primary-600 hover:underline mt-2 inline-block">
              Generate your first blog →
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {recentBlogs.map((blog, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{blog.action || 'Blog Generated'}</p>
                  <p className="text-sm text-gray-500">{new Date(blog.timestamp).toLocaleString()}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
