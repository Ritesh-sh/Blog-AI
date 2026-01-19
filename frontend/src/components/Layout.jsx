import { Outlet, NavLink } from 'react-router-dom'
import { 
  HomeIcon, 
  SparklesIcon, 
  ClockIcon,
  ArrowRightOnRectangleIcon 
} from '@heroicons/react/24/outline'

const navigation = [
  { name: 'Dashboard', to: '/dashboard', icon: HomeIcon },
  { name: 'Generate Blog', to: '/generate', icon: SparklesIcon },
  { name: 'History', to: '/history', icon: ClockIcon },
]

export default function Layout({ onLogout }) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="fixed inset-y-0 left-0 w-64 bg-white border-r border-gray-200">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center h-16 px-6 border-b border-gray-200">
            <SparklesIcon className="w-8 h-8 text-primary-600" />
            <span className="ml-2 text-xl font-bold text-gray-900">AI Blog Gen</span>
          </div>
          
          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-1">
            {navigation.map((item) => (
              <NavLink
                key={item.name}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                    isActive
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`
                }
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.name}
              </NavLink>
            ))}
          </nav>
          
          {/* Logout */}
          <div className="p-4 border-t border-gray-200">
            <button
              onClick={onLogout}
              className="flex items-center w-full px-4 py-3 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <ArrowRightOnRectangleIcon className="w-5 h-5 mr-3" />
              Logout
            </button>
          </div>
        </div>
      </aside>
      
      {/* Main content */}
      <main className="ml-64 p-8">
        <Outlet />
      </main>
    </div>
  )
}
