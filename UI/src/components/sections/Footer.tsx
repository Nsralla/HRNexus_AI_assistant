import { motion } from 'framer-motion';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    Product: ['Features', 'Integrations', 'API Docs', 'Pricing', 'Changelog'],
    Company: ['About Us', 'Careers', 'Blog', 'Press Kit', 'Partners'],
    Security: ['Security Overview', 'Privacy Policy', 'Terms of Service', 'Compliance', 'Trust Center'],
    Contact: ['Support', 'Sales', 'Help Center', 'Community', 'Status']
  };

  return (
    <footer className="bg-primary text-white py-16">
      <div className="container mx-auto px-6 lg:px-12">
        <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-12 mb-12">
          {/* Brand Section */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-accent to-purple-600 rounded-xl flex items-center justify-center text-2xl">
                  🤖
                </div>
                <span className="text-2xl font-bold">HR AI</span>
              </div>
              <p className="text-gray-400 text-sm leading-relaxed mb-6">
                Transform your HR operations with AI-powered intelligent search and knowledge management.
              </p>
              <div className="flex gap-4">
                <SocialIcon icon="𝕏" />
                <SocialIcon icon="in" />
                <SocialIcon icon="▶" />
                <SocialIcon icon="✉" />
              </div>
            </motion.div>
          </div>

          {/* Links Sections */}
          {Object.entries(footerLinks).map(([category, links], categoryIndex) => (
            <motion.div
              key={category}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: categoryIndex * 0.1 }}
            >
              <h3 className="font-bold text-lg mb-4">{category}</h3>
              <ul className="space-y-3">
                {links.map((link, index) => (
                  <li key={index}>
                    <a
                      href="#"
                      className="text-gray-400 hover:text-accent transition-colors text-sm"
                    >
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Bottom Bar */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center gap-4"
        >
          <p className="text-gray-500 text-sm">
            © {currentYear} HR AI Assistant. All rights reserved.
          </p>
          <div className="flex gap-6 text-sm text-gray-500">
            <a href="#" className="hover:text-accent transition-colors">Privacy</a>
            <a href="#" className="hover:text-accent transition-colors">Terms</a>
            <a href="#" className="hover:text-accent transition-colors">Cookies</a>
          </div>
        </motion.div>
      </div>
    </footer>
  );
};

const SocialIcon = ({ icon }: { icon: string }) => {
  return (
    <motion.a
      href="#"
      whileHover={{ scale: 1.1, y: -2 }}
      whileTap={{ scale: 0.95 }}
      className="w-9 h-9 bg-white/10 hover:bg-accent rounded-lg flex items-center justify-center transition-colors"
    >
      <span className="font-bold">{icon}</span>
    </motion.a>
  );
};

export default Footer;
