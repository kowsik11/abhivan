import React from "react";
import { Card, CardContent } from "./ui/card";
import { Database, Zap, CheckCircle } from "lucide-react";

const HowItWorks = () => {
  const steps = [
    {
      number: "01",
      icon: Database,
      title: "Connect Your Data Sources",
      description: "Integrate email, calendar, calls, and CRM in minutes.",
    },
    {
      number: "02", 
      icon: Zap,
      title: "AI Agents Capture & Enrich",
      description: "Every interaction is analyzed and synced with full context.",
    },
    {
      number: "03",
      icon: CheckCircle,
      title: "Perfect CRM Hygiene",
      description: "Always complete, accurate, and up-to-date records.",
    }
  ];

  return (
    <section className="section-padding" id="product">
      <div className="container max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-4">
            How It Works
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
            Three simple steps to transform your CRM data quality forever
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 lg:gap-12">
          {steps.map((step, index) => {
            const IconComponent = step.icon;
            return (
              <div
                key={step.number}
                className="relative group"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                <Card className="hover-lift border-0 shadow-card hover:shadow-enterprise transition-all duration-300 h-full">
                  <CardContent className="p-8 text-center">
                    <div className="flex items-center justify-center w-16 h-16 bg-primary-light rounded-full mb-6 mx-auto group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300">
                      <IconComponent className="h-8 w-8 text-primary group-hover:text-primary-foreground transition-colors duration-300" />
                    </div>
                    
                    <div className="text-xs font-mono text-primary mb-2 tracking-wider">
                      STEP {step.number}
                    </div>
                    
                    <h3 className="text-xl font-bold text-foreground mb-4">
                      {step.title}
                    </h3>
                    
                    <p className="text-muted-foreground leading-relaxed">
                      {step.description}
                    </p>
                  </CardContent>
                </Card>

                {/* Connection Line */}
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 -right-6 lg:-right-12 w-12 lg:w-24 h-px bg-gradient-to-r from-primary/50 to-transparent"></div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;