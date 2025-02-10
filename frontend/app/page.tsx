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
    <main className="container mx-auto my-6 px-4 max-w-5xl">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FormField
            control={form.control}
            name="text"
            render={({ field }) => (
              <FormItem>
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

          <div className="flex 
            flex-col space-y-2
            sm:flex-row justify-between items-center"
          >
            <FormField
              control={form.control}
              name="key"
              render={({ field }) => (
                <FormItem className="min-w-[13rem] w-[13rem] max-w-[13rem]">
                  <FormControl>
                    <Input
                      type="number"
                      placeholder="Encryption key"
                      className="text-center"
                      {...field}
                      value={field.value ?? ''}  // Convert null/undefined to empty string
                      onChange={(e) => {
                        const value = e.target.value;
                        field.onChange(value ? parseInt(value) : undefined);
                      }}
                    />
                  </FormControl>
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="transformCase"
              render={({ field }) => (
                <FormItem className="min-w-[13rem] w-[13rem] max-w-[13rem]">
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger className="text-center">
                        <SelectValue placeholder="Select case of return text" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent className="min-w-[13rem] w-[13rem] max-w-[13rem]">
                      <SelectItem value="keep_case">Keep case</SelectItem>
                      <SelectItem value="lowercase">Lowercase</SelectItem>
                      <SelectItem value="uppercase">Uppercase</SelectItem>
                    </SelectContent>
                  </Select>
                </FormItem>
              )}
            />

            <FormSwitch
              form={form}
              onLabel="Keep whitespace"
              offLabel="Remove whitespace"
              name="keepSpaces"
            />

            <FormSwitch
              form={form}
              onLabel="Keep punctuation"
              offLabel="Remove punctuation"
              name="keepPunctuation"
            />

          </div>

          <div className="flex flex-row w-full gap-4">
            <FormField
              control={form.control}
              name="action"
              render={({ field }) => (
                <Button 
                  type="submit" 
                  size="lg"
                  className="flex-1 text-base sm:text-sm md:text-base" 
                  onClick={() => field.onChange("encrypt" satisfies Action)}
                >
                  Encrypt
                </Button>
              )}
            />

            <FormField
              control={form.control}
              name="action"
              render={({ field }) => (
                <Button 
                  type="submit" 
                  size="lg"
                  className="flex-1 text-base sm:text-sm md:text-base" 
                  onClick={() => field.onChange(form.watch("key") === undefined ? "hack" : "decrypt" satisfies Action)}
                >
                  {form.watch("key") == undefined ? "Hack" : "Decrypt"}
                </Button>
              )}
            />
          </div>

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