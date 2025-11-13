import React from "react";
import { Button } from "./ui/button-enhanced";
import { ArrowRight, CheckCircle } from "lucide-react";

const FinalCTA = () => {
  return (
    <section className="section-padding bg-gradient-hero">
      <div className="container max-w-7xl mx-auto text-center">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6">
            Ready to automate your CRM?
          </h2>
          
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 text-balance">
            Save hours every week with perfect CRM hygiene
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Button variant="cta" size="xl" className="group">
              Book a Demo
              <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Button>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-success" />
              <span>Free setup & training</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-success" />
              <span>14-day trial</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-success" />
              <span>No long-term commitment</span>
            </div>
          </div>
        </div>
        
        {/* Background Decoration */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute top-0 left-1/4 w-64 h-64 bg-primary/10 rounded-full blur-3xl animate-pulse-primary"></div>
          <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-primary/10 rounded-full blur-3xl animate-pulse-primary delay-1000"></div>
        </div>
      </div>
    </section>
  );
};

export default FinalCTA;