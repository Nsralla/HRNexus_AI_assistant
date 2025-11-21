import { motion } from 'framer-motion';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import NexusLogo from '../components/shared/NexusLogo';

const LoginPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle login logic here
    console.log('Login:', { email, password, rememberMe });
    // For demo, navigate to chat
    navigate('/chat');
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Branding Panel */}
      <motion.div
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
        className="hidden lg:flex lg:w-1/2 relative overflow-hidden"
        style={{
          background: 'linear-gradient(135deg, #EEF3FF 0%, #DDE7FF 50%, #F7FAFF 100%)'
        }}
      >
        {/* Decorative Elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-accent/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-400/10 rounded-full blur-3xl" />

        {/* Geometric Pattern */}
        <div
          className="absolute inset-0 opacity-5"
          style={{
            backgroundImage: `
              linear-gradient(45deg, #4A7DFF 25%, transparent 25%),
              linear-gradient(-45deg, #4A7DFF 25%, transparent 25%),
              linear-gradient(45deg, transparent 75%, #4A7DFF 75%),
              linear-gradient(-45deg, transparent 75%, #4A7DFF 75%)
            `,
            backgroundSize: '60px 60px',
            backgroundPosition: '0 0, 0 30px, 30px -30px, -30px 0px'
          }}
        />

        {/* Content */}
        <div className="relative z-10 flex flex-col items-center justify-center w-full px-12">
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="mb-8"
          >
            <NexusLogo size={120} animate={true} />
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="text-5xl font-extrabold text-primary mb-4 text-center"
          >
            HR Nexus
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="text-xl text-gray-600 text-center max-w-md leading-relaxed"
          >
            Your HR assistant. One chat to all your company knowledge.
          </motion.p>

          {/* Floating Illustrations */}
          <div className="mt-16 relative w-full max-w-md h-40">
            <motion.div
              animate={{ y: [0, -10, 0], rotate: [0, 5, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              className="absolute top-0 left-12 w-16 h-16 bg-white/50 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-lg"
            >
              <span className="text-3xl">💬</span>
            </motion.div>

            <motion.div
              animate={{ y: [0, -15, 0], rotate: [0, -5, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
              className="absolute top-8 right-12 w-16 h-16 bg-white/50 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-lg"
            >
              <span className="text-3xl">🧠</span>
            </motion.div>

            <motion.div
              animate={{ y: [0, -12, 0], rotate: [0, 3, 0] }}
              transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut", delay: 1 }}
              className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-16 h-16 bg-white/50 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-lg"
            >
              <span className="text-3xl">📁</span>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Right Side - Login Card */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-neutral">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="w-full max-w-md"
        >
          {/* Mobile Logo */}
          <div className="lg:hidden flex flex-col items-center mb-8">
            <NexusLogo size={80} animate={false} />
            <h1 className="text-3xl font-bold text-primary mt-4">HR Nexus</h1>
          </div>

          {/* Login Card */}
          <div className="bg-white rounded-3xl p-12 shadow-soft border border-gray-200 relative overflow-hidden">
            {/* Glass Reflection */}
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-white to-transparent opacity-50" />

            {/* Title */}
            <div className="mb-8">
              <h2 className="text-3xl font-bold text-primary mb-2">Welcome Back</h2>
              <p className="text-gray-600">Sign in to access your HR AI assistant.</p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Email Input */}
              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  required
                  className="w-full px-4 py-3 bg-neutral rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all"
                />
              </div>

              {/* Password Input */}
              <div>
                <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="w-full px-4 py-3 bg-neutral rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all"
                />
              </div>

              {/* Remember Me & Forgot Password */}
              <div className="flex items-center justify-between">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-4 h-4 text-accent border-gray-300 rounded focus:ring-accent"
                  />
                  <span className="ml-2 text-sm text-gray-700">Remember me</span>
                </label>
                <a href="#" className="text-sm text-accent hover:text-blue-600 font-medium">
                  Forgot password?
                </a>
              </div>

              {/* Login Button */}
              <motion.button
                type="submit"
                whileHover={{ scale: 1.02, boxShadow: '0 10px 40px rgba(74, 125, 255, 0.3)' }}
                whileTap={{ scale: 0.98 }}
                className="w-full py-4 bg-gradient-to-r from-accent to-blue-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all"
              >
                Sign In
              </motion.button>

              {/* Divider */}
              <div className="relative my-6">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-4 bg-white text-gray-500">OR</span>
                </div>
              </div>

              {/* SSO Buttons */}
              <div className="space-y-3">
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full py-3 bg-white border-2 border-gray-300 rounded-xl font-semibold text-gray-700 hover:border-gray-400 transition-all flex items-center justify-center gap-3"
                >
                  <svg className="w-5 h-5" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                  Sign in with Google
                </motion.button>

                <motion.button
                  type="button"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full py-3 bg-white border-2 border-gray-300 rounded-xl font-semibold text-gray-700 hover:border-gray-400 transition-all flex items-center justify-center gap-3"
                >
                  <svg className="w-5 h-5" viewBox="0 0 23 23" fill="none">
                    <path d="M11.5 0C5.149 0 0 5.149 0 11.5S5.149 23 11.5 23 23 17.851 23 11.5 17.851 0 11.5 0zm5.08 15.914c-.353.293-.794.439-1.322.439-.646 0-1.205-.264-1.676-.793l-2.582-2.905-2.582 2.905c-.47.529-1.03.793-1.676.793-.528 0-.969-.146-1.322-.439-.353-.293-.529-.675-.529-1.147 0-.557.234-1.055.703-1.495l2.67-2.994-2.67-2.994c-.469-.44-.703-.938-.703-1.495 0-.472.176-.854.529-1.147.353-.293.794-.439 1.322-.439.646 0 1.205.264 1.676.793l2.582 2.905 2.582-2.905c.47-.529 1.03-.793 1.676-.793.528 0 .969.146 1.322.439.353.293.529.675.529 1.147 0 .557-.234 1.055-.703 1.495l-2.67 2.994 2.67 2.994c.469.44.703.938.703 1.495 0 .472-.176.854-.529 1.147z" fill="#00A4EF"/>
                  </svg>
                  Sign in with Microsoft
                </motion.button>
              </div>
            </form>

            {/* Bottom Text */}
            <p className="text-center text-sm text-gray-600 mt-8">
              Don't have an account?{' '}
              <span className="text-accent font-semibold">Contact your HR admin</span>
            </p>
          </div>

          {/* Security Badge */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 1 }}
            className="mt-6 flex items-center justify-center gap-2 text-sm text-gray-500"
          >
            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>Enterprise-grade encryption</span>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default LoginPage;
