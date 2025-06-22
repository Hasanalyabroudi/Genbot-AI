"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { MessageSquare, Star } from "lucide-react";

type RecentChatbot = {
  id: number;
  name: string;
  description: string;
  interactions: number;
};

type RecommendedChatbot = {
  id: number;
  name: string;
  description: string;
  users: number;
};

const recentChatbots: RecentChatbot[] = [
  {
    id: 1,
    name: "University of Ottawa",
    description: "Get answers about admissions, and campus life",
    interactions: 42,
  },
  {
    id: 2,
    name: "OC- Transport",
    description: "Get bus schedules and routes, and plan your trip.",
    interactions: 27,
  },
  {
    id: 3,
    name: "IT Helpdesk",
    description: "Technical support for common IT issues",
    interactions: 15,
  },
];

const recommendedChatbots: RecommendedChatbot[] = [
  {
    id: 4,
    name: "McGill University",
    description: "Get answers about admissions, and campus life",
    users: 1245,
  },
  {
    id: 5,
    name: "Course Advisor",
    description: "Get personalized course recommendations",
    users: 876,
  },
  {
    id: 6,
    name: "Real Estate Guide",
    description: "Find properties and get neighborhood information",
    users: 543,
  },
];

export default function UserDashboard() {
  const [favorites, setFavorites] = useState<number[]>([]);

  // Load favorites from localStorage on mount
  useEffect(() => {
    const storedFavorites = localStorage.getItem("favorites");
    if (storedFavorites) {
      setFavorites(JSON.parse(storedFavorites));
    }
  }, []);

  // Toggle favorite status for a chatbot
  const toggleFavorite = (chatbotId: number): void => {
    let updatedFavorites: number[];
    if (favorites.includes(chatbotId)) {
      updatedFavorites = favorites.filter((id) => id !== chatbotId);
    } else {
      updatedFavorites = [...favorites, chatbotId];
    }
    setFavorites(updatedFavorites);
    localStorage.setItem("favorites", JSON.stringify(updatedFavorites));
  };

  return (
    <div className="container mx-auto max-w-7xl space-y-8 py-8 bg-white px-4">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-[#1B708F]">
          Welcome!
        </h2>
        <p className="text-[#335F6F]">
          Find and chat with AI assistants built from website content.
        </p>
      </div>

      {/* Recently Used Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-semibold text-[#1B708F]">
            Recently Used
          </h3>
          <Link href="/user/chatbots">
            <Button variant="ghost" size="sm" className="text-[#539AB3]">
              View all
            </Button>
          </Link>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {recentChatbots.map((chatbot) => (
            <Card
              key={chatbot.id}
              className="border-2 border-[#24424D] bg-white h-72 flex flex-col overflow-hidden"
            >
              <CardHeader className="pb-2">
                <CardTitle className="text-[#1B708F] truncate">
                  {chatbot.name}
                </CardTitle>
                <CardDescription className="text-[#335F6F] line-clamp-2">
                  {chatbot.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex-1">
                <div className="flex items-center text-sm text-[#335F6F]">
                  <MessageSquare className="mr-1 h-4 w-4" />
                  {chatbot.interactions} recent interactions
                </div>
              </CardContent>
              <CardFooter className="mt-auto flex justify-between gap-2">
                <Link href={`/user/chat/${chatbot.id}`} className="flex-1">
                  <Button className="w-full bg-white text-[#1B708F] border border-[#24424D] hover:bg-[#E0EEF3]">
                    <MessageSquare className="mr-2 h-4 w-4" />
                    Start Chat
                  </Button>
                </Link>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => toggleFavorite(chatbot.id)}
                  className="text-[#539AB3] border border-[#24424D] hover:bg-[#E0EEF3]"
                >
                  {favorites.includes(chatbot.id) ? (
                    <Star className="h-4 w-4 fill-[#1B708F]" />
                  ) : (
                    <Star className="h-4 w-4 fill-transparent stroke-[#1B708F]" />
                  )}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>

      {/* Recommended for You Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-semibold text-[#1B708F]">
            Recommended for You
          </h3>
          <Link href="/user/chatbots">
            <Button variant="ghost" size="sm" className="text-[#539AB3]">
              Explore more
            </Button>
          </Link>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {recommendedChatbots.map((chatbot) => (
            <Card
              key={chatbot.id}
              className="border-2 border-[#24424D] bg-white h-72 flex flex-col overflow-hidden"
            >
              <CardHeader className="pb-2">
                <CardTitle className="text-[#1B708F] truncate">
                  {chatbot.name}
                </CardTitle>
                <CardDescription className="text-[#335F6F] line-clamp-2">
                  {chatbot.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex-1">
                <div className="flex items-center text-sm text-[#335F6F]">
                  <Star className="mr-1 h-4 w-4 fill-[#1B708F]" />
                  Used by {chatbot.users} people
                </div>
              </CardContent>
              <CardFooter className="mt-auto flex justify-between gap-2">
                <Link href={`/user/chat/${chatbot.id}`} className="flex-1">
                  <Button className="w-full bg-white text-[#1B708F] border border-[#24424D] hover:bg-[#E0EEF3]">
                    <MessageSquare className="mr-2 h-4 w-4" />
                    Chat
                  </Button>
                </Link>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => toggleFavorite(chatbot.id)}
                  className="text-[#539AB3] border border-[#24424D] hover:bg-[#E0EEF3]"
                >
                  {favorites.includes(chatbot.id) ? (
                    <Star className="h-4 w-4 fill-[#1B708F]" />
                  ) : (
                    <Star className="h-4 w-4 fill-transparent stroke-[#1B708F]" />
                  )}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
