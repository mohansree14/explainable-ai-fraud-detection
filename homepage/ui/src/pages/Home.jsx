import { motion } from "framer-motion";
import { fadeUp, stagger, pageAnim } from "../animations";
import { ShieldCheck, Gavel, BarChart3, ShieldAlert, BadgeCheck, BrainCircuit } from "lucide-react";
import DashboardPreview from "../components/DashboardPreview";

export default function Home() {
  const modules = [
    { title: "Content Moderation", desc: "Ensures all user-generated content stays safe, appropriate, and platform-compliant.", icon: ShieldCheck },
    { title: "Policy Enforcement", desc: "Automatically applies and maintains rules to keep the community aligned with guidelines.", icon: Gavel },
    { title: "Research & Analytics", desc: "Provides insights into trends, risks, and user behavior for smarter decision-making.", icon: BarChart3 },
    { title: "Threat Response", desc: "Detects and responds to threats in real time to prevent crises and platform abuse.", icon: ShieldAlert },
    { title: "Ad & Brand Safety", desc: "Protects brand reputation by ensuring ads and content meet safety standards.", icon: BadgeCheck },
    { title: "AI Marketing Intelligence", desc: "Drives growth with data-driven insights, automation, and campaign optimization.", icon: BrainCircuit },
  ];

  return (
    <motion.div
      variants={pageAnim}
      initial="hidden"
      animate="show"
      exit="exit"
      className="min-h-screen pt-20"
    >
      {/* Hero Section */}
      <section className="py-24 px-6 flex flex-col justify-center items-center text-center max-w-4xl mx-auto">
        <motion.span 
          variants={fadeUp} 
          className="text-xs font-semibold text-primary uppercase tracking-wider mb-6"
        >
          Enterprise Intelligence System
        </motion.span>
        
        <motion.h1 
          variants={fadeUp} 
          className="text-5xl md:text-6xl font-bold leading-tight tracking-tight text-heading"
        >
          Real-time intelligence for critical systems.
        </motion.h1>
        
        <motion.p 
          variants={fadeUp} 
          className="text-body mt-6 text-lg max-w-2xl leading-relaxed"
        >
          Guardian AI exists to deliver intelligence organizations can trust — enabling them to protect systems, make decisions, and act in real time without compromise.
        </motion.p>
        
        <motion.div variants={fadeUp} className="mt-10 flex gap-4">
          <button className="px-8 py-3.5 rounded-md bg-navy text-white font-medium hover:bg-navyHover transition-colors duration-300 shadow-sm">
            Start Analyzing
          </button>
          <a href="/dashboard/index.html" className="px-8 py-3.5 rounded-md border border-border text-heading bg-background hover:bg-bgSection transition-colors duration-300">
            View Platform
          </a>
        </motion.div>
      </section>

      {/* Why Guardian AI Section */}
      <section className="py-24 px-8 bg-bgSection border-y border-border">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-heading">Built for Critical Environments</h2>
            <p className="text-muted mt-4 max-w-2xl mx-auto text-lg">
              Engineered to protect platforms of every size with accuracy, speed, and reliability.
            </p>
          </div>

          <motion.div 
            variants={stagger} 
            initial="hidden" 
            whileInView="show" 
            viewport={{ once: true, margin: "-100px" }} 
            className="grid md:grid-cols-2 lg:grid-cols-4 gap-8"
          >
            {[
              { t: "Real-Time Protection", d: "Instant detection and response across content, users, and emerging threats." },
              { t: "AI-Powered Intelligence", d: "Advanced adaptive models that continuously learn and evolve for higher accuracy." },
              { t: "Scalable Security", d: "Engineered to protect platforms of every size — from startups to global enterprises." },
              { t: "Multi-Platform Support", d: "Seamlessly integrates across apps, websites, and digital ecosystems for unified protection." },
            ].map((item, i) => (
              <motion.div 
                variants={fadeUp} 
                key={i} 
                className="p-8 bg-card border border-[#E2E8F0] rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300"
              >
                <h3 className="font-bold text-heading mb-3">{item.t}</h3>
                <p className="text-body leading-relaxed">{item.d}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Core Modules Section */}
      <section className="py-24 px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-heading mb-4">Comprehensive Protection Suite</h2>
            <p className="text-muted max-w-2xl mx-auto text-lg">
              Six powerful modules working together to keep the platform safe, compliant, and scalable.
            </p>
          </div>

          <motion.div 
            variants={stagger} 
            initial="hidden" 
            whileInView="show" 
            viewport={{ once: true, margin: "-100px" }} 
            className="grid md:grid-cols-3 gap-8"
          >
            {modules.map((mod, i) => {
              const Icon = mod.icon;
              return (
                <motion.div 
                  variants={fadeUp} 
                  key={i} 
                  className="p-8 bg-card border border-[#E2E8F0] rounded-xl shadow-sm hover:shadow-md transition-all duration-300 group"
                >
                  <div className="w-12 h-12 rounded-md bg-white border border-border flex items-center justify-center mb-6 shadow-sm group-hover:border-primary/50 group-hover:bg-primary/5 transition-colors">
                    <Icon className="w-6 h-6 text-primary" />
                  </div>
                  <h3 className="font-bold text-lg text-heading mb-3">{mod.title}</h3>
                  <p className="text-body leading-relaxed">{mod.desc}</p>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>
      
      {/* Dashboard Preview Section */}
      <DashboardPreview />
      
      {/* CTA Section */}
      <section className="py-24 px-6 text-center bg-bgSection border-t border-border">
        <h2 className="text-3xl font-bold text-heading mb-6">Ready for real-time intelligence?</h2>
        <button className="px-10 py-4 rounded-md bg-navy text-white font-medium hover:bg-navyHover transition-colors duration-300 shadow-sm text-lg">
          Deploy Guardian AI
        </button>
      </section>
    </motion.div>
  );
}
