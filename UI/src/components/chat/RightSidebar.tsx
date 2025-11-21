import { motion } from 'framer-motion';

const RightSidebar = ({ isOpen, onToggle }: { isOpen: boolean; onToggle: () => void }) => {
  const contextData = {
    currentEmployee: {
      name: 'Sarah Chen',
      role: 'Engineering Manager',
      status: 'Active'
    },
    policiesReferenced: [
      'Leave Policy v3.2',
      'Remote Work Guidelines',
      'Benefits Handbook'
    ],
    filesSubmitted: [
      { name: 'org_chart_2024.pdf', size: '2.4 MB' },
      { name: 'policy_updates.docx', size: '156 KB' }
    ],
    detectedTasks: [
      'Employee lookup',
      'Policy search',
      'Analytics query'
    ],
    conversationSummary: 'Discussing employee records and leave policies for the Engineering department.',
    suggestedActions: [
      '📊 View team analytics',
      '📧 Send notification',
      '📄 Export report'
    ]
  };

  return (
    <>
      {/* Toggle Button for Mobile/Desktop */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        onClick={onToggle}
        className={`fixed ${isOpen ? 'right-72' : 'right-4'} top-20 z-50 w-10 h-10 bg-white border border-gray-300 rounded-xl flex items-center justify-center shadow-lg transition-all`}
      >
        {isOpen ? '→' : '←'}
      </motion.button>

      {/* Sidebar */}
      <motion.aside
        initial={{ x: 300 }}
        animate={{ x: isOpen ? 0 : 300 }}
        transition={{ type: 'spring', damping: 20 }}
        className="fixed right-0 top-0 h-screen w-80 bg-white border-l border-gray-200 z-40 overflow-y-auto shadow-lg"
      >
        <div className="p-6 space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-primary">Context Memory</h3>
            <motion.button
              whileHover={{ rotate: 180 }}
              className="text-gray-400 hover:text-gray-600"
            >
              ⚙️
            </motion.button>
          </div>

          {/* Current Employee */}
          <section className="bg-gradient-to-br from-accent/10 to-purple-100 rounded-2xl p-4">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-sm">👤</span>
              <h4 className="text-sm font-semibold text-primary">Current Employee</h4>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-accent to-purple-600 rounded-xl flex items-center justify-center text-white font-bold">
                SC
              </div>
              <div>
                <p className="font-semibold text-primary text-sm">{contextData.currentEmployee.name}</p>
                <p className="text-xs text-gray-600">{contextData.currentEmployee.role}</p>
                <span className="inline-block mt-1 px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                  {contextData.currentEmployee.status}
                </span>
              </div>
            </div>
          </section>

          {/* Policies Referenced */}
          <section>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-sm">📄</span>
              <h4 className="text-sm font-semibold text-primary">Policies Referenced</h4>
            </div>
            <div className="space-y-2">
              {contextData.policiesReferenced.map((policy, index) => (
                <motion.div
                  key={index}
                  whileHover={{ x: 4 }}
                  className="flex items-center gap-2 px-3 py-2 bg-neutral rounded-lg cursor-pointer"
                >
                  <div className="w-1.5 h-1.5 bg-accent rounded-full" />
                  <span className="text-sm text-gray-700">{policy}</span>
                </motion.div>
              ))}
            </div>
          </section>

          {/* Files Submitted */}
          <section>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-sm">📎</span>
              <h4 className="text-sm font-semibold text-primary">Files Submitted</h4>
            </div>
            {contextData.filesSubmitted.length > 0 ? (
              <div className="space-y-2">
                {contextData.filesSubmitted.map((file, index) => (
                  <motion.div
                    key={index}
                    whileHover={{ scale: 1.02 }}
                    className="flex items-center gap-3 px-3 py-2 bg-neutral rounded-lg"
                  >
                    <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600 text-xs font-bold">
                      PDF
                    </div>
                    <div className="flex-grow min-w-0">
                      <p className="text-sm font-medium text-gray-700 truncate">{file.name}</p>
                      <p className="text-xs text-gray-500">{file.size}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-400 italic">No files submitted</p>
            )}
          </section>

          {/* Detected Task Types */}
          <section>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-sm">🎯</span>
              <h4 className="text-sm font-semibold text-primary">Detected Tasks</h4>
            </div>
            <div className="flex flex-wrap gap-2">
              {contextData.detectedTasks.map((task, index) => (
                <motion.span
                  key={index}
                  whileHover={{ scale: 1.05 }}
                  className="px-3 py-1.5 bg-purple-100 text-purple-700 rounded-full text-xs font-medium"
                >
                  {task}
                </motion.span>
              ))}
            </div>
          </section>

          {/* Conversation Summary */}
          <section>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-sm">📝</span>
              <h4 className="text-sm font-semibold text-primary">Conversation Summary</h4>
            </div>
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-4">
              <p className="text-sm text-gray-700 leading-relaxed">
                {contextData.conversationSummary}
              </p>
            </div>
          </section>

          {/* Suggested Next Actions */}
          <section>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-sm">💡</span>
              <h4 className="text-sm font-semibold text-primary">Suggested Actions</h4>
            </div>
            <div className="space-y-2">
              {contextData.suggestedActions.map((action, index) => (
                <motion.button
                  key={index}
                  whileHover={{ scale: 1.02, x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full px-4 py-3 bg-gradient-to-r from-accent to-purple-600 text-white rounded-xl text-sm font-medium text-left shadow-soft hover:shadow-hover transition-all"
                >
                  {action}
                </motion.button>
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
          className="fixed inset-0 bg-black/30 z-30 lg:hidden"
        />
      )}
    </>
  );
};

export default RightSidebar;
