import React from "react";

const SocialProof = () => {
  const logos = [
    "Onyx", "Fern", "Cartage", "Zentura", "Axiom", "Pulse"
  ];

  return (
    <section className="section-padding bg-muted/20 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, hsl(var(--primary)) 1px, transparent 0)`,
          backgroundSize: '24px 24px'
        }} />
      </div>
      
      <div className="container max-w-7xl mx-auto text-center relative">
        <div className="mb-12">
          <p className="text-lg text-muted-foreground mb-8 font-medium">
            Trusted by leading teams and backed by industry leaders
          </p>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-6 gap-6">
          {logos.map((logo, index) => (
            <div 
              key={logo}
              className="group relative"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              <div className="bg-background/80 backdrop-blur-sm border border-border/50 rounded-xl p-6 h-20 flex items-center justify-center shadow-sm hover:shadow-md hover:border-primary/30 transition-all duration-300 hover:scale-105 hover:bg-background animate-fade-up">
                <div className="text-xl font-bold text-muted-foreground group-hover:text-foreground transition-colors duration-300">
                  {logo}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default SocialProof;