"use client"

import { TypingAnimation } from "@/components/ui/typing-animation";
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

          <div className="grid grid-cols-1 gap-4 w-full justify-center
            sm:flex sm:flex-row sm:justify-center sm:items-center">
            <div className="grid grid-cols-2 gap-x-[10%] gap-y-4 w-full max-w-4xl
              sm:flex sm:flex-row sm:justify-between sm:items-center sm:gap-4">
              <div className="flex flex-col gap-4 w-full justify-center
                sm:flex-row sm:gap-4">
                <FormField
                  control={form.control}
                  name="key"
                  render={({ field }) => (
                    <FormItem className="flex-1 min-w-[48%] sm:min-w-[13rem]">
                      <FormControl>
                        <Input
                          type="number"
                          placeholder="Encryption key"
                          className="text-center h-10"
                          {...field}
                          value={field.value ?? ''}
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
                    <FormItem className="flex-1 min-w-[48%] sm:min-w-[13rem]">
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger className="text-center">
                            <SelectValue placeholder="Select case of return text" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent className="min-w-[13rem] w-full">
                          <SelectItem value="keep_case">Keep case</SelectItem>
                          <SelectItem value="lowercase">Lowercase</SelectItem>
                          <SelectItem value="uppercase">Uppercase</SelectItem>
                        </SelectContent>
                      </Select>
                    </FormItem>
                  )}
                />
              </div>

              <div className="flex flex-col gap-4 w-full justify-center
                sm:flex-row sm:gap-4">
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
            </div>
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
        <div className="space-y-6">

        <TypingAnimation
          className="text-4xl font-bold text-black dark:text-white"
          text={response.data[0].text}
        />
          {/* <h2 className="font-semibold mb-2">Result:</h2>
          <p>{response.data[0].text}</p> */}
        </div>
      )}
    </main>
  );
}