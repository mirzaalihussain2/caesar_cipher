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
            <FormItem className="flex flex-row m-0 p-0 border-2 border-blue-700">
                {/* Set label width by field.value, rather than just making it big. UI looks better this way. */}
                <FormLabel className="flex flex-col justify-center mt-2 mb-0 mx-0 p-0 w-24 sm:w-28 lg:w-36">
                    <p className="text-center">
                        {field.value ? onLabel : offLabel }
                    </p>
                </FormLabel>
                <div className="flex flex-col justify-center m-0 p-0">
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
