import React from "react";
import Header from "../components/Header";
import Hero from "../components/Hero";
import SocialProof from "../components/SocialProof";
import HowItWorks from "../components/HowItWorks";
import ValuePillars from "../components/ValuePillars";
import ROICalculator from "../components/ROICalculator";
import Integrations from "../components/Integrations";
import UseCases from "../components/UseCases";
import Testimonials from "../components/Testimonials";
import Security from "../components/Security";
import FAQ from "../components/FAQ";
import FinalCTA from "../components/FinalCTA";
import Footer from "../components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <Hero />
        <SocialProof />
        <HowItWorks />
        <ValuePillars />
        <ROICalculator />
        <Integrations />
        <UseCases />
        <Testimonials />
        <Security />
        <FAQ />
        <FinalCTA />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
