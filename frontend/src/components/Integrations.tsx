import React from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button-enhanced";
import { ArrowRight, Mail, Calendar, MessageSquare, Database } from "lucide-react";

const Integrations = () => {
  const integrations = [
    { name: "Gmail", icon: Mail, category: "Email" },
    { name: "Outlook", icon: Mail, category: "Email" },
    { name: "Slack", icon: MessageSquare, category: "Communication" },
    { name: "Teams", icon: MessageSquare, category: "Communication" },
    { name: "HubSpot", icon: Database, category: "CRM" },
    { name: "Salesforce", icon: Database, category: "CRM" },
    { name: "Zoom", icon: Calendar, category: "Meetings" },
    { name: "Google Cal", icon: Calendar, category: "Calendar" },
  ];

  return (
    <section className="section-padding bg-muted/20" id="integrations">
      <div className="container max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-4">
            Connect NextEdge to the tools you already use
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
            Seamless integrations with your existing workflow
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-6 mb-12">
          {integrations.map((integration, index) => {
            const IconComponent = integration.icon;
            return (
              <Card
                key={integration.name}
                className="group hover-lift border-0 shadow-card hover:shadow-enterprise transition-all duration-300 aspect-square"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <CardContent className="p-4 flex flex-col items-center justify-center h-full text-center">
                  <div className="flex items-center justify-center w-12 h-12 bg-primary-light rounded-lg mb-3 group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300">
                    <IconComponent className="h-6 w-6 text-primary group-hover:text-primary-foreground transition-colors duration-300" />
                  </div>
                  
                  <div className="text-sm font-semibold text-foreground mb-1">
                    {integration.name}
                  </div>
                  
                  <div className="text-xs text-muted-foreground">
                    {integration.category}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="text-center">
          <p className="text-muted-foreground mb-6">
            Plus 50+ more integrations available
          </p>
          <Button variant="hero-outline" size="lg" className="group">
            View All Integrations
            <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
          </Button>
        </div>
      </div>
    </section>
  );
};

export default Integrations;