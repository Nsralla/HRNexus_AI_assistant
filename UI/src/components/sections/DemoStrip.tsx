import { TypeAnimation } from 'react-type-animation';
import { motion } from 'framer-motion';

const DemoStrip = () => {
  const questions = [
    "Who's on annual leave next week?",
    "Show me turnover rate this quarter.",
    "Find the latest salary updates.",
    "Generate a summary of HR tickets from yesterday."
  ];

  return (
    <section className="py-20 bg-gradient-to-r from-accent to-blue-600">
      <div className="container mx-auto px-6 lg:px-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-4xl mx-auto"
        >
          <h3 className="text-3xl font-bold text-white text-center mb-8">
            Try asking anything:
          </h3>

          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
            <div className="flex items-center gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                <span className="text-white text-xl">💬</span>
              </div>
              <div className="flex-grow">
                <TypeAnimation
                  sequence={[
                    questions[0],
                    2000,
                    questions[1],
                    2000,
                    questions[2],
                    2000,
                    questions[3],
                    2000,
                  ]}
                  wrapper="span"
                  speed={50}
                  className="text-white text-xl font-medium"
                  repeat={Infinity}
                />
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex-shrink-0 px-6 py-3 bg-white text-accent rounded-xl font-semibold hover:shadow-lg transition-all"
              >
                Ask
              </motion.button>
            </div>
          </div>

          <div className="mt-6 flex flex-wrap gap-3 justify-center">
            {questions.map((question, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-white text-sm border border-white/20 cursor-pointer hover:bg-white/20 transition-all"
              >
                {question}
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default DemoStrip;
