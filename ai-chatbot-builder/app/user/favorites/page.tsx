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

type Chatbot = {
  id: number;
  name: string;
  description: string;
  category: string;
  lastUsed: string;
};

const allChatbots: Chatbot[] = [
  {
    id: 1,
    name: "University FAQ",
    description: "Get answers about programs, admissions, and campus life",
    category: "Education",
    lastUsed: "2 days ago",
  },
  {
    id: 2,
    name: "E-commerce Support",
    description: "Help with orders, returns, and product information",
    category: "Shopping",
    lastUsed: "5 days ago",
  },
  {
    id: 3,
    name: "IT Helpdesk",
    description: "Technical support for common IT issues",
    category: "Technology",
    lastUsed: "1 week ago",
  },
  {
    id: 4,
    name: "Product Catalog",
    description: "Browse and search for products with AI assistance",
    category: "Shopping",
    lastUsed: "3 days ago",
  },
  {
    id: 5,
    name: "Course Advisor",
    description: "Get personalized course recommendations",
    category: "Education",
    lastUsed: "4 days ago",
  },
  {
    id: 6,
    name: "Real Estate Guide",
    description: "Find properties and get neighborhood information",
    category: "Real Estate",
    lastUsed: "2 weeks ago",
  },
  {
    id: 7,
    name: "Health Advisor",
    description: "General health information and wellness tips",
    category: "Health",
    lastUsed: "3 weeks ago",
  },
  {
    id: 8,
    name: "Travel Assistant",
    description: "Travel recommendations and booking assistance",
    category: "Travel",
    lastUsed: "1 month ago",
  },
  {
    id: 9,
    name: "Financial Advisor",
    description: "Personal finance tips and investment guidance",
    category: "Finance",
    lastUsed: "2 weeks ago",
  },
];

export default function UserFavorites() {
  const [favorites, setFavorites] = useState<number[]>([]);

  useEffect(() => {
    const storedFavorites = localStorage.getItem("favorites");
    if (storedFavorites) {
      setFavorites(JSON.parse(storedFavorites));
    }
  }, []);

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

  // Filter to show only favorited chatbots
  const favoriteChatbots = allChatbots.filter((chatbot) =>
    favorites.includes(chatbot.id)
  );

  return (
    <div className="container mx-auto max-w-7xl space-y-6 py-8 bg-white px-4">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-[#1B708F]">
          Favorite Chatbots
        </h2>
        <p className="text-[#335F6F]">
          Your saved chatbots for quick access
        </p>
      </div>

      {favoriteChatbots.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {favoriteChatbots.map((chatbot) => (
            <Card
              key={chatbot.id}
              className="border-2 border-[#24424D] bg-white h-72 flex flex-col overflow-hidden"
            >
              <CardHeader className="pb-2">
                <div className="flex justify-between">
                  <CardTitle className="text-[#1B708F] truncate">
                    {chatbot.name}
                  </CardTitle>
                  <span className="text-xs bg-[#E0EEF3] px-2 py-1 rounded-full text-[#1B708F] whitespace-nowrap">
                    {chatbot.category}
                  </span>
                </div>
                <CardDescription className="text-[#335F6F] line-clamp-2">
                  {chatbot.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex-1">
                <div className="flex items-center text-sm text-[#335F6F]">
                  <Star className="mr-1 h-4 w-4 fill-[#1B708F]" />
                  Last used {chatbot.lastUsed}
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
                  <Star className="h-4 w-4 fill-[#1B708F]" />
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <Star className="h-12 w-12 text-[#335F6F] mb-4" />
          <h3 className="text-xl font-semibold mb-2 text-[#1B708F]">
            No favorites yet
          </h3>
          <p className="text-[#335F6F] mb-6 max-w-md">
            You haven&apos;t added any chatbots to your favorites. Browse the chatbots and click the star icon to add them here.
          </p>
          <Link href="/user/chatbots">
            <Button className="bg-white text-[#1B708F] border border-[#24424D] hover:bg-[#E0EEF3]">
              Browse Chatbots
            </Button>
          </Link>
        </div>
      )}
    </div>
  );
}
