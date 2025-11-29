import { motion } from 'framer-motion';
import { useState } from 'react';

const Integrations = () => {
  const integrations = [
    { name: 'Jira', color: '#0052CC' },
    { name: 'Confluence', color: '#172B4D' },
    { name: 'Workday', color: '#EC5E2A' },
    { name: 'BambooHR', color: '#73C41D' },
    { name: 'Slack', color: '#4A154B' },
    { name: 'Teams', color: '#6264A7' },
    { name: 'PostgreSQL', color: '#336791' },
    { name: 'SQL Server', color: '#CC2927' },
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
            Seamless Integrations
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Connect with the tools you already use
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-5xl mx-auto">
          {integrations.map((integration, index) => (
            <IntegrationCard
              key={index}
              name={integration.name}
              color={integration.color}
              index={index}
            />
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="text-center mt-12"
        >
          <p className="text-gray-600 mb-4">And many more...</p>
          
        </motion.div>
      </div>
    </section>
  );
};

const IntegrationCard = ({ name, color, index }: { name: string; color: string; index: number }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
      whileHover={{ y: -5, scale: 1.05 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className="bg-white rounded-2xl p-8 shadow-soft hover:shadow-hover transition-all cursor-pointer flex items-center justify-center"
    >
      <div className="text-center">
        <div
          className="w-16 h-16 mx-auto mb-3 rounded-xl flex items-center justify-center text-2xl font-bold text-white transition-all"
          style={{
            backgroundColor: isHovered ? color : '#9CA3AF',
            transition: 'background-color 0.3s ease'
          }}
        >
          {name.substring(0, 2).toUpperCase()}
        </div>
        <p className="font-semibold text-primary">{name}</p>
      </div>
    </motion.div>
  );
};

export default Integrations;
