import { motion, AnimatePresence } from 'framer-motion';
import { useState, useRef, useEffect } from 'react';
import { EmployeeCard, PolicyCard, AnalyticsCard, TaskCard, SQLCard } from './ResponseCards';
import NexusLogo from '../shared/NexusLogo';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  text: string;
  cardType?: 'employee' | 'policy' | 'analytics' | 'task' | 'sql';
  cardData?: any;
  timestamp: Date;
}

const ChatArea = () => {
  const [messages] = useState<Message[]>([
    {
      id: 1,
      type: 'assistant',
      text: "👋 Hello! I'm your HR AI Assistant. I can help you with employee records, policies, analytics, and more. What would you like to know?",
      timestamp: new Date()
    }
  ]);
  const [isTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const renderCard = (cardType: string, cardData: any) => {
    switch (cardType) {
      case 'employee':
        return <EmployeeCard data={cardData} />;
      case 'policy':
        return <PolicyCard data={cardData} />;
      case 'analytics':
        return <AnalyticsCard data={cardData} />;
      case 'task':
        return <TaskCard data={cardData} />;
      case 'sql':
        return <SQLCard data={cardData} />;
      default:
        return null;
    }
  };

  return (
    <div className="flex-grow flex flex-col h-full overflow-hidden">

      {/* Messages Container */}
      <div className="flex-grow overflow-y-auto p-6 bg-neutral w-full">
        <div className="max-w-4xl mx-auto space-y-6 w-full">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
              <div className={`flex gap-3 max-w-3xl ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                {/* Avatar */}
                {message.type === 'assistant' && (
                  <div className="flex-shrink-0">
                    <NexusLogo size={32} animate={false} />
                  </div>
                )}

                {/* Message Bubble */}
                <div className="flex flex-col gap-3">
                  <motion.div
                    className={`px-5 py-3 rounded-2xl ${
                      message.type === 'user'
                        ? 'bg-gradient-to-r from-accent to-purple-600 text-white rounded-br-md'
                        : 'bg-white/80 backdrop-blur-lg text-gray-800 border border-gray-200 rounded-bl-md shadow-soft'
                    }`}
                  >
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
                  </motion.div>

                  {/* Render Card if present */}
                  {message.cardType && message.cardData && (
                    <div>{renderCard(message.cardType, message.cardData)}</div>
                  )}

                  {/* Timestamp */}
                  <span className={`text-xs text-gray-400 ${message.type === 'user' ? 'text-right' : 'text-left'}`}>
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

          {/* Typing Indicator */}
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-3"
            >
              <NexusLogo size={32} animate={false} />
              <div className="bg-white/80 backdrop-blur-lg px-5 py-3 rounded-2xl rounded-bl-md border border-gray-200">
                <div className="flex gap-1">
                  <motion.div
                    animate={{ y: [0, -8, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, repeatDelay: 0 }}
                    className="w-2 h-2 bg-gray-400 rounded-full"
                  />
                  <motion.div
                    animate={{ y: [0, -8, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, repeatDelay: 0, delay: 0.2 }}
                    className="w-2 h-2 bg-gray-400 rounded-full"
                  />
                  <motion.div
                    animate={{ y: [0, -8, 0] }}
                    transition={{ duration: 0.6, repeat: Infinity, repeatDelay: 0, delay: 0.4 }}
                    className="w-2 h-2 bg-gray-400 rounded-full"
                  />
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Scroll to Bottom Button */}
      {messages.length > 3 && (
        <motion.button
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          whileHover={{ scale: 1.1 }}
          onClick={scrollToBottom}
          className="absolute bottom-24 right-8 w-10 h-10 bg-accent text-white rounded-full shadow-lg flex items-center justify-center"
        >
          ↓
        </motion.button>
      )}
    </div>
  );
};

export default ChatArea;
