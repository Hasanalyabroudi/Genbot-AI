"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { ArrowRight } from "lucide-react"

export default function NewChatbot() {
  const [step, setStep] = useState(1)
  const [name, setName] = useState("")
  const [url, setUrl] = useState("")
  const [model, setModel] = useState("gpt-4o")
  const [systemPrompt, setSystemPrompt] = useState(
    "You are a helpful assistant. Answer questions based on the information provided.",
  )
  const router = useRouter()

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1)
    } else {
      // In a real app, this would create the chatbot
      router.push("/admin/chatbots")
    }
  }

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1)
    }
  }

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Create New Chatbot</h2>
      </div>

      <div className="flex justify-between mb-8">
        <div className="flex items-center gap-2">
          <div
            className={`rounded-full w-8 h-8 flex items-center justify-center ${step >= 1 ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"}`}
          >
            1
          </div>
          <span className={step >= 1 ? "font-medium" : "text-muted-foreground"}>Basic Info</span>
        </div>
        <div className="h-0.5 flex-1 mx-4 bg-muted self-center">
          <div className={`h-full bg-primary ${step >= 2 ? "w-full" : "w-0"} transition-all duration-300`}></div>
        </div>
        <div className="flex items-center gap-2">
          <div
            className={`rounded-full w-8 h-8 flex items-center justify-center ${step >= 2 ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"}`}
          >
            2
          </div>
          <span className={step >= 2 ? "font-medium" : "text-muted-foreground"}>Model Settings</span>
        </div>
        <div className="h-0.5 flex-1 mx-4 bg-muted self-center">
          <div className={`h-full bg-primary ${step >= 3 ? "w-full" : "w-0"} transition-all duration-300`}></div>
        </div>
        <div className="flex items-center gap-2">
          <div
            className={`rounded-full w-8 h-8 flex items-center justify-center ${step >= 3 ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"}`}
          >
            3
          </div>
          <span className={step >= 3 ? "font-medium" : "text-muted-foreground"}>Scraping</span>
        </div>
      </div>

      {step === 1 && (
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
            <CardDescription>Enter the basic details for your new chatbot</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Chatbot Name</Label>
              <Input
                id="name"
                placeholder="e.g., University FAQ"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="url">Website URL</Label>
              <Input
                id="url"
                placeholder="e.g., example.com"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
              />
              <p className="text-sm text-muted-foreground">The website to scrape content from</p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="category">Category</Label>
              <Select defaultValue="education">
                <SelectTrigger id="category">
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="education">Education</SelectItem>
                  <SelectItem value="ecommerce">E-commerce</SelectItem>
                  <SelectItem value="technology">Technology</SelectItem>
                  <SelectItem value="healthcare">Healthcare</SelectItem>
                  <SelectItem value="finance">Finance</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                placeholder="Briefly describe what this chatbot will help users with"
                rows={3}
              />
            </div>
          </CardContent>
          <CardFooter className="flex justify-end">
            <Button onClick={handleNext} disabled={!name || !url}>
              Next
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </CardFooter>
        </Card>
      )}

      {step === 2 && (
        <Card>
          <CardHeader>
            <CardTitle>Model Settings</CardTitle>
            <CardDescription>Configure the AI model for your chatbot</CardDescription>
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
              <p className="text-sm text-muted-foreground">Select the AI model to power your chatbot</p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="temperature">Temperature</Label>
              <Select defaultValue="0.7">
                <SelectTrigger id="temperature">
                  <SelectValue placeholder="Select temperature" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0.3">0.3 (More focused)</SelectItem>
                  <SelectItem value="0.5">0.5 (Balanced)</SelectItem>
                  <SelectItem value="0.7">0.7 (Default)</SelectItem>
                  <SelectItem value="0.9">0.9 (More creative)</SelectItem>
                </SelectContent>
              </Select>
              <p className="text-sm text-muted-foreground">
                Controls randomness: lower values are more deterministic, higher values are more creative
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="system-prompt">System Prompt</Label>
              <Textarea
                id="system-prompt"
                value={systemPrompt}
                onChange={(e) => setSystemPrompt(e.target.value)}
                rows={6}
              />
              <p className="text-sm text-muted-foreground">Instructions that define how the chatbot should behave</p>
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button variant="outline" onClick={handleBack}>
              Back
            </Button>
            <Button onClick={handleNext}>
              Next
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </CardFooter>
        </Card>
      )}

      {step === 3 && (
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
              <Select defaultValue="3">
                <SelectTrigger id="crawl-depth">
                  <SelectValue placeholder="Select depth" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">1 (Homepage only)</SelectItem>
                  <SelectItem value="2">2 (Homepage + direct links)</SelectItem>
                  <SelectItem value="3">3 (Default)</SelectItem>
                  <SelectItem value="5">5 (Deep crawl)</SelectItem>
                  <SelectItem value="10">10 (Very deep crawl)</SelectItem>
                </SelectContent>
              </Select>
              <p className="text-sm text-muted-foreground">How many links deep to crawl from the starting URL</p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="include-paths">Include Paths (Optional)</Label>
              <Textarea id="include-paths" placeholder="/blog/*, /faq/*, /about/*" className="resize-none" rows={3} />
              <p className="text-sm text-muted-foreground">
                Only scrape pages matching these patterns (comma-separated, supports * wildcard)
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="exclude-paths">Exclude Paths (Optional)</Label>
              <Textarea id="exclude-paths" placeholder="/admin/*, /login/*, /cart/*" className="resize-none" rows={3} />
              <p className="text-sm text-muted-foreground">
                Skip pages matching these patterns (comma-separated, supports * wildcard)
              </p>
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button variant="outline" onClick={handleBack}>
              Back
            </Button>
            <Button onClick={handleNext}>Create Chatbot</Button>
          </CardFooter>
        </Card>
      )}
    </div>
  )
}

