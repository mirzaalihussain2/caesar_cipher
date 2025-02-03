"use client"

import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
 
import { toast } from "@/components/hooks/use-toast"


export default function Home() {
  return (
    <main className="container mx-auto px-4 max-w-3xl">
      <div>
        <Textarea></Textarea>
      </div>

    </main>
  );
}