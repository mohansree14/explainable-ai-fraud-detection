import { motion } from "framer-motion";
import { Activity, TrendingUp, ShieldAlert, BadgeCheck, Search, Zap } from "lucide-react";

export default function DashboardPreview() {
  const stats = [
    { label: "Active Campaigns", value: "12", change: "+2", icon: Zap },
    { label: "Safety Score", value: "98.4%", change: "+0.5%", icon: BadgeCheck },
    { label: "Threats Blocked", value: "1,284", change: "+124", icon: ShieldAlert },
  ];

  const activities = [
    { id: 1, type: "Video Analysis", platform: "YouTube", status: "Safe", risk: "2%", time: "2m ago" },
    { id: 2, type: "Ad Placement", platform: "Instagram", status: "Flagged", risk: "64%", time: "5m ago" },
    { id: 3, type: "Comment Thread", platform: "Twitter", status: "Safe", risk: "8%", time: "12m ago" },
  ];

  return (
    <section className="py-24 px-8 bg-white overflow-hidden">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <motion.span 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            className="text-xs font-semibold text-primary uppercase tracking-wider mb-4 block"
          >
            Experience the Intelligence
          </motion.span>
          <h2 className="text-4xl font-bold text-heading mb-6">Live Intelligence Command Center</h2>
          <p className="text-muted max-w-2xl mx-auto text-lg">
            A unified view of your platform's health, safety, and performance in real time.
          </p>
        </div>

        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-navy rounded-2xl shadow-2xl overflow-hidden border border-navy/20"
        >
          {/* Dashboard Header */}
          <div className="bg-navyHover px-8 py-4 border-b border-white/5 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-red-500 shadow-lg shadow-red-500/20" />
              <span className="text-white font-medium text-sm tracking-tight">LIVE MONITORING</span>
            </div>
            <div className="hidden md:flex gap-6">
              <span className="text-white/40 text-xs">Uptime: 99.99%</span>
              <span className="text-white/40 text-xs">Latency: 24ms</span>
            </div>
          </div>

          <div className="grid lg:grid-cols-12 gap-0">
            {/* Sidebar (Desktop Only) */}
            <aside className="hidden lg:block lg:col-span-3 border-r border-white/5 p-6 bg-navy/50">
              <div className="space-y-6">
                <div className="space-y-2">
                  <p className="text-white/30 text-[10px] font-bold uppercase tracking-widest px-2">Navigation</p>
                  <nav className="space-y-1">
                    {["Overview", "Real-time Hub", "Risk Reports", "Policy Settings"].map((item, i) => (
                      <div key={i} className={`px-3 py-2 rounded-md text-sm cursor-pointer transition-colors ${i === 0 ? 'bg-primary text-white' : 'text-white/60 hover:bg-white/5 hover:text-white'}`}>
                        {item}
                      </div>
                    ))}
                  </nav>
                </div>
                <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="w-4 h-4 text-accent" />
                    <span className="text-white font-semibold text-xs">Global Risk Level</span>
                  </div>
                  <div className="text-2xl font-bold text-white">Low</div>
                  <div className="w-full bg-white/10 h-1 rounded-full mt-2 overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }}
                      whileInView={{ width: "15%" }}
                      className="h-full bg-green-500"
                    />
                  </div>
                </div>
              </div>
            </aside>

            {/* Main Content */}
            <div className="lg:col-span-9 p-8 space-y-8">
              {/* Stats Grid */}
              <div className="grid md:grid-cols-3 gap-6">
                {stats.map((stat, i) => {
                  const Icon = stat.icon;
                  return (
                    <motion.div 
                      key={i}
                      initial={{ opacity: 0, scale: 0.9 }}
                      whileInView={{ opacity: 1, scale: 1 }}
                      transition={{ delay: i * 0.1 }}
                      className="p-6 rounded-xl bg-white/5 border border-white/10"
                    >
                      <div className="flex justify-between items-start mb-4">
                        <div className="p-2 rounded-lg bg-primary/10 border border-primary/20">
                          <Icon className="w-5 h-5 text-primary" />
                        </div>
                        <span className="text-green-400 text-[10px] font-bold">{stat.change}</span>
                      </div>
                      <div className="text-white/50 text-xs mb-1">{stat.label}</div>
                      <div className="text-2xl font-bold text-white">{stat.value}</div>
                    </motion.div>
                  );
                })}
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                {/* Live Activity Feed */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-white font-bold text-sm flex items-center gap-2">
                      <Activity className="w-4 h-4 text-primary" /> Recent Activities
                    </h3>
                    <button className="text-white/40 text-[10px] hover:text-white transition-colors">VIEW ALL</button>
                  </div>
                  <div className="space-y-3">
                    {activities.map((act, i) => (
                      <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10 group hover:border-white/20 transition-colors">
                        <div className="flex items-center gap-4">
                          <div className={`w-2 h-2 rounded-full ${act.status === 'Safe' ? 'bg-green-500' : 'bg-red-500'}`} />
                          <div>
                            <div className="text-white text-sm font-medium">{act.type}</div>
                            <div className="text-white/40 text-[10px]">{act.platform}</div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className={`text-xs font-bold ${act.status === 'Safe' ? 'text-green-400' : 'text-red-400'}`}>
                            {act.status}
                          </div>
                          <div className="text-white/20 text-[10px]">{act.time}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Performance Analytics (Bars) */}
                <div className="space-y-4">
                   <div className="flex items-center justify-between">
                    <h3 className="text-white font-bold text-sm flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-primary" /> Performance Index
                    </h3>
                    <button className="text-white/40 text-[10px] hover:text-white transition-colors">EXPORT</button>
                  </div>
                  <div className="p-6 rounded-xl bg-white/5 border border-white/10 h-[210px] flex items-end justify-between gap-2">
                    {[45, 65, 40, 85, 55, 75, 90, 60].map((h, i) => (
                      <div key={i} className="flex-1 space-y-2 group">
                        <motion.div 
                          initial={{ height: 0 }}
                          whileInView={{ height: `${h}%` }}
                          transition={{ delay: i * 0.05, duration: 0.8 }}
                          className={`w-full rounded-t-sm transition-all duration-300 ${i === 6 ? 'bg-accent shadow-lg shadow-accent/20' : 'bg-primary/40 group-hover:bg-primary/60'}`}
                        />
                        <div className="text-[8px] text-white/20 text-center">M{i+1}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
        
        {/* Dashboard CTA */}
        <div className="mt-12 text-center">
          <a href="/dashboard/index.html" className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-bgSection border border-border text-heading font-medium hover:bg-white hover:shadow-md transition-all">
            Open Full Enterprise Dashboard <TrendingUp className="w-4 h-4 text-primary" />
          </a>
        </div>
      </div>
    </section>
  );
}
