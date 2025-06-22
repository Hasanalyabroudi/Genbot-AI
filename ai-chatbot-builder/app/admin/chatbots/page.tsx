import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Bot, Plus, Settings } from "lucide-react"

// Mock data for chatbots
const chatbots = [
  {
    id: 1,
    name: "University FAQ",
    url: "uottawa.ca",
    model: "GPT-4o",
    pagesScraped: 342,
    promptsUsed: 1245,
    status: "active",
  },
  {
    id: 2,
    name: "E-commerce Support",
    url: "shopify.com",
    model: "GPT-4o",
    pagesScraped: 215,
    promptsUsed: 987,
    status: "active",
  },
  {
    id: 3,
    name: "IT Helpdesk",
    url: "techsupport.com",
    model: "GPT-3.5",
    pagesScraped: 156,
    promptsUsed: 756,
    status: "active",
  },
  {
    id: 4,
    name: "Product Catalog",
    url: "products.com",
    model: "GPT-4o",
    pagesScraped: 423,
    promptsUsed: 532,
    status: "inactive",
  },
  {
    id: 5,
    name: "Course Advisor",
    url: "courses.edu",
    model: "GPT-3.5",
    pagesScraped: 189,
    promptsUsed: 421,
    status: "active",
  },
  {
    id: 6,
    name: "Real Estate Guide",
    url: "realestate.com",
    model: "GPT-4o",
    pagesScraped: 267,
    promptsUsed: 312,
    status: "inactive",
  },
]

export default function AdminChatbots() {
  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Chatbots</h2>
        <Link href="/admin/chatbots/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            New Chatbot
          </Button>
        </Link>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {chatbots.map((chatbot) => (
          <Card key={chatbot.id}>
            <CardHeader className="pb-2">
              <div className="flex items-start justify-between">
                <CardTitle className="text-lg font-bold">{chatbot.name}</CardTitle>
                <Badge variant={chatbot.status === "active" ? "default" : "secondary"}>{chatbot.status}</Badge>
              </div>
              <CardDescription>{chatbot.url}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="flex flex-col">
                  <span className="text-muted-foreground">Model</span>
                  <span className="font-medium">{chatbot.model}</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-muted-foreground">Pages Scraped</span>
                  <span className="font-medium">{chatbot.pagesScraped}</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-muted-foreground">Prompts Used</span>
                  <span className="font-medium">{chatbot.promptsUsed}</span>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Link href={`/admin/chatbots/${chatbot.id}`}>
                <Button variant="outline" size="sm">
                  <Bot className="mr-2 h-4 w-4" />
                  Test Chat
                </Button>
              </Link>
              <Link href={`/admin/chatbots/${chatbot.id}/settings`}>
                <Button variant="outline" size="sm">
                  <Settings className="mr-2 h-4 w-4" />
                  Settings
                </Button>
              </Link>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}

