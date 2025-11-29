import { motion, AnimatePresence } from 'framer-motion';
import { useState, useRef } from 'react';

interface InputAreaProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
}

const InputArea = ({ onSendMessage, disabled = false }: InputAreaProps) => {
  const [inputValue, setInputValue] = useState('');
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [fileError, setFileError] = useState<string>('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

 

  const MAX_FILES = 4;
  const ALLOWED_EXTENSIONS = ['.md', '.json'];
  const ALLOWED_TYPES = ['text/markdown', 'application/json', 'text/plain'];

  const validateFile = (file: File): boolean => {
    const fileName = file.name.toLowerCase();
    const hasValidExtension = ALLOWED_EXTENSIONS.some(ext => fileName.endsWith(ext));

    if (!hasValidExtension && !ALLOWED_TYPES.includes(file.type)) {
      return false;
    }
    return true;
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFileError('');
    const files = Array.from(e.target.files || []);

    if (selectedFiles.length + files.length > MAX_FILES) {
      setFileError(`You can only upload up to ${MAX_FILES} files at once`);
      return;
    }

    const invalidFiles = files.filter(file => !validateFile(file));
    if (invalidFiles.length > 0) {
      setFileError(`Only .md and .json files are supported`);
      return;
    }

    setSelectedFiles(prev => [...prev, ...files]);

    // Reset the input so the same file can be selected again
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleRemoveFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
    setFileError('');
  };


  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !disabled) {
      onSendMessage(inputValue);
      setInputValue('');
      setSelectedFiles([]);
      setFileError('');
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
        {/* Selected Files Preview */}
        <AnimatePresence>
          {selectedFiles.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mb-3 flex flex-wrap gap-2"
            >
              {selectedFiles.map((file, index) => (
                <motion.div
                  key={index}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0.8, opacity: 0 }}
                  className="flex items-center gap-2 bg-blue-50 border border-blue-200 rounded-lg px-3 py-2"
                >
                  <span className="text-sm">
                    {file.name.endsWith('.md') ? '📝' : '📋'}
                  </span>
                  <span className="text-sm text-gray-700 max-w-[200px] truncate">
                    {file.name}
                  </span>
                  <span className="text-xs text-gray-500">
                    ({(file.size / 1024).toFixed(1)} KB)
                  </span>
                  <button
                    type="button"
                    onClick={() => handleRemoveFile(index)}
                    className="ml-1 text-gray-400 hover:text-red-500 transition-colors"
                    title="Remove file"
                  >
                    ✕
                  </button>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error Message */}
        <AnimatePresence>
          {fileError && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mb-3 bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg text-sm flex items-center gap-2"
            >
              <span>⚠️</span>
              <span>{fileError}</span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".md,.json,text/markdown,application/json"
          onChange={handleFileSelect}
          className="hidden"
        />

        {/* Input Container */}
        <form onSubmit={handleSubmit} className="relative">
          <motion.div
            whileFocus={{ boxShadow: '0 0 0 3px rgba(74, 125, 255, 0.1)' }}
            className="rounded-3xl border border-gray-300 flex items-end gap-3 px-6 py-4 transition-all"
          >
          

            {/* Text Input */}
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={handleInput}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything... e.g. Who's on the backend team?"
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
        <div className="mt-3 flex flex-col sm:flex-row items-center justify-center gap-2 text-xs text-gray-400">
          <p>
            Press <kbd className="px-1.5 py-0.5 bg-gray-200 rounded text-gray-600 font-mono">Enter</kbd> to send,{' '}
            <kbd className="px-1.5 py-0.5 bg-gray-200 rounded text-gray-600 font-mono">Shift + Enter</kbd> for new line
          </p>
          <span className="hidden sm:inline text-gray-300">|</span>
          <p className="text-center">
            Upload up to <span className="font-semibold text-gray-500">4 files</span> (.md, .json)
          </p>
        </div>
      </div>
    </div>
  );
};

export default InputArea;
