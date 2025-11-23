import { motion } from 'framer-motion';
import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import NexusLogo from '../shared/NexusLogo';
import { authService } from '../../../services/auth.service';

interface Chat {
  id: string;
  title: string;
  created_at: string;
}

interface LeftSidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  chats: Chat[];
  currentChatId: string | null;
  onChatSelect: (chatId: string) => void;
  onNewChat: () => void;
  onDeleteChat: (chatId: string) => void;
  isCreatingChat?: boolean;
}

const LeftSidebar = ({
  isOpen,
  onToggle,
  chats,
  currentChatId,
  onChatSelect,
  onNewChat,
  onDeleteChat,
  isCreatingChat = false
}: LeftSidebarProps) => {
  const navigate = useNavigate();
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  // Group chats by time period
  const groupedChats = useMemo(() => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const lastWeek = new Date(today);
    lastWeek.setDate(lastWeek.getDate() - 7);

    const groups = {
      today: [] as Chat[],
      yesterday: [] as Chat[],
      lastWeek: [] as Chat[],
      older: [] as Chat[]
    };

    chats.forEach(chat => {
      const chatDate = new Date(chat.created_at);
      if (chatDate >= today) {
        groups.today.push(chat);
      } else if (chatDate >= yesterday) {
        groups.yesterday.push(chat);
      } else if (chatDate >= lastWeek) {
        groups.lastWeek.push(chat);
      } else {
        groups.older.push(chat);
      }
    });

    return groups;
  }, [chats]);

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date >= today) {
      return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
    } else if (date >= yesterday) {
      return 'Yesterday';
    } else {
      const daysAgo = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
      return `${daysAgo} days ago`;
    }
  };

  const handleDeleteClick = (e: React.MouseEvent, chatId: string) => {
    e.stopPropagation(); // Prevent chat selection
    setDeleteConfirmId(chatId);
  };

  const confirmDelete = () => {
    if (deleteConfirmId) {
      onDeleteChat(deleteConfirmId);
      setDeleteConfirmId(null);
    }
  };

  const cancelDelete = () => {
    setDeleteConfirmId(null);
  };

  // const quickActions = [
  //   { icon: '🔍', label: 'HR Policies', color: 'from-blue-500 to-cyan-500' },
  //   { icon: '📄', label: 'Employee Records', color: 'from-purple-500 to-pink-500' },
  //   { icon: '📝', label: 'Leaves & Requests', color: 'from-orange-500 to-red-500' },
  //   { icon: '🏢', label: 'Departments & Teams', color: 'from-green-500 to-emerald-500' },
  //   { icon: '📊', label: 'HR Analytics', color: 'from-indigo-500 to-purple-500' }
  // ];

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
        className="fixed top-4 left-4 z-50 w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shadow-lg"
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
        <div className="pt-16 p-6 space-y-6">
          {/* Logo and Logout Section */}
          <div className="flex flex-col gap-4 pb-4 border-b border-gray-700">
            {/* Logo */}
            <div
              onClick={() => navigate('/')}
              className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity"
            >
              <NexusLogo size={40} animate={false} />
              <div>
                <h1 className="text-xl font-bold text-white">HR Nexus</h1>
                <p className="text-xs text-gray-400">
                  Powered by LLM + RAG + LangGraph
                </p>
              </div>
            </div>

            {/* Logout Button */}
            <motion.button
              onClick={handleLogout}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              title="Logout"
              className="w-full px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-xl font-medium text-sm transition-colors"
            >
              Logout
            </motion.button>
          </div>

          {/* New Chat Button */}
          <motion.button
            whileHover={{ scale: isCreatingChat ? 1 : 1.02 }}
            whileTap={{ scale: isCreatingChat ? 1 : 0.98 }}
            onClick={onNewChat}
            disabled={isCreatingChat}
            className={`w-full py-3 bg-gradient-to-r from-accent to-purple-600 rounded-xl font-semibold text-white shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2 ${
              isCreatingChat ? 'opacity-70 cursor-not-allowed' : ''
            }`}
          >
            {isCreatingChat ? (
              <>
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating...
              </>
            ) : (
              '+ New Chat'
            )}
          </motion.button>

          {/* Quick Actions */}
          {/* <section>
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
          </section> */}

          {/* Conversation History */}
          <section>
            <h3 className="text-xs font-semibold text-gray-400 uppercase mb-3">Conversation History</h3>

            {chats.length === 0 ? (
              <p className="text-sm text-gray-500 px-2">No conversations yet. Start a new chat!</p>
            ) : (
              <>
                {/* Today */}
                {groupedChats.today.length > 0 && (
                  <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-2 px-2">Today</p>
                    {groupedChats.today.map((chat) => (
                      <motion.div
                        key={chat.id}
                        whileHover={{ x: 5, backgroundColor: 'rgba(74, 125, 255, 0.1)' }}
                        className={`group px-3 py-2.5 rounded-lg cursor-pointer text-sm transition-all mb-1 relative ${
                          currentChatId === chat.id
                            ? 'bg-gradient-to-r from-accent/30 to-purple-600/30 text-white border-l-2 border-accent shadow-md'
                            : 'text-gray-300 hover:text-white'
                        }`}
                      >
                        <div onClick={() => onChatSelect(chat.id)} className="flex-1 pr-8">
                          <p className="font-medium truncate">{chat.title}</p>
                          <p className="text-xs text-gray-500">{formatTime(chat.created_at)}</p>
                        </div>
                        <button
                          onClick={(e) => handleDeleteClick(e, chat.id)}
                          className="absolute right-2 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-red-500/20 rounded"
                          title="Delete chat"
                        >
                          <svg className="w-4 h-4 text-red-400 hover:text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </motion.div>
                    ))}
                  </div>
                )}

                {/* Yesterday */}
                {groupedChats.yesterday.length > 0 && (
                  <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-2 px-2">Yesterday</p>
                    {groupedChats.yesterday.map((chat) => (
                      <motion.div
                        key={chat.id}
                        whileHover={{ x: 5, backgroundColor: 'rgba(74, 125, 255, 0.1)' }}
                        className={`group px-3 py-2.5 rounded-lg cursor-pointer text-sm transition-all mb-1 relative ${
                          currentChatId === chat.id
                            ? 'bg-gradient-to-r from-accent/30 to-purple-600/30 text-white border-l-2 border-accent shadow-md'
                            : 'text-gray-300 hover:text-white'
                        }`}
                      >
                        <div onClick={() => onChatSelect(chat.id)} className="flex-1 pr-8">
                          <p className="font-medium truncate">{chat.title}</p>
                          <p className="text-xs text-gray-500">{formatTime(chat.created_at)}</p>
                        </div>
                        <button
                          onClick={(e) => handleDeleteClick(e, chat.id)}
                          className="absolute right-2 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-red-500/20 rounded"
                          title="Delete chat"
                        >
                          <svg className="w-4 h-4 text-red-400 hover:text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </motion.div>
                    ))}
                  </div>
                )}

                {/* Last 7 Days */}
                {groupedChats.lastWeek.length > 0 && (
                  <div className="mb-4">
                    <p className="text-xs text-gray-500 mb-2 px-2">Last 7 Days</p>
                    {groupedChats.lastWeek.map((chat) => (
                      <motion.div
                        key={chat.id}
                        whileHover={{ x: 5, backgroundColor: 'rgba(74, 125, 255, 0.1)' }}
                        className={`group px-3 py-2.5 rounded-lg cursor-pointer text-sm transition-all mb-1 relative ${
                          currentChatId === chat.id
                            ? 'bg-gradient-to-r from-accent/30 to-purple-600/30 text-white border-l-2 border-accent shadow-md'
                            : 'text-gray-300 hover:text-white'
                        }`}
                      >
                        <div onClick={() => onChatSelect(chat.id)} className="flex-1 pr-8">
                          <p className="font-medium truncate">{chat.title}</p>
                          <p className="text-xs text-gray-500">{formatTime(chat.created_at)}</p>
                        </div>
                        <button
                          onClick={(e) => handleDeleteClick(e, chat.id)}
                          className="absolute right-2 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-red-500/20 rounded"
                          title="Delete chat"
                        >
                          <svg className="w-4 h-4 text-red-400 hover:text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </motion.div>
                    ))}
                  </div>
                )}

                {/* Older */}
                {groupedChats.older.length > 0 && (
                  <div>
                    <p className="text-xs text-gray-500 mb-2 px-2">Older</p>
                    {groupedChats.older.map((chat) => (
                      <motion.div
                        key={chat.id}
                        whileHover={{ x: 5, backgroundColor: 'rgba(74, 125, 255, 0.1)' }}
                        className={`group px-3 py-2.5 rounded-lg cursor-pointer text-sm transition-all mb-1 relative ${
                          currentChatId === chat.id
                            ? 'bg-gradient-to-r from-accent/30 to-purple-600/30 text-white border-l-2 border-accent shadow-md'
                            : 'text-gray-300 hover:text-white'
                        }`}
                      >
                        <div onClick={() => onChatSelect(chat.id)} className="flex-1 pr-8">
                          <p className="font-medium truncate">{chat.title}</p>
                          <p className="text-xs text-gray-500">{formatTime(chat.created_at)}</p>
                        </div>
                        <button
                          onClick={(e) => handleDeleteClick(e, chat.id)}
                          className="absolute right-2 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-red-500/20 rounded"
                          title="Delete chat"
                        >
                          <svg className="w-4 h-4 text-red-400 hover:text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </motion.div>
                    ))}
                  </div>
                )}
              </>
            )}
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

      {/* Delete Confirmation Modal */}
      {deleteConfirmId && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">Delete Chat</h3>
                <p className="text-sm text-gray-500">This action cannot be undone</p>
              </div>
            </div>

            <p className="text-gray-700 mb-6">
              Are you sure you want to delete this chat? All messages in this conversation will be permanently removed.
            </p>

            <div className="flex gap-3">
              <button
                onClick={cancelDelete}
                className="flex-1 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl transition-colors"
              >
                Delete
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </>
  );
};

export default LeftSidebar;
