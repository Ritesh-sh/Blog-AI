import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { historyAPI } from '../lib/api'
import { ClockIcon } from '@heroicons/react/24/outline'

export default function History() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const response = await historyAPI.getHistory(50)
      setHistory(response.data || [])
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
        <h1 className="text-3xl font-bold text-gray-900">History</h1>
        <p className="text-gray-600 mt-1">Your blog generation history</p>
      </div>

      {/* History List */}
      <div className="card">
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600"></div>
          </div>
        ) : history.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <ClockIcon className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <p className="text-lg">No history yet</p>
            <p className="text-sm mt-1">Generated blogs will appear here</p>
          </div>
        ) : (
          <div className="space-y-4">
            {history.map((item, index) => {
              const isBlogEntry = item.action === 'generate_blog' && item.data?.blog_id
              const CardComponent = isBlogEntry ? Link : 'div'
              const cardProps = isBlogEntry ? { to: `/history/${item.data.blog_id}` } : {}
              return (
                <CardComponent
                  key={item.id || index}
                  {...cardProps}
                  className={`flex items-center justify-between p-4 bg-gray-50 rounded-lg transition-colors ${
                    isBlogEntry ? 'hover:bg-gray-100 cursor-pointer' : 'hover:bg-gray-100'
                  }`}
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        item.action === 'generate_blog' 
                          ? 'bg-green-100 text-green-700' 
                          : item.action === 'login'
                          ? 'bg-blue-100 text-blue-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}>
                        {item.action?.replace('_', ' ') || 'Action'}
                      </span>
                    </div>
                    {item.data?.url && (
                      <p className="text-sm text-gray-600 mt-1 truncate max-w-md">
                        {item.data.url}
                      </p>
                    )}
                    {item.data?.title && (
                      <p className="font-medium text-gray-900 mt-1">
                        {item.data.title}
                      </p>
                    )}
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-500">
                      {new Date(item.timestamp).toLocaleDateString()}
                    </p>
                    <p className="text-xs text-gray-400">
                      {new Date(item.timestamp).toLocaleTimeString()}
                    </p>
                    {isBlogEntry && (
                      <p className="text-xs text-primary-600 mt-2">View blog →</p>
                    )}
                  </div>
                </CardComponent>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
