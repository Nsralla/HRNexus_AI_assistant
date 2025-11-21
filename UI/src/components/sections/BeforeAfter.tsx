import { motion } from 'framer-motion';

const BeforeAfter = () => {
  const beforeItems = [
    'Flipping through folders',
    'Searching spreadsheets',
    'Asking colleagues',
    'Slow onboarding & resolution'
  ];

  const afterItems = [
    'Ask natural questions',
    'Instant answers',
    'AI-powered search',
    '24/7 availability'
  ];

  return (
    <section className="py-24 bg-white">
      <div className="container mx-auto px-6 lg:px-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-5xl font-extrabold text-primary mb-4">
            Transform Your HR Workflow
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            From hours of manual searching to instant AI-powered answers
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Before Card */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="bg-gray-100 rounded-2xl p-8 relative overflow-hidden"
          >
            <div className="absolute top-4 right-4 text-6xl opacity-10">⏱️</div>
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center text-2xl">
                  😓
                </div>
                <h3 className="text-2xl font-bold text-gray-700">Before</h3>
              </div>
              <ul className="space-y-4">
                {beforeItems.map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="text-red-500 mt-1">✗</span>
                    <span className="text-gray-600 text-lg">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>

          {/* After Card */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            whileHover={{ y: -5 }}
            className="bg-gradient-to-br from-accent to-blue-600 rounded-2xl p-8 relative overflow-hidden shadow-hover"
          >
            <div className="absolute top-4 right-4 text-6xl opacity-20">⚡</div>
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
                  🚀
                </div>
                <h3 className="text-2xl font-bold text-white">After</h3>
              </div>
              <ul className="space-y-4">
                {afterItems.map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="text-green-300 mt-1">✓</span>
                    <span className="text-white text-lg">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default BeforeAfter;
