import { motion, AnimatePresence } from 'framer-motion';
import { useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { EmployeeCard, PolicyCard, AnalyticsCard, TaskCard, SQLCard } from './ResponseCards';
import NexusLogo from '../shared/NexusLogo';
import type { MessageResponse } from '../../../services/chat.service';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  text: string;
  cardType?: 'employee' | 'policy' | 'analytics' | 'task' | 'sql';
  cardData?: any;
  timestamp: Date;
}

interface ChatAreaProps {
  messages: MessageResponse[];
  isLoading: boolean;
}

const ChatArea = ({ messages: apiMessages = [], isLoading = false }: ChatAreaProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const messages: Message[] = apiMessages.length > 0
    ? apiMessages.map(msg => ({
        id: msg.id,
        type: msg.role as 'user' | 'assistant',
        text: msg.content,
        timestamp: new Date(msg.created_at)
      }))
    : [
        {
          id: '1',
          type: 'assistant',
          text: "👋 Hello! I'm your HR AI Assistant. I can help you with employee records, policies, analytics, and more. What would you like to know?",
          timestamp: new Date()
        }
      ];

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
                    {message.type === 'assistant' ? (
                      <div className="prose prose-sm max-w-none">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            p: ({children}) => <p className="text-sm leading-relaxed mb-3 text-gray-700 last:mb-0">{children}</p>,
                            strong: ({children}) => <strong className="font-bold text-gray-900">{children}</strong>,
                            em: ({children}) => <em className="italic text-gray-700">{children}</em>,
                            ul: ({children}) => <ul className="list-disc list-outside ml-4 space-y-1 my-3">{children}</ul>,
                            ol: ({children}) => <ol className="list-decimal list-outside ml-4 space-y-1 my-3">{children}</ol>,
                            li: ({children}) => <li className="text-sm leading-relaxed text-gray-700 pl-1">{children}</li>,
                            h1: ({children}) => <h1 className="text-xl font-bold mb-3 mt-4 text-gray-900 border-b border-gray-200 pb-2 first:mt-0">{children}</h1>,
                            h2: ({children}) => <h2 className="text-lg font-bold mb-2 mt-4 text-gray-900 first:mt-0">{children}</h2>,
                            h3: ({children}) => <h3 className="text-base font-semibold mb-2 mt-3 text-gray-800 first:mt-0">{children}</h3>,
                            h4: ({children}) => <h4 className="text-sm font-semibold mb-1 mt-2 text-gray-800">{children}</h4>,
                            blockquote: ({children}) => (
                              <blockquote className="border-l-4 border-accent pl-4 py-2 my-3 bg-blue-50 rounded-r">
                                {children}
                              </blockquote>
                            ),
                            hr: () => <hr className="my-4 border-gray-300" />,
                            a: ({href, children}) => (
                              <a 
                                href={href} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-accent hover:text-purple-600 underline font-medium"
                              >
                                {children}
                              </a>
                            ),
                            table: ({children}) => (
                              <div className="overflow-x-auto my-4 rounded-lg border border-gray-200">
                                <table className="min-w-full divide-y divide-gray-200">
                                  {children}
                                </table>
                              </div>
                            ),
                            thead: ({children}) => (
                              <thead className="bg-gray-100">
                                {children}
                              </thead>
                            ),
                            tbody: ({children}) => (
                              <tbody className="bg-white divide-y divide-gray-200">
                                {children}
                              </tbody>
                            ),
                            tr: ({children}) => (
                              <tr className="hover:bg-gray-50 transition-colors">
                                {children}
                              </tr>
                            ),
                            th: ({children}) => (
                              <th className="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                                {children}
                              </th>
                            ),
                            td: ({children}) => (
                              <td className="px-4 py-3 text-sm text-gray-700 whitespace-normal">
                                {children}
                              </td>
                            ),
                            code: ({children, className}) => {
                              const isInline = !className?.includes('language-');
                              return isInline ? (
                                <code className="px-1.5 py-0.5 bg-pink-100 text-pink-700 rounded text-xs font-mono border border-pink-200">
                                  {children}
                                </code>
                              ) : (
                                <code className="block p-4 bg-gray-900 text-gray-100 rounded-lg text-xs font-mono overflow-x-auto my-3 border border-gray-700">
                                  {children}
                                </code>
                              );
                            },
                            pre: ({children}) => (
                              <pre className="my-3 rounded-lg overflow-hidden">
                                {children}
                              </pre>
                            ),
                          }}
                        >
                          {message.text}
                        </ReactMarkdown>
                      </div>
                    ) : (
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
                    )}
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
          {isLoading && (
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
