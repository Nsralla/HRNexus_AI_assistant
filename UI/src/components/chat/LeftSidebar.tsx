import { motion } from 'framer-motion';
// import { useState } from 'react';

const LeftSidebar = ({ isOpen, onToggle }: { isOpen: boolean; onToggle: () => void }) => {
  // const [activeSection] = useState('quick-actions');

  const conversations = {
    today: [
      { id: 1, title: 'Employee leave requests', time: '10:30 AM' },
      { id: 2, title: 'Engineering team headcount', time: '9:15 AM' }
    ],
    yesterday: [
      { id: 3, title: 'Q1 turnover analysis', time: 'Yesterday' },
      { id: 4, title: 'Onboarding checklist', time: 'Yesterday' }
    ],
    lastWeek: [
      { id: 5, title: 'Benefits policy review', time: '3 days ago' },
      { id: 6, title: 'Department org chart', time: '5 days ago' }
    ]
  };

  const quickActions = [
    { icon: '🔍', label: 'HR Policies', color: 'from-blue-500 to-cyan-500' },
    { icon: '📄', label: 'Employee Records', color: 'from-purple-500 to-pink-500' },
    { icon: '📝', label: 'Leaves & Requests', color: 'from-orange-500 to-red-500' },
    { icon: '🏢', label: 'Departments & Teams', color: 'from-green-500 to-emerald-500' },
    { icon: '📊', label: 'HR Analytics', color: 'from-indigo-500 to-purple-500' }
  ];

  const integrations = [
    { name: 'Jira', icon: 'J', connected: true },
    { name: 'Confluence', icon: 'C', connected: true },
    { name: 'HRIS', icon: 'H', connected: false },
    { name: 'SQL Sources', icon: 'S', connected: true }
  ];

  return (
    <>
      {/* Toggle Button - Visible on all screen sizes */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        onClick={onToggle}
        className="fixed top-20 left-4 z-50 w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shadow-lg"
      >
        {isOpen ? '✕' : '☰'}
      </motion.button>

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ x: isOpen ? 0 : -300 }}
        transition={{ type: 'spring', damping: 20 }}
        className="fixed top-0 left-0 h-screen w-72 bg-[#0D0F11] text-white z-40 overflow-y-auto"
      >
        <div className="p-6 space-y-6">

          {/* New Chat Button */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full py-3 bg-gradient-to-r from-accent to-purple-600 rounded-xl font-semibold text-white shadow-lg hover:shadow-xl transition-all"
          >
            + New Chat
          </motion.button>

          {/* Quick Actions */}
          <section>
            <h3 className="text-xs font-semibold text-gray-400 uppercase mb-3">Quick Actions</h3>
            <div className="space-y-2">
              {quickActions.map((action, index) => (
                <motion.button
                  key={index}
                  whileHover={{ x: 5, backgroundColor: 'rgba(74, 125, 255, 0.1)' }}
                  className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-300 hover:text-white transition-all"
                >
                  <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${action.color} flex items-center justify-center text-sm`}>
                    {action.icon}
                  </div>
                  <span className="text-sm font-medium">{action.label}</span>
                </motion.button>
              ))}
            </div>
          </section>

          {/* Conversation History */}
          <section>
            <h3 className="text-xs font-semibold text-gray-400 uppercase mb-3">Conversation History</h3>

            {/* Today */}
            <div className="mb-4">
              <p className="text-xs text-gray-500 mb-2 px-2">Today</p>
              {conversations.today.map((conv) => (
                <motion.div
                  key={conv.id}
                  whileHover={{ x: 5, backgroundColor: 'rgba(74, 125, 255, 0.1)' }}
                  className="px-3 py-2.5 rounded-lg cursor-pointer text-sm text-gray-300 hover:text-white transition-all mb-1"
                >
                  <p className="font-medium truncate">{conv.title}</p>
                  <p className="text-xs text-gray-500">{conv.time}</p>
                </motion.div>
              ))}
            </div>

            {/* Yesterday */}
            <div className="mb-4">
              <p className="text-xs text-gray-500 mb-2 px-2">Yesterday</p>
              {conversations.yesterday.map((conv) => (
                <motion.div
                  key={conv.id}
                  whileHover={{ x: 5, backgroundColor: 'rgba(74, 125, 255, 0.1)' }}
                  className="px-3 py-2.5 rounded-lg cursor-pointer text-sm text-gray-300 hover:text-white transition-all mb-1"
                >
                  <p className="font-medium truncate">{conv.title}</p>
                  <p className="text-xs text-gray-500">{conv.time}</p>
                </motion.div>
              ))}
            </div>

            {/* Last 7 Days */}
            <div>
              <p className="text-xs text-gray-500 mb-2 px-2">Last 7 Days</p>
              {conversations.lastWeek.map((conv) => (
                <motion.div
                  key={conv.id}
                  whileHover={{ x: 5, backgroundColor: 'rgba(74, 125, 255, 0.1)' }}
                  className="px-3 py-2.5 rounded-lg cursor-pointer text-sm text-gray-300 hover:text-white transition-all mb-1"
                >
                  <p className="font-medium truncate">{conv.title}</p>
                  <p className="text-xs text-gray-500">{conv.time}</p>
                </motion.div>
              ))}
            </div>
          </section>

          {/* Integrations */}
          <section>
            <h3 className="text-xs font-semibold text-gray-400 uppercase mb-3">Integrations</h3>
            <div className="space-y-2">
              {integrations.map((integration, index) => (
                <motion.div
                  key={index}
                  whileHover={{ x: 5 }}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg"
                >
                  <div className="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                    {integration.icon}
                  </div>
                  <span className="flex-grow text-sm text-gray-300">{integration.name}</span>
                  <div className={`w-2 h-2 rounded-full ${integration.connected ? 'bg-green-500' : 'bg-gray-600'}`} />
                </motion.div>
              ))}
            </div>
          </section>

        </div>
      </motion.aside>

      {/* Overlay for Mobile */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={onToggle}
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
        />
      )}
    </>
  );
};

export default LeftSidebar;
