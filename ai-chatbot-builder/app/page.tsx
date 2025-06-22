"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-white">
      {/* Navbar */}
      <header className="sticky top-0 z-50 w-full border-b" style={{ borderColor: "#539AB3" }}>
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2 font-bold" style={{ color: "#62B7D5" }}>
            <span className="text-2xl">AI Chatbot Builder</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button
                className="border transition-colors duration-300"
                style={{
                  borderColor: "#539AB3",
                  color: "#539AB3",
                }}
                onMouseOver={(e) => {
                  (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#539AB3";
                  (e.currentTarget as HTMLButtonElement).style.color = "#FFFFFF";
                }}
                onMouseOut={(e) => {
                  (e.currentTarget as HTMLButtonElement).style.backgroundColor = "transparent";
                  (e.currentTarget as HTMLButtonElement).style.color = "#539AB3";
                }}
              >
                Login
              </Button>
            </Link>
            <Link href="/register">
              <Button
                className="transition-colors duration-300"
                style={{
                  backgroundColor: "#66BEDE",
                  color: "#FFFFFF",
                }}
                onMouseOver={(e) => {
                  (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#539AB3";
                }}
                onMouseOut={(e) => {
                  (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#66BEDE";
                }}
              >
                Register
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center text-center py-24 space-y-16">
        <h1
          className="text-5xl font-bold transition-transform duration-700 ease-in-out hover:scale-105"
          style={{ color: "#1B708F" }}
        >
          Build AI Chatbots from Websites
        </h1>
        <p
          className="max-w-xl text-lg transition-transform duration-700 ease-in-out hover:scale-105"
          style={{ color: "#335F6F" }}
        >
          Scrape content. Train bots. Zero code.
        </p>
        <div className="flex gap-4">
          <Link href="/register">
            <Button
              className="transition-colors duration-300"
              style={{ backgroundColor: "#66BEDE", color: "#FFFFFF" }}
              onMouseOver={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#539AB3";
              }}
              onMouseOut={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#66BEDE";
              }}
            >
              Get Started
            </Button>
          </Link>
          {/* "Explore Chatbots" now routes to the same page as a user login */}
          <Link href="/user/dashboard">
            <Button
              className="border transition-colors duration-300"
              style={{ borderColor: "#539AB3", color: "#539AB3" }}
              onMouseOver={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#539AB3";
                (e.currentTarget as HTMLButtonElement).style.color = "#FFFFFF";
              }}
              onMouseOut={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "transparent";
                (e.currentTarget as HTMLButtonElement).style.color = "#539AB3";
              }}
            >
              Explore Chatbots
            </Button>
          </Link>
        </div>

        {/* Picture placeholder with scroll/hover animation */}
        <div className="w-full max-w-3xl h-64 rounded-2xl mt-10 flex items-center justify-center transition-transform duration-700 ease-in-out hover:-translate-y-2 overflow-hidden"
            style={{ border: "2px solid #539AB3" }}>
            <img
              src="/photo1.jpg"
              alt="AI Chatbot Preview"
              className="w-full h-full object-cover opacity-80 hover:opacity-100 transition-opacity duration-500"
            />
        </div>


        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          <FeatureCard
            title="Web Scraper"
            description="Extract content automatically from any website."
          />
          <FeatureCard
            title="Smart Database"
            description="Organize data efficiently for fast responses."
          />
          <FeatureCard
            title="LLM Integration"
            description="Generate accurate replies using AI models."
          />
        </div>
      </main>

      {/* Footer */}
      <footer
        className="border-t py-6 text-center text-sm"
        style={{ borderColor: "#539AB3", color: "#539AB3" }}
      >
        © 2025 AI Chatbot Builder. All rights reserved.
      </footer>
    </div>
  );
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div
      className="p-4 rounded-xl transition-all hover:shadow-lg"
      style={{ border: `2px solid #24424D`, backgroundColor: "#FFFFFF" }}
    >
      <div
        className="mb-2 w-full h-32 rounded-lg flex items-center justify-center transition-transform duration-700 ease-in-out hover:-translate-y-2"
        style={{ backgroundColor: "#66BEDE", opacity: 0.2, border: "2px solid #24424D", color: "#539AB3" }}
      >
        [ Picture / Icon ]
      </div>
      <h3
        className="text-xl font-semibold transition-transform duration-500 ease-in-out hover:scale-105"
        style={{ color: "#1B708F" }}
      >
        {title}
      </h3>
      <p
        className="text-sm transition-transform duration-500 ease-in-out hover:scale-105"
        style={{ color: "#335F6F" }}
      >
        {description}
      </p>
    </div>
  );
}
