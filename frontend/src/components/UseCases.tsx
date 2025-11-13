import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Users, BarChart3, Building2, Rocket } from "lucide-react";

const UseCases = () => {
  const useCases = [
    {
      icon: Users,
      title: "Sales Teams",
      subtitle: "Perfect notes & deal insights",
      description: "Automatically capture every customer interaction, generate intelligent meeting summaries, and surface deal insights that drive revenue growth.",
      benefits: ["Auto-capture all touchpoints", "AI-generated meeting notes", "Deal progression insights"]
    },
    {
      icon: BarChart3,
      title: "RevOps",
      subtitle: "Clean, reliable pipeline data", 
      description: "Ensure data quality across your entire revenue operations with automated cleansing, enrichment, and real-time pipeline visibility.",
      benefits: ["Clean pipeline data", "Revenue forecasting", "Automated reporting"]
    },
    {
      icon: Building2,
      title: "Asset Managers",
      subtitle: "Track every client interaction automatically",
      description: "Maintain comprehensive client relationship records with automated interaction tracking and compliance-ready audit trails.",
      benefits: ["Complete audit trails", "Compliance ready", "Client relationship mapping"]
    },
    {
      icon: Rocket,
      title: "Startups",
      subtitle: "Scale without admin overhead", 
      description: "Focus on growth while NextEdge handles your CRM hygiene. Scale your sales operations without adding administrative burden.",
      benefits: ["Zero admin overhead", "Instant setup", "Scales with growth"]
    }
  ];

  return (
    <section className="section-padding">
      <div className="container max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-4">
            Who It's For
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
            NextEdge adapts to your team's unique needs and workflow
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {useCases.map((useCase, index) => {
            const IconComponent = useCase.icon;
            return (
              <Card
                key={useCase.title}
                className="group hover-lift border-0 shadow-card hover:shadow-enterprise transition-all duration-300 h-full"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                <CardHeader className="pb-4">
                  <div className="flex items-center gap-4">
                    <div className="flex items-center justify-center w-12 h-12 bg-primary-light rounded-xl group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300">
                      <IconComponent className="h-6 w-6 text-primary group-hover:text-primary-foreground transition-colors duration-300" />
                    </div>
                    <div>
                      <CardTitle className="text-xl font-bold text-foreground">
                        {useCase.title}
                      </CardTitle>
                      <p className="text-sm font-medium text-primary">
                        {useCase.subtitle}
                      </p>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent className="pt-0">
                  <p className="text-muted-foreground mb-6 leading-relaxed">
                    {useCase.description}
                  </p>
                  
                  <div className="space-y-2">
                    {useCase.benefits.map((benefit, benefitIndex) => (
                      <div key={benefitIndex} className="flex items-center gap-3">
                        <div className="w-2 h-2 bg-primary rounded-full flex-shrink-0"></div>
                        <span className="text-sm text-foreground font-medium">
                          {benefit}
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default UseCases;