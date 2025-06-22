"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { Slider } from "@/components/ui/slider"

// Mock data for chatbot details
const getChatbotDetails = (id: string) => {
  const chatbots = {
    "1": {
      name: "University FAQ",
      url: "uottawa.ca",
      model: "gpt-4o",
      temperature: 0.7,
      maxTokens: 1024,
      pagesScraped: 342,
      promptsUsed: 1245,
      status: "active",
      systemPrompt:
        "You are a helpful assistant for the University of Ottawa. Answer questions about programs, admissions, campus life, and other university-related topics based on the information provided.",
    },
    "2": {
      name: "E-commerce Support",
      url: "shopify.com",
      model: "gpt-4o",
      temperature: 0.5,
      maxTokens: 2048,
      pagesScraped: 215,
      promptsUsed: 987,
      status: "active",
      systemPrompt:
        "You are a customer support assistant for an e-commerce platform. Help users with orders, returns, product information, and other shopping-related questions based on the information provided.",
    },
  }

  return (
    chatbots[id as keyof typeof chatbots] || {
      name: "New Chatbot",
      url: "",
      model: "gpt-4o",
      temperature: 0.7,
      maxTokens: 1024,
      pagesScraped: 0,
      promptsUsed: 0,
      status: "inactive",
      systemPrompt: "You are a helpful assistant. Answer questions based on the information provided.",
    }
  )
}

export default function ChatbotSettings({ params }: { params: { id: string } }) {
  const chatbotDetails = getChatbotDetails(params.id)
  const [name, setName] = useState(chatbotDetails.name)
  const [url, setUrl] = useState(chatbotDetails.url)
  const [model, setModel] = useState(chatbotDetails.model)
  const [temperature, setTemperature] = useState(chatbotDetails.temperature)
  const [maxTokens, setMaxTokens] = useState(chatbotDetails.maxTokens)
  const [systemPrompt, setSystemPrompt] = useState(chatbotDetails.systemPrompt)
  const [status, setStatus] = useState(chatbotDetails.status === "active")

  const handleSave = () => {
    // In a real app, this would save the settings to the backend
    alert("Settings saved successfully!")
  }

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Chatbot Settings</h2>
        <Button onClick={handleSave}>Save Changes</Button>
      </div>

      <Tabs defaultValue="general" className="space-y-4">
        <TabsList>
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="model">Model</TabsTrigger>
          <TabsTrigger value="scraping">Scraping</TabsTrigger>
          <TabsTrigger value="advanced">Advanced</TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>General Settings</CardTitle>
              <CardDescription>Basic information about your chatbot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Chatbot Name</Label>
                <Input id="name" value={name} onChange={(e) => setName(e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="url">Website URL</Label>
                <Input id="url" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="example.com" />
                <p className="text-sm text-muted-foreground">The website to scrape content from</p>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="status">Active</Label>
                  <Switch id="status" checked={status} onCheckedChange={setStatus} />
                </div>
                <p className="text-sm text-muted-foreground">Enable or disable this chatbot</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Statistics</CardTitle>
              <CardDescription>Usage statistics for this chatbot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h3 className="text-sm font-medium">Pages Scraped</h3>
                  <p className="text-2xl font-bold">{chatbotDetails.pagesScraped}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium">Prompts Used</h3>
                  <p className="text-2xl font-bold">{chatbotDetails.promptsUsed}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="model" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Model Settings</CardTitle>
              <CardDescription>Configure the AI model used by this chatbot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="model">Model</Label>
                <Select value={model} onValueChange={setModel}>
                  <SelectTrigger id="model">
                    <SelectValue placeholder="Select model" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="gpt-4o">GPT-4o</SelectItem>
                    <SelectItem value="gpt-4">GPT-4</SelectItem>
                    <SelectItem value="gpt-3.5">GPT-3.5 Turbo</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="temperature">Temperature: {temperature}</Label>
                </div>
                <Slider
                  id="temperature"
                  min={0}
                  max={1}
                  step={0.1}
                  value={[temperature]}
                  onValueChange={(value) => setTemperature(value[0])}
                />
                <p className="text-sm text-muted-foreground">
                  Controls randomness: 0 is deterministic, 1 is very creative
                </p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="max-tokens">Max Tokens</Label>
                <Input
                  id="max-tokens"
                  type="number"
                  value={maxTokens}
                  onChange={(e) => setMaxTokens(Number.parseInt(e.target.value))}
                />
                <p className="text-sm text-muted-foreground">Maximum number of tokens to generate in a response</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>System Prompt</CardTitle>
              <CardDescription>Define how the chatbot should behave</CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                value={systemPrompt}
                onChange={(e) => setSystemPrompt(e.target.value)}
                rows={6}
                className="resize-none"
              />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="scraping" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Scraping Settings</CardTitle>
              <CardDescription>Configure how content is scraped from the website</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="max-pages">Maximum Pages</Label>
                <Input id="max-pages" type="number" defaultValue="500" />
                <p className="text-sm text-muted-foreground">Limit the number of pages to scrape</p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="crawl-depth">Crawl Depth</Label>
                <Input id="crawl-depth" type="number" defaultValue="3" />
                <p className="text-sm text-muted-foreground">How many links deep to crawl from the starting URL</p>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="respect-robots">Respect robots.txt</Label>
                  <Switch id="respect-robots" defaultChecked />
                </div>
                <p className="text-sm text-muted-foreground">Follow robots.txt directives when crawling</p>
              </div>
            </CardContent>
            <CardFooter>
              <Button variant="outline">Start Scraping</Button>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Content Filters</CardTitle>
              <CardDescription>Configure which content to include or exclude</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="include-paths">Include Paths</Label>
                <Textarea id="include-paths" placeholder="/blog/*, /faq/*, /about/*" className="resize-none" rows={3} />
                <p className="text-sm text-muted-foreground">
                  Only scrape pages matching these patterns (comma-separated, supports * wildcard)
                </p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="exclude-paths">Exclude Paths</Label>
                <Textarea
                  id="exclude-paths"
                  placeholder="/admin/*, /login/*, /cart/*"
                  className="resize-none"
                  rows={3}
                />
                <p className="text-sm text-muted-foreground">
                  Skip pages matching these patterns (comma-separated, supports * wildcard)
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="advanced" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Advanced Settings</CardTitle>
              <CardDescription>Additional configuration options</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="streaming">Enable Streaming Responses</Label>
                  <Switch id="streaming" defaultChecked />
                </div>
                <p className="text-sm text-muted-foreground">Stream responses as they are generated</p>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="memory">Conversation Memory</Label>
                  <Switch id="memory" defaultChecked />
                </div>
                <p className="text-sm text-muted-foreground">Remember previous messages in the conversation</p>
              </div>
              <div className="space-y-2">
                <Label htmlFor="memory-limit">Memory Limit</Label>
                <Select defaultValue="10">
                  <SelectTrigger id="memory-limit">
                    <SelectValue placeholder="Select limit" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="5">5 messages</SelectItem>
                    <SelectItem value="10">10 messages</SelectItem>
                    <SelectItem value="20">20 messages</SelectItem>
                    <SelectItem value="50">50 messages</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-sm text-muted-foreground">Maximum number of previous messages to remember</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Danger Zone</CardTitle>
              <CardDescription>Destructive actions for this chatbot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Button variant="destructive">Reset Chatbot</Button>
                <p className="text-sm text-muted-foreground">Clear all data and settings for this chatbot</p>
              </div>
              <div className="space-y-2">
                <Button variant="destructive">Delete Chatbot</Button>
                <p className="text-sm text-muted-foreground">Permanently delete this chatbot and all associated data</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

