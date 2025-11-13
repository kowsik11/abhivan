import React from "react";
import { Button } from "./ui/button-enhanced";
import { ArrowRight, Play } from "lucide-react";

const Hero = () => {
  const stats = [
    { number: "10M+", label: "Activities Captured" },
    { number: "2.5M+", label: "Records Enriched" },
    { number: "500K+", label: "Dupes Fixed" }
  ];

  return (
    <section className="relative overflow-hidden bg-gradient-hero section-padding">
      <div className="container relative z-10 max-w-7xl mx-auto text-center">
        <div className="animate-fade-up">
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight text-balance mb-6">
            <span className="text-foreground">AI that updates your CRM for you,</span>
            <br />
            <span className="text-primary">perfectly.</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto mb-12 text-balance">
            Auto-capture every email, meeting, and note — then sync clean, enriched data into your CRM.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
            <Button variant="hero" size="xl" className="group">
              Book a Demo
              <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Button>
            <Button variant="hero-outline" size="xl" className="group">
              <Play className="mr-2 h-5 w-5 transition-transform group-hover:scale-110" />
              Learn More
            </Button>
          </div>

          {/* Stats Cards */}
          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {stats.map((stat, index) => (
              <div 
                key={stat.label}
                className="bg-background/80 backdrop-blur-sm border border-border rounded-xl p-6 text-center hover-lift"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                <div className="text-3xl font-bold text-primary mb-2">
                  {stat.number}
                </div>
                <div className="text-base font-medium text-muted-foreground">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Hero Background Decoration */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-0 w-72 h-72 bg-primary/5 rounded-full blur-3xl animate-pulse-primary"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-primary/5 rounded-full blur-3xl animate-pulse-primary delay-1000"></div>
        </div>
      </div>
    </section>
  );
};

export default Hero;