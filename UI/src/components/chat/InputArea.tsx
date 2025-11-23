import { motion } from 'framer-motion';
import { useState, useRef } from 'react';

interface InputAreaProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
}

const InputArea = ({ onSendMessage, disabled = false }: InputAreaProps) => {
  const [inputValue, setInputValue] = useState('');
  const [showPlugins, setShowPlugins] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const plugins = [
    { icon: '📊', label: 'Generate report', color: 'from-purple-500 to-pink-500' },
  ];

 

  const [selectedMode, setSelectedMode] = useState('creative');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !disabled) {
      onSendMessage(inputValue);
      setInputValue('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
    // Auto-expand textarea
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 150) + 'px';
  };

  return (
    <div className="px-6 py-4 w-full">
      <div className="max-w-4xl mx-auto w-full">


        {/* Input Container */}
        <form onSubmit={handleSubmit} className="relative">
          <motion.div
            whileFocus={{ boxShadow: '0 0 0 3px rgba(74, 125, 255, 0.1)' }}
            className="rounded-3xl border border-gray-300 flex items-end gap-3 px-6 py-4 transition-all"
          >
            {/* Left Actions */}
            <div className="flex items-center gap-2 pb-1">
              {/* Upload Button */}
              <motion.button
                type="button"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="w-9 h-9 flex items-center justify-center text-gray-600 hover:bg-white rounded-xl transition-colors"
                title="Upload files"
              >
                <span className="text-xl">📎</span>
              </motion.button>

              {/* Plugins Dropdown */}
              <div className="relative">
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowPlugins(!showPlugins)}
                  className="w-9 h-9 flex items-center justify-center text-gray-600 hover:bg-white rounded-xl transition-colors"
                  title="Plugins"
                >
                  <span className="text-xl">🧩</span>
                </motion.button>

                {/* Plugins Menu */}
                {showPlugins && (
                  <>
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      className="absolute bottom-full left-0 mb-2 w-64 bg-white rounded-2xl shadow-hover border border-gray-200 p-2 z-50"
                    >
                      <div className="text-xs font-semibold text-gray-500 px-3 py-2">Quick Actions</div>
                      {plugins.map((plugin, index) => (
                        <motion.button
                          key={index}
                          type="button"
                          whileHover={{ x: 4, backgroundColor: 'rgba(74, 125, 255, 0.05)' }}
                          onClick={() => {
                            setInputValue(plugin.label);
                            setShowPlugins(false);
                          }}
                          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-colors"
                        >
                          <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${plugin.color} flex items-center justify-center text-sm`}>
                            {plugin.icon}
                          </div>
                          <span className="text-sm font-medium text-gray-700">{plugin.label}</span>
                        </motion.button>
                      ))}
                    </motion.div>
                    <div
                      className="fixed inset-0 z-40"
                      onClick={() => setShowPlugins(false)}
                    />
                  </>
                )}
              </div>

              {/* Voice Input */}
              <motion.button
                type="button"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                className="w-9 h-9 flex items-center justify-center text-gray-600 hover:bg-white rounded-xl transition-colors"
                title="Voice input"
              >
                <span className="text-xl">🎤</span>
              </motion.button>
            </div>

            {/* Text Input */}
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={handleInput}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything... e.g. Who's on leave next week?"
              disabled={disabled}
              className="flex-grow bg-transparent resize-none focus:outline-none text-gray-800 placeholder-gray-400 max-h-[150px] min-h-[24px] leading-relaxed disabled:opacity-50 disabled:cursor-not-allowed"
              rows={1}
            />

            {/* Send Button */}
            <motion.button
              type="submit"
              whileHover={{ scale: 1.1, boxShadow: '0 0 20px rgba(74, 125, 255, 0.4)' }}
              whileTap={{ scale: 0.95 }}
              disabled={!inputValue.trim() || disabled}
              className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                inputValue.trim() && !disabled
                  ? 'bg-gradient-to-r from-accent to-purple-600 text-white shadow-lg'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
            >
              <span className="text-xl">➤</span>
            </motion.button>
          </motion.div>
        </form>

        {/* Helper Text */}
        <p className="text-xs text-gray-400 text-center mt-3">
          Press <kbd className="px-1.5 py-0.5 bg-gray-200 rounded text-gray-600 font-mono">Enter</kbd> to send,{' '}
          <kbd className="px-1.5 py-0.5 bg-gray-200 rounded text-gray-600 font-mono">Shift + Enter</kbd> for new line
        </p>
      </div>
    </div>
  );
};

export default InputArea;
