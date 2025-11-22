import { useState, useEffect } from 'react';
import TopNavBar from '../components/chat/TopNavBar';
import LeftSidebar from '../components/chat/LeftSidebar';
import ChatArea from '../components/chat/ChatArea';
import InputArea from '../components/chat/InputArea';
import RightSidebar from '../components/chat/RightSidebar';
import { chatService, type MessageResponse } from '../../services/chat.service';

const ChatPage = () => {
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [messages, setMessages] = useState<MessageResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    initializeChat();
  }, []);

  const initializeChat = async () => {
    try {
      const chats = await chatService.getUserChats();

      if (chats.length > 0) {
        const latestChat = chats[0];
        setCurrentChatId(latestChat.id);
        await loadMessages(latestChat.id);
      } else {
        const newChat = await chatService.createChat({ title: 'New Conversation' });
        setCurrentChatId(newChat.id);
      }
    } catch (error) {
      console.error('Failed to initialize chat:', error);
    }
  };

  const loadMessages = async (chatId: string) => {
    try {
      const chatMessages = await chatService.getChatMessages(chatId);
      setMessages(chatMessages);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!currentChatId || !content.trim()) return;

    setIsLoading(true);
    try {
      await chatService.sendMessage({
        chat_id: currentChatId,
        content: content.trim(),
      });

      await loadMessages(currentChatId);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-neutral">
      <TopNavBar />

      <div className="flex-grow flex overflow-hidden relative">
        <LeftSidebar
          isOpen={leftSidebarOpen}
          onToggle={() => setLeftSidebarOpen(!leftSidebarOpen)}
        />

        <main
          className={`flex-grow flex flex-col w-full overflow-hidden transition-all duration-300 ${
            leftSidebarOpen ? 'ml-72' : 'ml-0'
          }`}
        >
          <ChatArea messages={messages} isLoading={isLoading} />
          <InputArea onSendMessage={handleSendMessage} disabled={isLoading} />
        </main>

        <RightSidebar
          isOpen={rightSidebarOpen}
          onToggle={() => setRightSidebarOpen(!rightSidebarOpen)}
        />
      </div>
    </div>
  );
};

export default ChatPage;
