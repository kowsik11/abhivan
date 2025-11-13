import React from "react";
import { Card, CardContent } from "./ui/card";
import { Shield, Lock, UserCheck, FileX, Award } from "lucide-react";

const Security = () => {
  const securityFeatures = [
    {
      icon: Shield,
      title: "Data Never Used for Model Training",
      description: "Your sensitive business data stays private and is never used to train our AI models."
    },
    {
      icon: Lock,
      title: "End-to-End Encryption",
      description: "All data is encrypted in transit and at rest using industry-standard AES-256 encryption."
    },
    {
      icon: UserCheck,
      title: "RBAC Permissions",
      description: "Role-based access controls ensure only authorized team members can access specific data."
    },
    {
      icon: FileX,
      title: "Deletion Policy",
      description: "Complete data deletion on demand with verified removal from all systems and backups."
    },
    {
      icon: Award,
      title: "SOC2 Roadmap",
      description: "Currently pursuing SOC2 Type II certification to meet enterprise compliance standards."
    }
  ];

  return (
    <section className="section-padding" id="security">
      <div className="container max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-4">
            Enterprise-grade security and reliability
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
            Your data security and privacy are our top priorities
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {securityFeatures.map((feature, index) => {
            const IconComponent = feature.icon;
            return (
              <Card
                key={feature.title}
                className="group hover-lift border-0 shadow-card hover:shadow-enterprise transition-all duration-300 h-full"
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <CardContent className="p-6 text-center">
                  <div className="flex items-center justify-center w-16 h-16 bg-success/10 rounded-full mb-4 mx-auto group-hover:bg-success group-hover:text-success-foreground transition-all duration-300">
                    <IconComponent className="h-8 w-8 text-success group-hover:text-success-foreground transition-colors duration-300" />
                  </div>
                  
                  <h3 className="text-lg font-bold text-foreground mb-3">
                    {feature.title}
                  </h3>
                  
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>
        
        <div className="mt-12 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-success/10 text-success rounded-full text-sm font-medium">
            <Shield className="h-4 w-4" />
            Enterprise Security & Compliance Ready
          </div>
        </div>
      </div>
    </section>
  );
};

export default Security;