import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import NexusLogo from "../shared/NexusLogo";
import { authService } from "../../../services/auth.service";

const TopNavBar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between sticky top-0 z-50 shadow-sm"
    >
      {/* Left - Logo */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3">
          <NexusLogo size={40} animate={false} />
          <div>
            <h1 className="text-xl font-bold text-primary">HR Nexus</h1>
            <p className="text-xs text-gray-500">
              Powered by LLM + RAG + LangGraph
            </p>
          </div>
        </div>
      </div>

      {/* Center - Model Selector */}
      <div className="hidden md:flex items-center gap-2">
        <motion.select
          whileHover={{ scale: 1.02 }}
          className="px-4 py-2 bg-neutral rounded-xl border border-gray-300 text-sm font-medium text-primary cursor-pointer focus:outline-none focus:ring-2 focus:ring-accent"
        >
          <option>HR Assistant – Live</option>
       
        </motion.select>
        <div className="flex items-center gap-2 px-3 py-2 bg-green-50 rounded-lg">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-xs font-medium text-green-700">Online</span>
        </div>
      </div>

      {/* Right - Actions */}
      <div className="flex items-center gap-3">

        <motion.button
          onClick={handleLogout}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          title="Logout"
          className="px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-xl font-medium text-sm transition-colors"
        >
          Logout
        </motion.button>

        {/* <motion.div
          whileHover={{ scale: 1.05 }}
          className="w-10 h-10 bg-gradient-to-br from-accent to-purple-600 rounded-full flex items-center justify-center text-white font-bold cursor-pointer"
        >
          JD
        </motion.div> */}
      </div>
    </motion.nav>
  );
};

export default TopNavBar;
