/**
 * v0 by Vercel.
 * @see https://v0.dev/t/5IPL1g7ucTw
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
import { CardTitle, CardDescription, CardHeader, CardContent, Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"


export default function Component() {
  return (
    <div className="grid md:grid-cols-[1fr_1fr] gap-4 w-full max-w-6xl rounded-xl mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Word Cloud Generator</CardTitle>
          <CardDescription>Create a unique word cloud based on your text and shape.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <div className="space-y-2">
              <Label htmlFor="text-input">Your Text</Label>
              <Textarea id="text-input" placeholder="Enter your text here..." />
            </div>
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <Label htmlFor="shape">Shape</Label>
              <Input id="shape" type="file" />
            </div>
            <Button>Generate Word Cloud</Button>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Your Word Cloud</CardTitle>
          <CardDescription>The word cloud generated from your text and shape.</CardDescription>
        </CardHeader>
        <CardContent>
          
          <Button className="mt-4">Download Image</Button>
        </CardContent>
      </Card>
    </div>
  )
}

