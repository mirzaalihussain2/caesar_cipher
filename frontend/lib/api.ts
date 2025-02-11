import { toCamelCase, toSnakeCase } from "./transform";
import { Action, ApiRequest, ApiResponse, ApiResponseSchema } from "./types";
import { EndpointSchema, ApiRequestSchema } from "./types";

const API_URL = new URL(process.env.NEXT_PUBLIC_API_URL as string);

export async function apiRequest(action: Action, request: ApiRequest): Promise<ApiResponse> {
    const endpoint = EndpointSchema.parse(action);
    const validRequest = ApiRequestSchema.parse(request);

    const cleanRequest = action === 'hack' 
        ? { ...validRequest, key: undefined }
        : validRequest;

    try {
        console.log("API has been called!")
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(toSnakeCase(cleanRequest)),
            signal: AbortSignal.timeout(20000),
        })

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return ApiResponseSchema.parse(toCamelCase(data))
    } catch (error) {
        if (error instanceof Error) {
            console.error(`Failed to fetch transactions: ${error.message}`);
        } else {
            console.error('An unknown error occurred while fetching transactions');
        }
        throw error;
    }
}