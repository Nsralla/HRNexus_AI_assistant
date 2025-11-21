import { motion } from 'framer-motion';

const HowItWorks = () => {
  const steps = [
    {
      number: '01',
      title: 'Connect Your Data',
      description: 'Employee DB, Jira, Confluence, internal HR systems.',
      icon: '🔗',
      items: ['Employee Databases', 'Jira & Confluence', 'HR Management Systems', 'Custom Data Sources']
    },
    {
      number: '02',
      title: 'We Index & Build the Knowledge Graph',
      description: 'RAG pipeline + embeddings + LangGraph agent flows.',
      icon: '🧩',
      items: ['Vector Embeddings', 'Knowledge Graph', 'RAG Pipeline', 'LangGraph Agents']
    },
    {
      number: '03',
      title: 'Ask Anything',
      description: 'Instant answers via web, Slack, Teams, or API.',
      icon: '💡',
      items: ['Web Interface', 'Slack Integration', 'Teams Integration', 'REST API']
    }
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
            How It Works
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Three simple steps to transform your HR knowledge management
          </p>
        </motion.div>

        <div className="relative max-w-6xl mx-auto">
          {/* Connection Lines */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-accent via-purple-500 to-green-500 -z-10"
               style={{ transform: 'translateY(-50%)' }}
          />

          <div className="grid lg:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="relative"
              >
                {/* Step Card */}
                <div className="bg-neutral rounded-2xl p-8 shadow-soft hover:shadow-hover transition-all h-full">
                  {/* Step Number Badge */}
                  <div className="absolute -top-4 -left-4 w-16 h-16 bg-gradient-to-br from-accent to-purple-600 rounded-2xl flex items-center justify-center text-white font-bold text-xl shadow-lg">
                    {step.number}
                  </div>

                  {/* Icon */}
                  <div className="text-6xl mb-6 mt-4 text-center">
                    {step.icon}
                  </div>

                  {/* Title */}
                  <h3 className="text-2xl font-bold text-primary mb-3 text-center">
                    {step.title}
                  </h3>

                  {/* Description */}
                  <p className="text-gray-600 mb-6 text-center leading-relaxed">
                    {step.description}
                  </p>

                  {/* Items List */}
                  <ul className="space-y-2">
                    {step.items.map((item, itemIndex) => (
                      <li key={itemIndex} className="flex items-center gap-2 text-sm text-gray-600">
                        <span className="w-1.5 h-1.5 bg-accent rounded-full" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Arrow for mobile */}
                {index < steps.length - 1 && (
                  <div className="lg:hidden flex justify-center my-4">
                    <div className="text-accent text-3xl">↓</div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
