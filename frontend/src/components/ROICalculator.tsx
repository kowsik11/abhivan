import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button-enhanced";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Calculator, TrendingUp, ArrowRight } from "lucide-react";

const ROICalculator = () => {
  const [reps, setReps] = useState(10);
  const [hourlyCost, setHourlyCost] = useState(75);
  const [hoursSaved, setHoursSaved] = useState(10);
  const [monthlySavings, setMonthlySavings] = useState(0);

  useEffect(() => {
    // Calculate monthly savings: reps × hourly × hours × 4.3 weeks
    const savings = reps * hourlyCost * hoursSaved * 4.3;
    setMonthlySavings(savings);
  }, [reps, hourlyCost, hoursSaved]);

  const yearlyROI = monthlySavings * 12;

  return (
    <section className="section-padding" id="roi">
      <div className="container max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground mb-4">
            Prove the ROI in seconds
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-balance">
            Calculate your potential savings with NextEdge automation
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <Card className="shadow-enterprise border-0 overflow-hidden">
            <CardHeader className="bg-gradient-card border-b">
              <CardTitle className="flex items-center gap-3 text-2xl">
                <div className="flex items-center justify-center w-10 h-10 bg-primary rounded-lg">
                  <Calculator className="h-6 w-6 text-primary-foreground" />
                </div>
                ROI Calculator
              </CardTitle>
            </CardHeader>
            
            <CardContent className="p-8">
              <div className="grid md:grid-cols-2 gap-8">
                {/* Input Section */}
                <div className="space-y-6">
                  <h3 className="text-lg font-semibold text-foreground mb-4">
                    Your Current Metrics
                  </h3>
                  
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="reps" className="text-sm font-medium text-foreground">
                        Number of Sales Reps
                      </Label>
                      <Input
                        id="reps"
                        type="number"
                        value={reps}
                        onChange={(e) => setReps(Number(e.target.value))}
                        className="mt-1"
                        min={1}
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="hourly" className="text-sm font-medium text-foreground">
                        Hourly Cost per Rep ($)
                      </Label>
                      <Input
                        id="hourly"
                        type="number"
                        value={hourlyCost}
                        onChange={(e) => setHourlyCost(Number(e.target.value))}
                        className="mt-1"
                        min={1}
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="hours" className="text-sm font-medium text-foreground">
                        Hours Saved per Rep per Week
                      </Label>
                      <Input
                        id="hours"
                        type="number"
                        value={hoursSaved}
                        onChange={(e) => setHoursSaved(Number(e.target.value))}
                        className="mt-1"
                        min={1}
                        max={40}
                      />
                    </div>
                  </div>
                </div>

                {/* Results Section */}
                <div className="bg-primary-light/50 rounded-xl p-6 space-y-6">
                  <div className="flex items-center gap-3 mb-4">
                    <TrendingUp className="h-6 w-6 text-primary" />
                    <h3 className="text-lg font-semibold text-foreground">
                      Your Potential Savings
                    </h3>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="p-4 bg-background rounded-lg border">
                      <div className="text-sm text-muted-foreground mb-1">Monthly Savings</div>
                      <div className="text-3xl font-bold text-success">
                        ${monthlySavings.toLocaleString()}
                      </div>
                    </div>
                    
                    <div className="p-4 bg-background rounded-lg border">
                      <div className="text-sm text-muted-foreground mb-1">Annual ROI</div>
                      <div className="text-2xl font-bold text-primary">
                        ${yearlyROI.toLocaleString()}
                      </div>
                    </div>
                    
                    <div className="text-xs text-muted-foreground">
                      * Based on {reps} reps saving {hoursSaved} hours/week at ${hourlyCost}/hour
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-8 text-center">
                <Button variant="cta" size="xl" className="group">
                  See Your Savings in Action
                  <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default ROICalculator;