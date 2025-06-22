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
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MessageSquare, Search, Star } from "lucide-react";

type Chatbot = {
  id: number;
  name: string;
  description: string;
  category: string;
  users: number;
};

const allChatbots: Chatbot[] = [
  {
    id: 1,
    name: "University FAQ",
    description: "Get answers about programs, admissions, and campus life",
    category: "Education",
    users: 2453,
  },
  {
    id: 2,
    name: "E-commerce Support",
    description: "Help with orders, returns, and product information",
    category: "Shopping",
    users: 1876,
  },
  {
    id: 3,
    name: "IT Helpdesk",
    description: "Technical support for common IT issues",
    category: "Technology",
    users: 1542,
  },
  {
    id: 4,
    name: "Product Catalog",
    description: "Browse and search for products with AI assistance",
    category: "Shopping",
    users: 1245,
  },
  {
    id: 5,
    name: "Course Advisor",
    description: "Get personalized course recommendations",
    category: "Education",
    users: 876,
  },
  {
    id: 6,
    name: "Real Estate Guide",
    description: "Find properties and get neighborhood information",
    category: "Real Estate",
    users: 543,
  },
  {
    id: 7,
    name: "Health Advisor",
    description: "General health information and wellness tips",
    category: "Health",
    users: 987,
  },
  {
    id: 8,
    name: "Travel Assistant",
    description: "Travel recommendations and booking assistance",
    category: "Travel",
    users: 765,
  },
  {
    id: 9,
    name: "Financial Advisor",
    description: "Personal finance tips and investment guidance",
    category: "Finance",
    users: 654,
  },
];

export default function UserChatbots() {
  const [searchQuery, setSearchQuery] = useState("");
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

  const filteredChatbots = allChatbots.filter(
    (chatbot) =>
      chatbot.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      chatbot.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      chatbot.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const categories = [
    "All",
    "Education",
    "Shopping",
    "Technology",
    "Real Estate",
    "Health",
    "Travel",
    "Finance",
  ];

  return (
    <div className="container mx-auto max-w-7xl space-y-6 py-8 bg-white px-4">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-[#1B708F]">
          Explore Chatbots
        </h2>
        <p className="text-[#335F6F]">
          Discover AI chatbots built from various websites
        </p>
      </div>

      <div className="flex w-full max-w-sm items-center space-x-2">
        <Input
          type="search"
          placeholder="Search chatbots..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full"
        />
        <Button
          type="submit"
          size="icon"
          className="bg-white text-[#1B708F] border border-[#24424D] hover:bg-[#E0EEF3]"
        >
          <Search className="h-4 w-4" />
        </Button>
      </div>

      <Tabs defaultValue="All" className="space-y-4">
        <TabsList className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <TabsTrigger
              key={category}
              value={category}
              className="px-4 py-2 rounded border border-[#24424D] text-[#1B708F] hover:bg-[#E0EEF3] data-[state=active]:bg-[#E0EEF3] data-[state=active]:text-[#1B708F]"
            >
              {category}
            </TabsTrigger>
          ))}
        </TabsList>

        {categories.map((category) => (
          <TabsContent key={category} value={category} className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {filteredChatbots
                .filter(
                  (chatbot) =>
                    category === "All" || chatbot.category === category
                )
                .map((chatbot) => (
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
                        Used by {chatbot.users} people
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
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}
