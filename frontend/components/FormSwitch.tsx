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
            <FormItem className="flex flex-row min-w-[13rem] w-[13rem] max-w-[13rem] p-2 h-10 space-x-2 rounded-sm border shadow-sm">
                {/*
                    Set label width by field.value, rather than just making it big. UI looks better this way.
                    field.value ?                 
                
                */}
                <FormLabel className="flex flex-col justify-center mt-2 mb-1 mx-0 p-0 w-40">
                    <p className="text-center">
                        {field.value ? onLabel : offLabel }
                    </p>
                </FormLabel>
                <div className="flex flex-col justify-center mb-1 mt-0 mx-0 p-0">
                    <FormControl className="m-0 p-0">
                        <Switch
                            checked={field.value}
                            onCheckedChange={field.onChange}
                        />
                    </FormControl>
                </div>

            </FormItem>
        )}
    />
)

export { FormSwitch }
