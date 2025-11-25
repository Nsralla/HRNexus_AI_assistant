import { motion } from 'framer-motion';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import NexusLogo from '../components/shared/NexusLogo';
import { authService } from '../../services/auth.service';

const SignupPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    company_id: '464d373e-4594-4d08-b8dd-c827809ff41c'
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate password match
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    // Validate password length
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setIsLoading(true);

    try {
      await authService.register({
        email: formData.email,
        password: formData.password,
        full_name: formData.full_name,
        company_id: formData.company_id
      });
      navigate('/chat');
    } catch (err) {
      // Extract meaningful error message from the backend
      let errorMessage = 'Registration failed. Please try again.';

      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'object' && err !== null && 'detail' in err) {
        errorMessage = String((err as any).detail);
      }

      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
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
            Join us today and experience the future of HR management with AI-powered assistance.
          </motion.p>

          {/* Floating Illustrations */}
          <div className="mt-16 relative w-full max-w-md h-40">
            <motion.div
              animate={{ y: [0, -10, 0], rotate: [0, 5, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              className="absolute top-0 left-12 w-16 h-16 bg-white/50 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-lg"
            >
              <span className="text-3xl">🚀</span>
            </motion.div>

            <motion.div
              animate={{ y: [0, -15, 0], rotate: [0, -5, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
              className="absolute top-8 right-12 w-16 h-16 bg-white/50 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-lg"
            >
              <span className="text-3xl">✨</span>
            </motion.div>

            <motion.div
              animate={{ y: [0, -12, 0], rotate: [0, 3, 0] }}
              transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut", delay: 1 }}
              className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-16 h-16 bg-white/50 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-lg"
            >
              <span className="text-3xl">👥</span>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Right Side - Signup Card */}
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

          {/* Signup Card */}
          <div className="bg-white rounded-3xl p-12 shadow-soft border border-gray-200 relative overflow-hidden">
            {/* Glass Reflection */}
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-white to-transparent opacity-50" />

            {/* Title */}
            <div className="mb-8">
              <h2 className="text-3xl font-bold text-primary mb-2">Create Account</h2>
              <p className="text-gray-600">Get started with your HR AI assistant.</p>
              <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg px-4 py-3">
                <p className="text-xs text-blue-700">
                  <span className="font-semibold">Note:</span> If you don't have a valid company ID, please don't edit the default one.
                </p>
              </div>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Error Message */}
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm"
                >
                  {error}
                </motion.div>
              )}

              {/* Full Name Input */}
              <div>
                <label htmlFor="full_name" className="block text-sm font-semibold text-gray-700 mb-2">
                  Full Name
                </label>
                <input
                  id="full_name"
                  name="full_name"
                  type="text"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="John Doe"
                  required
                  className="w-full px-4 py-3 bg-neutral rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all"
                />
              </div>

              {/* Email Input */}
              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
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
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  required
                  minLength={8}
                  className="w-full px-4 py-3 bg-neutral rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all"
                />
                <p className="mt-1 text-xs text-gray-500">Must be at least 8 characters</p>
              </div>

              {/* Confirm Password Input */}
              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-semibold text-gray-700 mb-2">
                  Confirm Password
                </label>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="••••••••"
                  required
                  minLength={8}
                  className="w-full px-4 py-3 bg-neutral rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all"
                />
              </div>

              {/* Company ID Input */}
              <div>
                <label htmlFor="company_id" className="block text-sm font-semibold text-gray-700 mb-2">
                  Company ID
                </label>
                <input
                  id="company_id"
                  name="company_id"
                  type="text"
                  value={formData.company_id}
                  onChange={handleChange}
                  placeholder="Company ID"
                  required
                  className="w-full px-4 py-3 bg-neutral rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all font-mono text-sm"
                />
                <p className="mt-1 text-xs text-gray-500">Default company ID is pre-filled</p>
              </div>

              {/* Sign Up Button */}
              <motion.button
                type="submit"
                disabled={isLoading}
                whileHover={{ scale: isLoading ? 1 : 1.02, boxShadow: isLoading ? undefined : '0 10px 40px rgba(74, 125, 255, 0.3)' }}
                whileTap={{ scale: isLoading ? 1 : 0.98 }}
                className={`w-full py-4 bg-gradient-to-r from-accent to-blue-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all ${
                  isLoading ? 'opacity-70 cursor-not-allowed' : ''
                }`}
              >
                {isLoading ? (
                  <div className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Creating account...
                  </div>
                ) : (
                  'Create Account'
                )}
              </motion.button>

              {/* Terms and Privacy */}
              <p className="text-xs text-gray-500 text-center">
                By signing up, you agree to our{' '}
                <a href="#" className="text-accent hover:underline">Terms of Service</a>
                {' '}and{' '}
                <a href="#" className="text-accent hover:underline">Privacy Policy</a>
              </p>
            </form>

            {/* Bottom Text */}
            <p className="text-center text-sm text-gray-600 mt-8">
              Already have an account?{' '}
              <a href="/login" className="text-accent font-semibold hover:underline">
                Sign in
              </a>
            </p>
          </div>

          {/* Company ID Info */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="mt-4 bg-gray-50 border border-gray-200 rounded-lg px-4 py-3"
          >
            <p className="text-xs text-gray-600 text-center">
              Want to register with your own company ID?{' '}
              <span className="text-accent font-semibold">Contact the admins</span>
            </p>
          </motion.div>

          {/* Security Badge */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 1 }}
            className="mt-4 flex items-center justify-center gap-2 text-sm text-gray-500"
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

export default SignupPage;
