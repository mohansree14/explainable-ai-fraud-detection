import { Link } from "react-router-dom";
import { FaYoutube, FaXTwitter, FaLinkedinIn } from "react-icons/fa6";

export default function Footer() {
  return (
    <footer className="bg-navy px-8 py-16 mt-20">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12 text-sm text-border">
        
        {/* Brand Section */}
        <div className="flex flex-col gap-4">
          <Link to="/" className="text-white font-serif font-bold text-xl tracking-wide">
            GUARDIAN<span className="text-primary font-sans font-semibold ml-1">AI</span>
          </Link>
          <p className="text-border/80">Real-time intelligence for critical systems.</p>
          <div className="flex gap-4 mt-2">
            <a href="#" className="w-10 h-10 rounded-md bg-navyHover border border-border/20 flex items-center justify-center hover:bg-primary transition-colors duration-300">
              <FaYoutube className="text-white text-lg" />
            </a>
            <a href="#" className="w-10 h-10 rounded-md bg-navyHover border border-border/20 flex items-center justify-center hover:bg-primary transition-colors duration-300">
              <FaXTwitter className="text-white text-lg" />
            </a>
            <a href="https://www.linkedin.com/company/guardian-aioffical/posts/?feedView=all" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-md bg-navyHover border border-border/20 flex items-center justify-center hover:bg-primary transition-colors duration-300">
              <FaLinkedinIn className="text-white text-lg" />
            </a>
          </div>
        </div>

        {/* Links */}
        <div>
          <h4 className="text-white font-semibold mb-4 font-serif">Platform</h4>
          <ul className="flex flex-col gap-3 text-border/80">
            <li><Link to="/dashboard" className="hover:text-white transition-colors duration-200">Dashboard</Link></li>
            <li><Link to="/pricing" className="hover:text-white transition-colors duration-200">Pricing</Link></li>
            <li><Link to="/integrations" className="hover:text-white transition-colors duration-200">Integrations</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-semibold mb-4 font-serif">Solutions</h4>
          <ul className="flex flex-col gap-3 text-border/80">
            <li><Link to="/solutions/enterprise" className="hover:text-white transition-colors duration-200">Enterprise</Link></li>
            <li><Link to="/solutions/startups" className="hover:text-white transition-colors duration-200">Startups</Link></li>
            <li><Link to="/solutions/communities" className="hover:text-white transition-colors duration-200">Communities</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-semibold mb-4 font-serif">Resources</h4>
          <ul className="flex flex-col gap-3 text-border/80">
            <li><Link to="/docs" className="hover:text-white transition-colors duration-200">Documentation</Link></li>
            <li><Link to="/api-docs" className="hover:text-white transition-colors duration-200">API Reference</Link></li>
            <li><Link to="/help" className="hover:text-white transition-colors duration-200">Help Center</Link></li>
          </ul>
        </div>
      </div>

      <div className="max-w-7xl mx-auto mt-16 pt-8 border-t border-border/20 flex flex-col md:flex-row justify-between items-center text-border/60 text-xs gap-4">
        <div className="flex gap-6">
          <Link to="/privacy" className="hover:text-white transition-colors duration-200">Privacy Policy</Link>
          <Link to="/terms" className="hover:text-white transition-colors duration-200">Terms & Conditions</Link>
        </div>
        <div>
          <span>© 2026 Guardian AI. All rights reserved.</span>
        </div>
        <div>
          <span>Global Operations</span>
        </div>
      </div>
    </footer>
  );
}
