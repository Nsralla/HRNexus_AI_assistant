import { motion, AnimatePresence } from 'framer-motion';
import { Globe, X } from 'lucide-react';
import { useEffect } from 'react';

interface WebSearchBannerProps {
    onDismiss: () => void;
    isVisible: boolean;
}

const WebSearchBanner = ({ onDismiss, isVisible }: WebSearchBannerProps) => {
    // Auto-dismiss after 8 seconds
    useEffect(() => {
        if (isVisible) {
            const timer = setTimeout(() => {
                onDismiss();
            }, 8000);

            return () => clearTimeout(timer);
        }
    }, [isVisible, onDismiss]);

    return (
        <AnimatePresence>
            {isVisible && (
                <motion.div
                    initial={{ x: 400, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    exit={{ x: 400, opacity: 0 }}
                    transition={{ duration: 0.4, ease: 'easeOut' }}
                    className="fixed top-4 right-4 max-w-md w-full sm:w-auto z-50 pointer-events-auto px-4 sm:px-0"
                >
                    <div className="bg-white rounded-lg shadow-2xl border-l-4 border-accent overflow-hidden">
                        <div className="p-4">
                            <div className="flex items-start gap-3">
                                {/* Icon */}
                                <div className="flex-shrink-0">
                                    <div className="w-10 h-10 bg-accent/10 rounded-full flex items-center justify-center">
                                        <Globe className="w-5 h-5 text-accent" />
                                    </div>
                                </div>

                                {/* Content */}
                                <div className="flex-1 min-w-0 pt-0.5">
                                    <div className="flex items-start justify-between gap-2">
                                        <div className="flex-1">
                                            <h3 className="text-sm font-bold text-gray-900 mb-1">
                                                🌐 Web Search Available!
                                            </h3>
                                            <p className="text-xs text-gray-600 leading-relaxed">
                                                Ask about trends, current news, or anything beyond company data.
                                            </p>
                                        </div>

                                        {/* Dismiss Button */}
                                        <button
                                            onClick={onDismiss}
                                            className="flex-shrink-0 p-1 rounded-md hover:bg-gray-100 transition-colors"
                                            aria-label="Dismiss notification"
                                        >
                                            <X className="w-4 h-4 text-gray-400 hover:text-gray-600" />
                                        </button>
                                    </div>
                                </div>
                            </div>

                            {/* Progress bar for auto-dismiss */}
                            <motion.div
                                initial={{ scaleX: 1 }}
                                animate={{ scaleX: 0 }}
                                transition={{ duration: 8, ease: 'linear' }}
                                className="absolute bottom-0 left-0 h-1 bg-accent origin-left"
                                style={{ width: '100%' }}
                            />
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default WebSearchBanner;

