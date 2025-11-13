import React from "react";
import { Button } from "./ui/button-enhanced";
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { SignedIn, SignedOut, UserButton } from "@clerk/clerk-react";
import { Link } from "react-router-dom";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 max-w-7xl items-center justify-between">
        {/* Logo */}
        <div className="flex items-center">
          <img 
            src="/lovable-uploads/adc57d85-0a2e-43b2-91d1-45cf3e175ec3.png" 
            alt="NEXTEDGE" 
            className="h-8 w-auto"
          />
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-8">
          <a href="#product" className="text-sm font-medium text-foreground hover:text-primary transition-colors">
            Product
          </a>
          <a href="#integrations" className="text-sm font-medium text-foreground hover:text-primary transition-colors">
            Integrations
          </a>
          <a href="#pricing" className="text-sm font-medium text-foreground hover:text-primary transition-colors">
            Pricing
          </a>
          <a href="#security" className="text-sm font-medium text-foreground hover:text-primary transition-colors">
            Security
          </a>
          <a href="#contact" className="text-sm font-medium text-foreground hover:text-primary transition-colors">
            Contact
          </a>
        </nav>

        {/* Desktop CTA Buttons */}
        <div className="hidden md:flex items-center space-x-4">
          <SignedOut>
            <Button variant="nav" size="sm" asChild>
              <Link to="/sign-in">Login</Link>
            </Button>
            <Button variant="hero" size="sm" asChild>
              <Link to="/sign-up">Sign Up</Link>
            </Button>
            <Button variant="hero" size="sm">
              Book a Demo
            </Button>
          </SignedOut>
          <SignedIn>
            <Button variant="hero" size="sm">
              Book a Demo
            </Button>
            <UserButton afterSignOutUrl="/" />
          </SignedIn>
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={toggleMenu}
          className="md:hidden p-2 text-foreground hover:text-primary"
          aria-label="Toggle menu"
        >
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="md:hidden border-t bg-background/95 backdrop-blur">
          <nav className="container py-4 space-y-4">
            <a href="#product" className="block text-sm font-medium text-foreground hover:text-primary transition-colors">
              Product
            </a>
            <a href="#integrations" className="block text-sm font-medium text-foreground hover:text-primary transition-colors">
              Integrations
            </a>
            <a href="#pricing" className="block text-sm font-medium text-foreground hover:text-primary transition-colors">
              Pricing
            </a>
            <a href="#security" className="block text-sm font-medium text-foreground hover:text-primary transition-colors">
              Security
            </a>
            <a href="#contact" className="block text-sm font-medium text-foreground hover:text-primary transition-colors">
              Contact
            </a>
            <div className="flex flex-col space-y-3 pt-4 border-t">
              <SignedOut>
                <Button variant="nav" size="sm" asChild>
                  <Link to="/sign-in">Login</Link>
                </Button>
                <Button variant="hero" size="sm" asChild>
                  <Link to="/sign-up">Sign Up</Link>
                </Button>
                <Button variant="hero" size="sm">
                  Book a Demo
                </Button>
              </SignedOut>
              <SignedIn>
                <Button variant="hero" size="sm">
                  Book a Demo
                </Button>
                <div className="flex items-center">
                  <UserButton afterSignOutUrl="/" />
                </div>
              </SignedIn>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
};

export default Header;
