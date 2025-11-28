import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import LeftSidebar from '../components/chat/LeftSidebar';
import ChatArea from '../components/chat/ChatArea';
import InputArea from '../components/chat/InputArea';
import GuideCards from '../components/chat/GuideCards';
import DatasetInfoPopup from '../components/chat/DatasetInfoPopup';
import { chatService, type MessageResponse, type ChatResponse } from '../../services/chat.service';
import { getAuthToken } from '../../services/api.config';

const ChatPage = () => {
  const navigate = useNavigate();
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [chats, setChats] = useState<ChatResponse[]>([]);
  const [messages, setMessages] = useState<MessageResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSwitchingChat, setIsSwitchingChat] = useState(false);
  const [isCreatingChat, setIsCreatingChat] = useState(false);
  const [isLoadingChats, setIsLoadingChats] = useState(true);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showGuideCards, setShowGuideCards] = useState(false);

  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      navigate('/login');
      return;
    }
    initializeChat();
  }, [navigate]);

  const initializeChat = async () => {
    try {
      setError(null);
      setIsLoadingChats(true);
      const userChats = await chatService.getUserChats();
      setChats(userChats);

      if (userChats.length > 0) {
        const latestChat = userChats[0];
        setCurrentChatId(latestChat.id);
        await loadMessages(latestChat.id);
      } else {
        // No chats exist, create a new one and show guide cards
        const newChat = await chatService.createChat({ title: 'New Conversation' });
        setChats([newChat]);
        setCurrentChatId(newChat.id);
        setShowGuideCards(true); // Show guide cards for new users
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to initialize chat';
      setError(errorMessage);
      console.error('Failed to initialize chat:', err);
    } finally {
      setIsLoadingChats(false);
    }
  };

  const loadMessages = async (chatId: string, showLoading: boolean = true) => {
    try {
      setError(null);
      if (showLoading) {
        setIsLoadingMessages(true);
      }
      const chatMessages = await chatService.getChatMessages(chatId);
      setMessages(chatMessages);
      // Show guide cards if this is an empty chat
      setShowGuideCards(chatMessages.length === 0);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load messages';
      setError(errorMessage);
      console.error('Failed to load messages:', err);
    } finally {
      if (showLoading) {
        setIsLoadingMessages(false);
      }
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!currentChatId || !content.trim()) return;

    const currentChat = chats.find(c => c.id === currentChatId);
    const isFirstMessage = messages.length === 0;

    // Hide guide cards when sending a message
    setShowGuideCards(false);

    // Create optimistic user message
    const optimisticUserMessage: MessageResponse = {
      id: `temp-${Date.now()}`,
      chat_id: currentChatId,
      user_id: 'current-user',
      content: content.trim(),
      role: 'user',
      created_at: new Date().toISOString(),
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, optimisticUserMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Send message to backend
      await chatService.sendMessage({
        chat_id: currentChatId,
        content: content.trim(),
      });

      // Auto-name the chat based on first message if it's still "New Conversation"
      if (isFirstMessage && currentChat && currentChat.title === 'New Conversation') {
        const newTitle = content.trim().slice(0, 50) + (content.length > 50 ? '...' : '');
        await updateChatTitle(currentChatId, newTitle);
      }

      // Reload messages to get the actual messages with correct IDs and AI response
      // Don't show loading spinner since we already have the chat UI visible
      await loadMessages(currentChatId, false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      console.error('Failed to send message:', err);

      // Remove optimistic message on error
      setMessages(prev => prev.filter(msg => msg.id !== optimisticUserMessage.id));
    } finally {
      setIsLoading(false);
    }
  };

  const updateChatTitle = async (chatId: string, newTitle: string) => {
    try {
      // Update locally first for immediate UI feedback
      setChats(prev => prev.map(chat =>
        chat.id === chatId ? { ...chat, title: newTitle } : chat
      ));

      // Update on backend
      await chatService.updateChat(chatId, { title: newTitle });
    } catch (err) {
      console.error('Failed to update chat title:', err);
      // Revert local change on error
      const userChats = await chatService.getUserChats();
      setChats(userChats);
    }
  };

  const handleNewChat = async () => {
    try {
      setError(null);
      setIsCreatingChat(true);
      const newChat = await chatService.createChat({ title: 'New Conversation' });
      setChats((prev) => [newChat, ...prev]);
      setCurrentChatId(newChat.id);
      setMessages([]);
      setShowGuideCards(true); // Show guide cards for new empty chat
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create new chat';
      setError(errorMessage);
      console.error('Failed to create new chat:', err);
    } finally {
      setIsCreatingChat(false);
    }
  };

  const handleChatSelect = async (chatId: string) => {
    if (chatId === currentChatId) return;

    setIsSwitchingChat(true);
    setCurrentChatId(chatId);
    try {
      await loadMessages(chatId);
    } finally {
      setIsSwitchingChat(false);
    }
  };

  const handleDeleteChat = async (chatId: string) => {
    try {
      setError(null);

      // Delete the chat
      await chatService.deleteChat(chatId);

      // Remove from local state
      setChats(prev => prev.filter(chat => chat.id !== chatId));

      // If the deleted chat was the current one, switch to another chat or create new
      if (chatId === currentChatId) {
        const remainingChats = chats.filter(chat => chat.id !== chatId);
        if (remainingChats.length > 0) {
          const nextChat = remainingChats[0];
          setCurrentChatId(nextChat.id);
          await loadMessages(nextChat.id);
        } else {
          // No more chats, create a new one
          const newChat = await chatService.createChat({ title: 'New Conversation' });
          setChats([newChat]);
          setCurrentChatId(newChat.id);
          setMessages([]);
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete chat';
      setError(errorMessage);
      console.error('Failed to delete chat:', err);
    }
  };

  return (
    <div className="h-screen flex overflow-hidden bg-neutral">
      {/* Error Banner */}
      {error && (
        <div className="fixed top-0 left-0 right-0 bg-red-50 border-b border-red-200 px-6 py-3 flex items-center justify-between z-50">
          <div className="flex items-center gap-2 text-red-700">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span className="text-sm font-medium">{error}</span>
          </div>
          <button
            onClick={() => setError(null)}
            className="text-red-700 hover:text-red-900"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      )}

      <div className="flex-grow flex overflow-hidden relative w-full">
        <LeftSidebar
          isOpen={leftSidebarOpen}
          onToggle={() => setLeftSidebarOpen(!leftSidebarOpen)}
          chats={chats}
          currentChatId={currentChatId}
          onChatSelect={handleChatSelect}
          onNewChat={handleNewChat}
          onDeleteChat={handleDeleteChat}
          isCreatingChat={isCreatingChat}
          isLoadingChats={isLoadingChats}
        />

        <main
          className={`flex-grow flex flex-col w-full overflow-hidden transition-all duration-300 ${
            leftSidebarOpen ? 'ml-72' : 'ml-0'
          }`}
        >
          {isLoadingChats || isLoadingMessages ? (
            <div className="flex-1 flex items-center justify-center">
              <div className="flex flex-col items-center gap-4">
                <svg className="animate-spin h-12 w-12 text-accent" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p className="text-gray-500 text-sm">
                  {isLoadingChats ? 'Loading chats...' : 'Loading messages...'}
                </p>
              </div>
            </div>
          ) : showGuideCards && messages.length === 0 ? (
            <GuideCards
              onSelectPrompt={handleSendMessage}
              onClose={() => setShowGuideCards(false)}
            />
          ) : (
            <>
              <ChatArea messages={messages} isLoading={isLoading || isSwitchingChat} />
              <InputArea onSendMessage={handleSendMessage} disabled={isLoading || isSwitchingChat} />
            </>
          )}
        </main>

        {/* Dataset Info Popup - appears as floating widget */}
        <DatasetInfoPopup />
      </div>
    </div>
  );
};

export default ChatPage;
