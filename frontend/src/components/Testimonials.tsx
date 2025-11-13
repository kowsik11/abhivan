import React from "react";
import { Card, CardContent } from "./ui/card";
import { Star, Quote } from "lucide-react";

const Testimonials = () => {
  const testimonials = [
    {
      quote: "NextEdge saves us 10+ hours per rep each week — with cleaner CRM data than ever before.",
      name: "Sarah Chen",
      role: "COO",
      company: "Altai Capital",
      rating: 5
    },
    {
      quote: "Seamlessly aggregates info, transforming our workflows.",
      name: "Marcus Rodriguez", 
      role: "Director",
      company: "ContextLogic",
      rating: 5
    },
    {
      quote: "Perfect CRM hygiene without manual effort.",
      name: "Jennifer Walsh",
      role: "CEO",
      company: "Onyx AI",
      rating: 5
    }
  ];

  return (
    <section className="section-padding bg-muted/20">
      <div className="container max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-4">
            Loved by Sales Leaders
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
            See what our customers say about NextEdge
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <Card
              key={testimonial.name}
              className="group hover-lift border-0 shadow-card hover:shadow-enterprise transition-all duration-300 h-full"
              style={{ animationDelay: `${index * 200}ms` }}
            >
              <CardContent className="p-8 h-full flex flex-col">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-1">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 fill-primary text-primary" />
                    ))}
                  </div>
                  <Quote className="h-8 w-8 text-primary/20" />
                </div>
                
                <blockquote className="text-foreground leading-relaxed mb-6 flex-grow">
                  "{testimonial.quote}"
                </blockquote>
                
                <div className="border-t pt-4">
                  <div className="font-semibold text-foreground">
                    {testimonial.name}
                  </div>
                  <div className="text-sm text-primary font-medium">
                    {testimonial.role}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {testimonial.company}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;