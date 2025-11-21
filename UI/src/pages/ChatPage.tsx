import { useState } from 'react';
import TopNavBar from '../components/chat/TopNavBar';
import LeftSidebar from '../components/chat/LeftSidebar';
import ChatArea from '../components/chat/ChatArea';
import InputArea from '../components/chat/InputArea';
import RightSidebar from '../components/chat/RightSidebar';

const ChatPage = () => {
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false);

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-neutral">
      {/* Top Navigation */}
      <TopNavBar />

      {/* Main Layout */}
      <div className="flex-grow flex overflow-hidden relative">
        {/* Left Sidebar */}
        <LeftSidebar
          isOpen={leftSidebarOpen}
          onToggle={() => setLeftSidebarOpen(!leftSidebarOpen)}
        />

        {/* Main Chat Area */}
        <main
          className={`flex-grow flex flex-col w-full overflow-hidden transition-all duration-300 ${
            leftSidebarOpen ? 'ml-72' : 'ml-0'
          }`}
        >
          <ChatArea />
          <InputArea />
        </main>

        {/* Right Sidebar */}
        <RightSidebar
          isOpen={rightSidebarOpen}
          onToggle={() => setRightSidebarOpen(!rightSidebarOpen)}
        />
      </div>
    </div>
  );
};

export default ChatPage;
