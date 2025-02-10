import { FormField, FormItem, FormLabel, FormControl } from "@/components/ui/form";
import { UseFormReturn } from "react-hook-form";
import { Switch } from "@/components/ui/switch";
import { FormData } from "@/lib/types";

interface FormSwitchProps {
    form: UseFormReturn<FormData>;
    name: keyof Pick<FormData, 'keepSpaces' | 'keepPunctuation'>;
    onLabel: string;
    offLabel: string;
}

const FormSwitch = ({ form, name, onLabel, offLabel }: FormSwitchProps) => (
    <FormField
        control={form.control}
        name={name}
        render={({ field }) => (
            <FormItem className="flex flex-row items-center justify-between gap-2">
                <FormLabel className="!mt-0">
                    {field.value ? onLabel : offLabel }
                </FormLabel>
                <FormControl className="flex items-center">
                    <Switch
                        checked={field.value}
                        onCheckedChange={field.onChange}
                    />
                </FormControl>
            </FormItem>
        )}
    />
)

export { FormSwitch }
