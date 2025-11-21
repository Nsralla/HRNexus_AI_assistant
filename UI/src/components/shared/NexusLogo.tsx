import { motion } from 'framer-motion';

interface NexusLogoProps {
  size?: number;
  animate?: boolean;
  className?: string;
}

const NexusLogo = ({ size = 40, animate = false, className = '' }: NexusLogoProps) => {
  return (
    <motion.svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      initial={animate ? { scale: 0, rotate: -180 } : undefined}
      animate={animate ? { scale: 1, rotate: 0 } : undefined}
      transition={animate ? { duration: 0.8, ease: "easeOut" } : undefined}
    >
      {/* Background Circle with Gradient */}
      <defs>
        <linearGradient id="nexusGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#4A7DFF" />
          <stop offset="100%" stopColor="#6B5FED" />
        </linearGradient>

        <linearGradient id="nodeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#FFFFFF" />
          <stop offset="100%" stopColor="#E0E7FF" />
        </linearGradient>

        {/* Glow Filter */}
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>

      {/* Main Background Circle */}
      <circle
        cx="50"
        cy="50"
        r="45"
        fill="url(#nexusGradient)"
        opacity="0.95"
      />

      {/* Connection Lines forming "N" shape */}
      <g opacity="0.6" strokeWidth="2.5" stroke="#FFFFFF" strokeLinecap="round">
        {/* Left vertical line */}
        <motion.line
          x1="30"
          y1="30"
          x2="30"
          y2="70"
          initial={animate ? { pathLength: 0 } : undefined}
          animate={animate ? { pathLength: 1 } : undefined}
          transition={animate ? { duration: 0.5, delay: 0.3 } : undefined}
        />

        {/* Diagonal line */}
        <motion.line
          x1="30"
          y1="30"
          x2="70"
          y2="70"
          initial={animate ? { pathLength: 0 } : undefined}
          animate={animate ? { pathLength: 1 } : undefined}
          transition={animate ? { duration: 0.6, delay: 0.5 } : undefined}
        />

        {/* Right vertical line */}
        <motion.line
          x1="70"
          y1="30"
          x2="70"
          y2="70"
          initial={animate ? { pathLength: 0 } : undefined}
          animate={animate ? { pathLength: 1 } : undefined}
          transition={animate ? { duration: 0.5, delay: 0.7 } : undefined}
        />
      </g>

      {/* Network Nodes */}
      {/* Top Left Node */}
      <motion.circle
        cx="30"
        cy="30"
        r="6"
        fill="url(#nodeGradient)"
        filter="url(#glow)"
        initial={animate ? { scale: 0 } : undefined}
        animate={animate ? { scale: 1 } : undefined}
        transition={animate ? { duration: 0.3, delay: 0.9 } : undefined}
      />
      <circle cx="30" cy="30" r="3" fill="#4A7DFF" />

      {/* Bottom Left Node */}
      <motion.circle
        cx="30"
        cy="70"
        r="6"
        fill="url(#nodeGradient)"
        filter="url(#glow)"
        initial={animate ? { scale: 0 } : undefined}
        animate={animate ? { scale: 1 } : undefined}
        transition={animate ? { duration: 0.3, delay: 1.0 } : undefined}
      />
      <circle cx="30" cy="70" r="3" fill="#4A7DFF" />

      {/* Top Right Node */}
      <motion.circle
        cx="70"
        cy="30"
        r="6"
        fill="url(#nodeGradient)"
        filter="url(#glow)"
        initial={animate ? { scale: 0 } : undefined}
        animate={animate ? { scale: 1 } : undefined}
        transition={animate ? { duration: 0.3, delay: 1.1 } : undefined}
      />
      <circle cx="70" cy="30" r="3" fill="#4A7DFF" />

      {/* Bottom Right Node */}
      <motion.circle
        cx="70"
        cy="70"
        r="6"
        fill="url(#nodeGradient)"
        filter="url(#glow)"
        initial={animate ? { scale: 0 } : undefined}
        animate={animate ? { scale: 1 } : undefined}
        transition={animate ? { duration: 0.3, delay: 1.2 } : undefined}
      />
      <circle cx="70" cy="70" r="3" fill="#4A7DFF" />

      {/* Center Connection Node */}
      <motion.circle
        cx="50"
        cy="50"
        r="5"
        fill="#FFFFFF"
        opacity="0.9"
        initial={animate ? { scale: 0 } : undefined}
        animate={animate ? { scale: 1 } : undefined}
        transition={animate ? { duration: 0.3, delay: 1.3 } : undefined}
      />
      <circle cx="50" cy="50" r="2" fill="#4A7DFF" />
    </motion.svg>
  );
};

export default NexusLogo;
