import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const FinalCTA = () => {
  const navigate = useNavigate();
  return (
    <section className="py-24 bg-neutral relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-accent/30 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-400/30 rounded-full blur-3xl" />
      </div>

      {/* Mesh Grid Pattern */}
      <div
        className="absolute inset-0 opacity-5"
        style={{
          backgroundImage: `
            linear-gradient(to right, #4A7DFF 1px, transparent 1px),
            linear-gradient(to bottom, #4A7DFF 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px'
        }}
      />

      <div className="container mx-auto px-6 lg:px-12 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto"
        >
          <div className="bg-gradient-to-br from-primary via-gray-900 to-accent rounded-3xl p-12 md:p-16 shadow-2xl text-center relative overflow-hidden">
            {/* Glow Effect */}
            <div className="absolute inset-0 bg-gradient-to-br from-accent/20 to-purple-600/20 blur-2xl" />

            <div className="relative z-10">
              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="inline-block mb-6"
              >
                <div className="w-20 h-20 mx-auto bg-white/10 backdrop-blur-sm rounded-2xl flex items-center justify-center text-5xl">
                  🚀
                </div>
              </motion.div>

              <h2 className="text-4xl md:text-6xl font-extrabold text-white mb-6 leading-tight">
                Ready to upgrade your HR team with AI?
              </h2>

              <p className="text-xl md:text-2xl text-gray-200 mb-10 max-w-2xl mx-auto leading-relaxed">
                Let your company's knowledge become searchable in seconds.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <motion.button
                  whileHover={{ scale: 1.05, boxShadow: '0 0 30px rgba(74, 125, 255, 0.5)' }}
                  whileTap={{ scale: 0.95 }}
                  className="px-10 py-5 bg-white text-primary rounded-2xl font-bold text-lg shadow-2xl hover:shadow-accent/50 transition-all"
                  onClick={()=> navigate("/login")}
                >
                  Get Started Free
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-10 py-5 bg-white/10 backdrop-blur-sm border-2 border-white/30 text-white rounded-2xl font-bold text-lg hover:bg-white/20 transition-all"
                >
                  Schedule a Demo
                </motion.button>
              </div>

              <p className="text-gray-300 text-sm mt-8">
                No credit card required • 14-day free trial • Cancel anytime
              </p>
            </div>
          </div>

          {/* Trust Badges */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex flex-wrap justify-center gap-8 mt-12 text-gray-600"
          >
            <div className="flex items-center gap-2">
              <span className="text-green-500 text-xl">✓</span>
              <span>SOC2 Compliant</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500 text-xl">✓</span>
              <span>GDPR Ready</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500 text-xl">✓</span>
              <span>256-bit Encryption</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500 text-xl">✓</span>
              <span>24/7 Support</span>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
};

export default FinalCTA;
