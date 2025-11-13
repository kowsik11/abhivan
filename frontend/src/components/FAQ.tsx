import React from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "./ui/accordion";

const FAQ = () => {
  const faqs = [
    {
      question: "How does the automation work?",
      answer: "NextEdge uses advanced AI to monitor your communication channels (email, calendar, calls) in real-time. Our AI agents automatically capture interactions, extract key information, enrich contact data, and sync everything to your CRM with perfect accuracy."
    },
    {
      question: "Which CRMs do you integrate with?",
      answer: "We integrate with all major CRM platforms including Salesforce, HubSpot, Pipedrive, Zoho, and Microsoft Dynamics. Our flexible API also supports custom CRM implementations. Setup typically takes less than 15 minutes."
    },
    {
      question: "How accurate is the AI?",
      answer: "Our AI maintains 99.2% accuracy in data capture and enrichment. The system continuously learns and improves, with built-in validation checks and human-in-the-loop verification for critical data points. You can also customize confidence thresholds."
    },
    {
      question: "Can we customize the data mapping?",
      answer: "Absolutely. NextEdge offers flexible field mapping, custom data transformation rules, and configurable sync preferences. You can map any data point to any CRM field and set up complex business logic for different scenarios."
    },
    {
      question: "Is my data secure?",
      answer: "Yes. We use enterprise-grade security with AES-256 encryption, SOC2 compliance roadmap, and strict data governance policies. Your data is never used for AI training, and we offer complete data deletion on demand with audit trails."
    },
    {
      question: "How long does implementation take?",
      answer: "Most customers are up and running within 24-48 hours. Initial setup takes 15 minutes, and our AI begins learning your patterns immediately. Full optimization typically occurs within the first week of usage."
    },
    {
      question: "Do you offer training and onboarding?",
      answer: "Yes, we provide comprehensive onboarding including live training sessions, detailed documentation, and ongoing support. Our customer success team ensures your team maximizes value from day one."
    },
    {
      question: "What kind of support is included?",
      answer: "All plans include 24/7 technical support, dedicated customer success managers, regular optimization reviews, and access to our knowledge base and community forums."
    }
  ];

  return (
    <section className="section-padding bg-muted/20">
      <div className="container max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-4">
            Frequently Asked Questions
          </h2>
          <p className="text-xl text-muted-foreground text-balance">
            Everything you need to know about NextEdge
          </p>
        </div>

        <div className="bg-background rounded-2xl shadow-enterprise p-8">
          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem 
                key={index} 
                value={`item-${index}`}
                className="border border-border rounded-lg px-6"
              >
                <AccordionTrigger className="text-left text-lg font-semibold text-foreground hover:text-primary transition-colors">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground leading-relaxed pt-2 text-base">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
};

export default FAQ;