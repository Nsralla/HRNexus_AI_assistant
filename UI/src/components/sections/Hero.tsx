import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Hero = () => {
  const navigate = useNavigate();
  const [chatMessages, setChatMessages] = useState<Array<{ type: 'user' | 'ai'; text: string }>>([]);
  const [currentStep, setCurrentStep] = useState(0);

  const demoSequence = [
    { type: 'user' as const, text: 'Find me all employees in Engineering hired after 2020' },
    {
      type: 'ai' as const,
      text: 'Found 12 employees matching your criteria. Here\'s a summary:'
    }
  ];

  useEffect(() => {
    const timer = setTimeout(() => {
      if (currentStep < demoSequence.length) {
        setChatMessages(prev => [...prev, demoSequence[currentStep]]);
        setCurrentStep(currentStep + 1);
      } else {
        // Reset after showing all messages
        setTimeout(() => {
          setChatMessages([]);
          setCurrentStep(0);
        }, 3000);
      }
    }, currentStep === 0 ? 1000 : 2000);

    return () => clearTimeout(timer);
  }, [currentStep]);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-neutral via-white to-blue-50">
      {/* Background Gradient Orbs */}
      <div className="absolute top-20 left-10 w-96 h-96 bg-accent/20 rounded-full blur-3xl" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl" />

      <div className="container mx-auto px-6 lg:px-12 py-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-16 items-center">

          {/* Left Side - Content */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-6xl lg:text-7xl font-extrabold leading-tight mb-6 text-primary">
              Meet Your AI-Powered HR Assistant
            </h1>
            <p className="text-2xl text-gray-600 mb-4 leading-relaxed">
              The fastest way to find answers across your company data.
            </p>
            <p className="text-lg text-gray-500 mb-10 leading-relaxed max-w-xl">
              Let employees and HR teams instantly retrieve policies, employee details, org charts,
              Jira tickets, records, and reports — powered by LLMs, RAG, and LangGraph.
            </p>

            <div className="flex gap-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/login')}
                className="px-8 py-4 bg-accent text-white rounded-2xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
              >
                Get Started
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 border-2 border-gray-300 text-primary rounded-2xl font-semibold text-lg hover:border-accent transition-all"
              >
                Watch How It Works
              </motion.button>
            </div>
          </motion.div>

          {/* Right Side - Animated Chat Demo */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            <div className="bg-white rounded-2xl shadow-soft p-6 max-w-lg mx-auto">
              <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-200">
                <div className="w-3 h-3 rounded-full bg-red-400" />
                <div className="w-3 h-3 rounded-full bg-yellow-400" />
                <div className="w-3 h-3 rounded-full bg-green-400" />
                <span className="ml-auto text-sm text-gray-500 font-medium">HR AI Assistant</span>
              </div>

              <div className="space-y-4 min-h-[300px]">
                {chatMessages.map((message, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs px-5 py-3 rounded-2xl ${
                        message.type === 'user'
                          ? 'bg-accent text-white rounded-br-md'
                          : 'bg-gray-100 text-gray-800 rounded-bl-md'
                      }`}
                    >
                      <p className="text-sm leading-relaxed">{message.text}</p>
                      {message.type === 'ai' && index === chatMessages.length - 1 && (
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.5 }}
                          className="mt-3 p-3 bg-white rounded-xl shadow-sm border border-gray-200"
                        >
                          <div className="flex items-center justify-between text-xs text-gray-600 mb-2">
                            <span className="font-semibold">Engineering</span>
                            <span>12 employees</span>
                          </div>
                          <div className="flex -space-x-2">
                            {[...Array(4)].map((_, i) => (
                              <div
                                key={i}
                                className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 border-2 border-white"
                              />
                            ))}
                            <div className="w-7 h-7 rounded-full bg-gray-200 border-2 border-white flex items-center justify-center text-xs font-medium">
                              +8
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </div>
                  </motion.div>
                ))}

                {chatMessages.length === 0 && (
                  <div className="flex items-center justify-center h-64 text-gray-400">
                    <p>Waiting for query...</p>
                  </div>
                )}
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
};

export default Hero;
