import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { documentService } from '../../../services/document.service';

interface DocumentUploadProps {
  isOpen: boolean;
  onClose: () => void;
}

const DocumentUpload = ({ isOpen, onClose }: DocumentUploadProps) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<Record<string, 'pending' | 'uploading' | 'success' | 'error'>>({});
  const [uploadResults, setUploadResults] = useState<Record<string, string>>({});
  const [error, setError] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const MAX_FILES = 10;
  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
  const ALLOWED_EXTENSIONS = ['.txt', '.md', '.json', '.csv', '.pdf'];
  const ALLOWED_TYPES = [
    'text/plain',
    'text/markdown',
    'application/json',
    'text/csv',
    'application/pdf',
    'application/x-pdf',
  ];

  const validateFile = (file: File): string | null => {
    const fileName = file.name.toLowerCase();
    const hasValidExtension = ALLOWED_EXTENSIONS.some(ext => fileName.endsWith(ext));

    if (!hasValidExtension && !ALLOWED_TYPES.includes(file.type)) {
      return `${file.name}: Invalid file type. Allowed: ${ALLOWED_EXTENSIONS.join(', ')}`;
    }

    if (file.size > MAX_FILE_SIZE) {
      return `${file.name}: File size exceeds 10MB limit`;
    }

    return null;
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError('');
    const files = Array.from(e.target.files || []);

    if (selectedFiles.length + files.length > MAX_FILES) {
      setError(`You can only upload up to ${MAX_FILES} files at once`);
      return;
    }

    const errors: string[] = [];
    const validFiles: File[] = [];

    files.forEach(file => {
      const validationError = validateFile(file);
      if (validationError) {
        errors.push(validationError);
      } else {
        validFiles.push(file);
      }
    });

    if (errors.length > 0) {
      setError(errors.join('\n'));
    }

    setSelectedFiles(prev => [...prev, ...validFiles]);

    // Reset the input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleRemoveFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
    setError('');
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;

    setUploading(true);
    setError('');

    // Initialize progress for all files
    const initialProgress: Record<string, 'pending' | 'uploading' | 'success' | 'error'> = {};
    selectedFiles.forEach(file => {
      initialProgress[file.name] = 'uploading';
    });
    setUploadProgress(initialProgress);

    // Upload files one by one to show progress
    const results: Record<string, string> = {};
    
    for (const file of selectedFiles) {
      try {
        const result = await documentService.uploadDocument(file);
        setUploadProgress(prev => ({ ...prev, [file.name]: 'success' }));
        results[file.name] = `✓ Uploaded successfully (${result.chunks_created || 0} chunks)`;
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Upload failed';
        setUploadProgress(prev => ({ ...prev, [file.name]: 'error' }));
        results[file.name] = `✗ ${errorMsg}`;
      }
    }

    setUploadResults(results);
    setUploading(false);

    // Auto-close after success (wait 2s to show results)
    const allSuccessful = Object.values(uploadProgress).every(status => status === 'success');
    if (allSuccessful) {
      setTimeout(() => {
        handleClose();
      }, 2000);
    }
  };

  const handleClose = () => {
    setSelectedFiles([]);
    setUploadProgress({});
    setUploadResults({});
    setError('');
    setUploading(false);
    onClose();
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      // Simulate file input change event
      const input = fileInputRef.current;
      if (input) {
        const dataTransfer = new DataTransfer();
        files.forEach(file => dataTransfer.items.add(file));
        input.files = dataTransfer.files;
        handleFileSelect({ target: input } as any);
      }
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'uploading':
        return <span className="animate-spin">⏳</span>;
      case 'success':
        return <span className="text-green-500">✓</span>;
      case 'error':
        return <span className="text-red-500">✗</span>;
      default:
        return <span className="text-gray-400">○</span>;
    }
  };

  const getFileIcon = (fileName: string) => {
    if (fileName.endsWith('.md')) return '📝';
    if (fileName.endsWith('.json')) return '📋';
    if (fileName.endsWith('.txt')) return '📄';
    if (fileName.endsWith('.csv')) return '📊';
    if (fileName.endsWith('.pdf')) return '📕';
    return '📎';
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
          >
            <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
              {/* Header */}
              <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-gray-800">Upload Documents</h2>
                  <p className="text-sm text-gray-500 mt-1">
                    Upload text files to embed in the knowledge base
                  </p>
                </div>
                <button
                  onClick={handleClose}
                  disabled={uploading}
                  className="text-gray-400 hover:text-gray-600 transition-colors disabled:opacity-50"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Content */}
              <div className="flex-1 overflow-y-auto px-6 py-4">
                {/* Hidden File Input */}
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept={ALLOWED_EXTENSIONS.join(',')}
                  onChange={handleFileSelect}
                  className="hidden"
                  disabled={uploading}
                />

                {/* Drag & Drop Zone */}
                <div
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={() => !uploading && fileInputRef.current?.click()}
                  className={`border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer
                    ${uploading ? 'border-gray-300 bg-gray-50 cursor-not-allowed' : 'border-blue-300 bg-blue-50/30 hover:bg-blue-50 hover:border-blue-400'}
                  `}
                >
                  <div className="flex flex-col items-center gap-3">
                    <svg className="w-16 h-16 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <div>
                      <p className="text-lg font-semibold text-gray-700">
                        Drop files here or click to browse
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        Supports: {ALLOWED_EXTENSIONS.join(', ')} (max 10MB each)
                      </p>
                    </div>
                  </div>
                </div>

                {/* Error Message */}
                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm flex items-start gap-2"
                  >
                    <span className="text-lg">⚠️</span>
                    <span className="whitespace-pre-line">{error}</span>
                  </motion.div>
                )}

                {/* Selected Files List */}
                {selectedFiles.length > 0 && (
                  <div className="mt-6">
                    <h3 className="text-sm font-semibold text-gray-700 mb-3">
                      Selected Files ({selectedFiles.length})
                    </h3>
                    <div className="space-y-2 max-h-60 overflow-y-auto">
                      {selectedFiles.map((file, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          className="flex items-center gap-3 bg-gray-50 border border-gray-200 rounded-lg px-4 py-3"
                        >
                          <span className="text-2xl">{getFileIcon(file.name)}</span>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-700 truncate">
                              {file.name}
                            </p>
                            <p className="text-xs text-gray-500">
                              {(file.size / 1024).toFixed(1)} KB
                            </p>
                            {uploadResults[file.name] && (
                              <p className="text-xs mt-1 text-gray-600">
                                {uploadResults[file.name]}
                              </p>
                            )}
                          </div>
                          {uploadProgress[file.name] ? (
                            <span className="text-xl">
                              {getStatusIcon(uploadProgress[file.name])}
                            </span>
                          ) : (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleRemoveFile(index);
                              }}
                              disabled={uploading}
                              className="text-gray-400 hover:text-red-500 transition-colors disabled:opacity-50"
                            >
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                              </svg>
                            </button>
                          )}
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Footer */}
              <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
                <p className="text-xs text-gray-500">
                  {selectedFiles.length} / {MAX_FILES} files selected
                </p>
                <div className="flex gap-3">
                  <button
                    onClick={handleClose}
                    disabled={uploading}
                    className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Cancel
                  </button>
                  <motion.button
                    onClick={handleUpload}
                    disabled={selectedFiles.length === 0 || uploading}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className={`px-6 py-2 rounded-lg font-semibold transition-all flex items-center gap-2
                      ${selectedFiles.length > 0 && !uploading
                        ? 'bg-gradient-to-r from-accent to-purple-600 text-white shadow-lg hover:shadow-xl'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      }
                    `}
                  >
                    {uploading ? (
                      <>
                        <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Uploading...
                      </>
                    ) : (
                      <>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        Upload Files
                      </>
                    )}
                  </motion.button>
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default DocumentUpload;

