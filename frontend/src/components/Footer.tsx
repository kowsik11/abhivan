import React from "react";
import { Separator } from "./ui/separator";
import { Linkedin, Twitter, Instagram, Youtube, Facebook, Github } from "lucide-react";

const Footer = () => {
  const footerLinks = {
    product: ["Product", "Integrations", "Pricing", "Security"],
    legal: ["Contact", "Privacy Policy", "Terms"]
  };

  return (
    <footer className="bg-muted text-muted-foreground">
      <div className="container max-w-7xl mx-auto px-4 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="text-2xl font-bold text-foreground mb-4">
              NextEdge
            </div>
            <p className="text-base text-muted-foreground">
              CRM that works, without the work
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-semibold text-foreground mb-3">Product</h4>
            <ul className="space-y-2">
              {footerLinks.product.map((link) => (
                <li key={link}>
                  <a href="#" className="text-base hover:text-primary transition-colors">
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-foreground mb-3">Legal</h4>
            <ul className="space-y-2">
              {footerLinks.legal.map((link) => (
                <li key={link}>
                  <a href="#" className="text-base hover:text-primary transition-colors">
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <Separator className="my-8" />
        
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="text-base">
            © 2025 NextEdge. All rights reserved.
          </div>
          
          <div className="flex items-center gap-4 mt-4 md:mt-0">
            <a href="#" className="hover:text-primary transition-colors hover:scale-110 transform duration-200">
              <span className="sr-only">LinkedIn</span>
              <Linkedin className="w-5 h-5" />
            </a>
            <a href="#" className="hover:text-primary transition-colors hover:scale-110 transform duration-200">
              <span className="sr-only">Twitter</span>
              <Twitter className="w-5 h-5" />
            </a>
            <a href="#" className="hover:text-primary transition-colors hover:scale-110 transform duration-200">
              <span className="sr-only">Instagram</span>
              <Instagram className="w-5 h-5" />
            </a>
            <a href="#" className="hover:text-primary transition-colors hover:scale-110 transform duration-200">
              <span className="sr-only">YouTube</span>
              <Youtube className="w-5 h-5" />
            </a>
            <a href="#" className="hover:text-primary transition-colors hover:scale-110 transform duration-200">
              <span className="sr-only">Facebook</span>
              <Facebook className="w-5 h-5" />
            </a>
            <a href="#" className="hover:text-primary transition-colors hover:scale-110 transform duration-200">
              <span className="sr-only">GitHub</span>
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;