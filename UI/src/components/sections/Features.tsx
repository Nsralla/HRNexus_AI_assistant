import { motion } from 'framer-motion';

const Features = () => {
  const features = [
    {
      icon: '🔍',
      title: 'Retrieve Any Data Instantly',
      description: 'Employees, schedules, payroll details, policies, contracts, org charts.',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: '🧠',
      title: 'RAG + LangGraph Engine',
      description: 'Built with a controllable graph workflow for guaranteed accuracy.',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: '💬',
      title: 'Context-Aware Answers',
      description: 'Structured, summarized, and cross-referenced responses.',
      gradient: 'from-orange-500 to-red-500'
    },
    {
      icon: '🔐',
      title: 'Enterprise-Grade Security',
      description: 'SOC2-ready, fully encrypted, zero training data leakage.',
      gradient: 'from-green-500 to-emerald-500'
    }
  ];

  return (
    <section className="py-24 bg-neutral">
      <div className="container mx-auto px-6 lg:px-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-5xl font-extrabold text-primary mb-4">
            Powerful Features
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Everything you need to transform your HR operations
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ y: -8, transition: { duration: 0.3 } }}
              className="bg-white rounded-2xl p-6 shadow-soft hover:shadow-hover transition-all"
            >
              <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center text-3xl mb-4`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-primary mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
