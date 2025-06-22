"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Send, Bot, User, ArrowLeft } from "lucide-react"
import Link from "next/link"

// Mock data for chatbot details
const getChatbotDetails = (id: string) => {
  const chatbots = {
    "1": {
      name: "University FAQ",
      description: "Get answers about programs, admissions, and campus life",
      avatar: "/placeholder.svg?height=40&width=40",
    },
    "2": {
      name: "E-commerce Support",
      description: "Help with orders, returns, and product information",
      avatar: "/placeholder.svg?height=40&width=40",
    },
    "3": {
      name: "IT Helpdesk",
      description: "Technical support for common IT issues",
      avatar: "/placeholder.svg?height=40&width=40",
    },
  }

  return (
    chatbots[id as keyof typeof chatbots] || {
      name: "Chatbot",
      description: "AI Assistant",
      avatar: "/placeholder.svg?height=40&width=40",
    }
  )
}

// Sample initial messages
const getInitialMessages = (chatbotName: string) => [
  {
    role: "bot",
    content: `Hi there! I'm the ${chatbotName} assistant. How can I help you today?`,
  },
]

interface Message {
  role: "user" | "bot"
  content: string
}

export default function AdminChatTest({ params }: { params: { id: string } }) {
  const chatbotDetails = getChatbotDetails(params.id)
  const [messages, setMessages] = useState<Message[]>(getInitialMessages(chatbotDetails.name))
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = () => {
    if (!input.trim()) return

    // Add user message
    const userMessage = { role: "user" as const, content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // Simulate bot response after a delay
    setTimeout(() => {
      const botResponses: { [key: string]: string } = {
        university:
          "Our university offers over 200 undergraduate programs across 6 faculties. Admissions for the fall semester are open until May 1st. Would you like specific information about a particular program?",
        course:
          "We offer a variety of courses in different disciplines. To find the right course, you can browse by faculty, program, or use keywords. What subject are you interested in?",
        admission:
          "For admission requirements, you'll need to submit your transcripts, a personal statement, and letters of recommendation. International students may need to provide language proficiency test results.",
        product:
          "We have a wide range of products available. You can browse by category, brand, or price range. Is there a specific type of product you're looking for?",
        order:
          "To check your order status, please provide your order number. If you need to make changes to your order, you can do so within 24 hours of placing it.",
        return:
          "Our return policy allows returns within 30 days of purchase. Items must be in original condition with tags attached. Would you like to initiate a return?",
        password:
          "If you've forgotten your password, you can reset it by clicking the 'Forgot Password' link on the login page. We'll send a reset link to your registered email address.",
        software:
          "For software issues, first try restarting your computer. If the problem persists, check for updates or reinstall the software. Would you like more specific troubleshooting steps?",
      }

      // Check if any keywords match
      const lowercaseInput = input.toLowerCase()
      let botResponse = "I'm not sure I understand. Could you please provide more details or rephrase your question?"

      for (const [keyword, response] of Object.entries(botResponses)) {
        if (lowercaseInput.includes(keyword)) {
          botResponse = response
          break
        }
      }

      setMessages((prev) => [...prev, { role: "bot", content: botResponse }])
      setIsLoading(false)
    }, 1500)
  }

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-64px)]">
      <div className="flex items-center gap-2 p-4 border-b">
        <Link href="/admin/chatbots">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-5 w-5" />
          </Button>
        </Link>
        <Avatar>
          <AvatarImage src={chatbotDetails.avatar} alt={chatbotDetails.name} />
          <AvatarFallback>
            <Bot className="h-5 w-5" />
          </AvatarFallback>
        </Avatar>
        <div>
          <h2 className="text-lg font-semibold">{chatbotDetails.name}</h2>
          <p className="text-sm text-muted-foreground">{chatbotDetails.description}</p>
        </div>
        <div className="ml-auto flex gap-2">
          <Link href={`/admin/chatbots/${params.id}/settings`}>
            <Button variant="outline" size="sm">
              Settings
            </Button>
          </Link>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className="flex gap-3 max-w-[80%]">
              {message.role === "bot" && (
                <Avatar className="h-8 w-8">
                  <AvatarImage src={chatbotDetails.avatar} alt="Bot" />
                  <AvatarFallback>
                    <Bot className="h-4 w-4" />
                  </AvatarFallback>
                </Avatar>
              )}
              <Card className={message.role === "user" ? "bg-primary text-primary-foreground" : ""}>
                <CardContent className="p-3">
                  <p>{message.content}</p>
                </CardContent>
              </Card>
              {message.role === "user" && (
                <Avatar className="h-8 w-8">
                  <AvatarFallback>
                    <User className="h-4 w-4" />
                  </AvatarFallback>
                </Avatar>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="flex gap-3 max-w-[80%]">
              <Avatar className="h-8 w-8">
                <AvatarImage src={chatbotDetails.avatar} alt="Bot" />
                <AvatarFallback>
                  <Bot className="h-4 w-4" />
                </AvatarFallback>
              </Avatar>
              <Card>
                <CardContent className="p-3">
                  <div className="flex space-x-1">
                    <div className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" />
                    <div className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce [animation-delay:0.2s]" />
                    <div className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce [animation-delay:0.4s]" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t">
        <form
          onSubmit={(e) => {
            e.preventDefault()
            handleSendMessage()
          }}
          className="flex gap-2"
        >
          <Input
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
          <Button type="submit" disabled={!input.trim() || isLoading}>
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </div>
    </div>
  )
}

