import { motion } from "framer-motion";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <motion.div
      initial={{ y: -60 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="fixed top-0 w-full z-50 bg-background/90 backdrop-blur-md border-b border-border px-8 py-4 flex justify-between items-center"
    >
      <Link to="/" className="text-heading font-serif font-bold text-xl tracking-wide">
        GUARDIAN<span className="text-primary font-sans font-semibold ml-1">AI</span>
      </Link>
      
      <div className="hidden md:flex gap-8 text-muted text-sm font-medium">
        <Link to="/" className="hover:text-primary transition-colors duration-200">Platform</Link>
        <Link to="/about" className="hover:text-primary transition-colors duration-200">About</Link>
        <Link to="/team" className="hover:text-primary transition-colors duration-200">Team</Link>
        <Link to="/pricing" className="hover:text-primary transition-colors duration-200">Pricing</Link>
        <Link to="/contact" className="hover:text-primary transition-colors duration-200">Contact</Link>
      </div>

      <div className="flex gap-4 items-center">
        <Link to="/login" className="text-sm font-medium text-heading hover:text-primary transition-colors duration-200">
          Sign In
        </Link>
        <Link
          to="/dashboard"
          className="px-5 py-2.5 rounded-md text-sm bg-navy text-white font-medium hover:bg-navyHover transition-colors duration-300 shadow-sm"
        >
          Launch Platform
        </Link>
      </div>
    </motion.div>
  );
}
