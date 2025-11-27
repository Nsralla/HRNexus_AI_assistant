import { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, X, Sparkles, Users, FileText, TrendingUp } from 'lucide-react';

interface GuideCard {
  id: string;
  icon: React.ReactNode;
  title: string;
  description: string;
  prompts: string[];
}

interface GuideCardsProps {
  onSelectPrompt: (prompt: string) => void;
  onClose: () => void;
}

const GuideCards = ({ onSelectPrompt, onClose }: GuideCardsProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const cards: GuideCard[] = [
    {
      id: 'welcome',
      icon: <Sparkles className="w-8 h-8 text-primary" />,
      title: 'Welcome to HR Nexus',
      description: 'Your AI-powered HR assistant. Ask me anything about employees, policies, or HR documentation.',
      prompts: [
        'What can you help me with?',
        'Show me company policies',
        'How do I request time off?',
      ],
    },
    {
      id: 'employees',
      icon: <Users className="w-8 h-8 text-primary" />,
      title: 'Employee Information',
      description: 'Search and manage employee data, view profiles, and access organizational charts.',
      prompts: [
        'Show me all employees in Engineering',
        'Find employees with React skills',
        'Who are the managers in Sales?',
      ],
    },
    {
      id: 'documentation',
      icon: <FileText className="w-8 h-8 text-primary" />,
      title: 'HR Documentation',
      description: 'Access company policies, procedures, and HR guidelines instantly.',
      prompts: [
        'What is the remote work policy?',
        'Tell me about the code review process',
        'Explain the performance review cycle',
      ],
    },
    {
      id: 'analytics',
      icon: <TrendingUp className="w-8 h-8 text-primary" />,
      title: 'Data & Analytics',
      description: 'Query employee data and get insights about your workforce.',
      prompts: [
        'How many employees do we have?',
        'Show me the department distribution',
        'What are the most common skills?',
      ],
    },
  ];

  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % cards.length);
  };

  const handlePrev = () => {
    setCurrentIndex((prev) => (prev - 1 + cards.length) % cards.length);
  };

  const handlePromptClick = (prompt: string) => {
    onSelectPrompt(prompt);
    onClose();
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'ArrowLeft') {
        handlePrev();
      } else if (event.key === 'ArrowRight') {
        handleNext();
      } else if (event.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentIndex]); // eslint-disable-line react-hooks/exhaustive-deps

  const currentCard = cards[currentIndex];

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-200px)] p-6">
      <div className="relative max-w-2xl w-full">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute -top-4 -right-4 z-10 p-2 bg-white rounded-full shadow-lg hover:shadow-xl transition-shadow border border-gray-200 hover:border-gray-300"
          aria-label="Close guide"
        >
          <X className="w-5 h-5 text-gray-600" />
        </button>

        {/* Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
          {/* Card Content */}
          <div className="p-8 min-h-[400px] flex flex-col">
            {/* Icon */}
            <div className="flex justify-center mb-6">
              <div className="p-4 bg-primary/10 rounded-2xl">
                {currentCard.icon}
              </div>
            </div>

            {/* Title */}
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-4">
              {currentCard.title}
            </h2>

            {/* Description */}
            <p className="text-gray-600 text-center mb-8 text-lg">
              {currentCard.description}
            </p>

            {/* Suggested Prompts */}
            <div className="flex-grow">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">
                Try asking:
              </h3>
              <div className="space-y-3">
                {currentCard.prompts.map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => handlePromptClick(prompt)}
                    className="w-full text-left px-4 py-3 bg-gray-50 hover:bg-primary/5 rounded-lg transition-colors border border-gray-200 hover:border-primary/30 group"
                  >
                    <span className="text-gray-700 group-hover:text-primary transition-colors">
                      {prompt}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Navigation */}
          <div className="bg-gray-50 px-8 py-6 flex items-center justify-between border-t border-gray-200">
            {/* Previous Button */}
            <button
              onClick={handlePrev}
              className="p-2 rounded-full hover:bg-white transition-colors border border-transparent hover:border-gray-200 hover:shadow-sm"
              aria-label="Previous card"
            >
              <ChevronLeft className="w-6 h-6 text-gray-600" />
            </button>

            {/* Dots Indicator */}
            <div className="flex gap-2">
              {cards.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentIndex(index)}
                  className={`h-2 rounded-full transition-all ${
                    index === currentIndex
                      ? 'w-8 bg-primary'
                      : 'w-2 bg-gray-300 hover:bg-gray-400'
                  }`}
                  aria-label={`Go to card ${index + 1}`}
                />
              ))}
            </div>

            {/* Next Button */}
            <button
              onClick={handleNext}
              className="p-2 rounded-full hover:bg-white transition-colors border border-transparent hover:border-gray-200 hover:shadow-sm"
              aria-label="Next card"
            >
              <ChevronRight className="w-6 h-6 text-gray-600" />
            </button>
          </div>
        </div>

        {/* Hint Text */}
        <div className="text-center mt-6">
          <p className="text-sm text-gray-500">
            Use arrow keys or swipe to navigate • Click any suggestion to start
          </p>
        </div>
      </div>
    </div>
  );
};

export default GuideCards;
