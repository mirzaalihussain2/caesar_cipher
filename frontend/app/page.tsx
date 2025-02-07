"use client"

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
 
import { toast } from "@/components/hooks/use-toast";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { ApiRequest, ApiRequestSchema, Endpoint, FormSchema, FormData } from "@/lib/types";
import { apiRequest } from "@/lib/api";


export default function Home() {
  const form = useForm<FormData>({
    resolver: zodResolver(FormSchema),
  })

  function onSubmit(formData: z.infer<typeof FormSchema>) {
    const response = apiRequest(formData.action, formData)
    
    return toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify({formData}, null, 2)}</code>
        </pre>
      ),
    })
  }

  return (
    <main className="container mx-auto px-4 max-w-3xl">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 space-y-6">
          <FormField
            control={form.control}
            name="text"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Text</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="Tell us a little bit about yourself"
                    className="resize-none"
                    {...field}
                  />
                </FormControl>
                <FormDescription>
                  You can <span>@mention</span> other users and organisations.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="key"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Key</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                  />
                </FormControl>
                <FormDescription>
                  Encryption key
                </FormDescription>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="keepSpaces"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Keep spaces</FormLabel>
                <FormControl>
                  <Switch
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="keepPunctuation"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Keep punctuation</FormLabel>
                <FormControl>
                  <Switch
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="transformCase"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Transform Case </FormLabel>
                <Select onValueChange={field.onChange} defaultValue={field.value}>
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select case of return text" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="keep_case">Keep case</SelectItem>
                    <SelectItem value="lowercase">Lowercase</SelectItem>
                    <SelectItem value="uppercase">Uppercase</SelectItem>
                  </SelectContent>
                </Select>
              </FormItem>
            )}
          />

          <Button type="submit">Encrypt</Button>
          <Button type="submit">Decrypt</Button>
          <Button type="submit">Hack</Button>
        </form>
      </Form>
    </main>
  );
}