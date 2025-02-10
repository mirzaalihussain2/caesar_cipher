"use client"

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { FormSwitch } from '@/components/FormSwitch';
import { Textarea } from "@/components/ui/textarea";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
 
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { ApiRequest, ApiRequestSchema, Endpoint, FormSchema, FormData, Action, ApiResponse } from "@/lib/types";
import { apiRequest } from "@/lib/api";
import { useState } from "react";


export default function Home() {
  const [response, setResponse] = useState<ApiResponse | null>(null)
  const form = useForm<FormData>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      text: "",
      key: undefined,
      keepSpaces: true,
      keepPunctuation: true,
      transformCase: "keep_case"
    }
  })

  async function onSubmit(formData: z.infer<typeof FormSchema>) {
    const response = await apiRequest(formData.action, formData)
    console.log(response)
    setResponse(response)
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
                    placeholder="Text to encrypt, decrypt or hack"
                    className="resize-none"
                    {...field}
                  />
                </FormControl>
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
                    type="number"
                    {...field}
                    value={field.value ?? ''}  // Convert null/undefined to empty string
                    onChange={(e) => {
                      const value = e.target.value;
                      field.onChange(value ? parseInt(value) : undefined);
                    }}
                  />
                </FormControl>
                <FormDescription>
                  Encryption key
                </FormDescription>
              </FormItem>
            )}
          />

          <div className="flex flex-row">
            <FormSwitch
              form={form}
              onLabel="Keep spaces"
              offLabel="Remove spaces"
              name="keepSpaces"
            />

            <FormSwitch
              form={form}
              onLabel="Keep punctuation"
              offLabel="Remove punctuation"
              name="keepPunctuation"
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
          </div>


          <FormField
            control={form.control}
            name="action"
            render={({ field }) => (
              <Button type="submit" onClick={() => field.onChange("encrypt" satisfies Action)}>
                Encrypt
              </Button>
            )}
          />

          <FormField
            control={form.control}
            name="action"
            render={({ field }) => (
              <Button type="submit" onClick={() => field.onChange("decrypt" satisfies Action)}>
                Decrypt
              </Button>
            )}
          />

          <FormField
            control={form.control}
            name="action"
            render={({ field }) => (
              <Button type="submit" onClick={() => field.onChange("hack" satisfies Action)}>
                Hack
              </Button>
            )}
          />

        </form>
      </Form>

      {response?.data && (
        <div className="w-2/3 space-y-6">
          <h2 className="font-semibold mb-2">Result:</h2>
          <p>{response.data[0].text}</p>
        </div>
      )}
    </main>
  );
}