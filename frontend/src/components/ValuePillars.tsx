import React from "react";
import { Card, CardContent } from "./ui/card";
import { Target, Sparkles, RefreshCw, Shield } from "lucide-react";

const ValuePillars = () => {
  const pillars = [
    {
      icon: Target,
      title: "Capture",
      description: "Auto-capture every touchpoint",
      details: "Never miss an important interaction. Our AI automatically captures emails, calls, meetings, and notes from all your communication channels."
    },
    {
      icon: Sparkles,
      title: "Clean", 
      description: "Remove duplicates & enrich contacts",
      details: "AI-powered data cleansing removes duplicates, fills in missing information, and enriches contact profiles with accurate, up-to-date data."
    },
    {
      icon: RefreshCw,
      title: "Sync",
      description: "Push perfect data into your CRM", 
      details: "Seamlessly sync clean, enriched data directly into your CRM with smart field mapping and real-time updates."
    },
    {
      icon: Shield,
      title: "Governance",
      description: "Stay compliant with fields, audit trail, and mapping",
      details: "Enterprise-grade compliance with custom field validation, complete audit trails, and flexible data mapping rules."
    }
  ];

  return (
    <section className="section-padding bg-muted/20">
      <div className="container max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-4">
            Why NextEdge
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
            Four pillars of perfect CRM hygiene, powered by enterprise AI
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {pillars.map((pillar, index) => {
            const IconComponent = pillar.icon;
            return (
              <Card
                key={pillar.title}
                className="group hover-lift border-0 shadow-card hover:shadow-enterprise transition-all duration-300 h-full"
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <CardContent className="p-6">
                  <div className="flex items-center justify-center w-14 h-14 bg-primary-light rounded-xl mb-4 group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300">
                    <IconComponent className="h-7 w-7 text-primary group-hover:text-primary-foreground transition-colors duration-300" />
                  </div>
                  
                  <h3 className="text-lg font-bold text-foreground mb-2">
                    {pillar.title}
                  </h3>
                  
                  <p className="text-sm font-medium text-primary mb-3">
                    {pillar.description}
                  </p>
                  
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {pillar.details}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default ValuePillars;