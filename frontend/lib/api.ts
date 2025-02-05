import { toCamelCase, toSnakeCase } from "./transform";
import { ApiRequest, Endpoint, ApiResponse, ApiResponseSchema } from "./types";
import { EndpointSchema, ApiRequestSchema } from "./types";

const API_URL = new URL(process.env.NEXT_PUBLIC_API_URL as string);

export async function apiRequest(endpoint: Endpoint, request: ApiRequest): Promise<ApiResponse> {
    // Validate at runtime
    const validEndpoint = EndpointSchema.parse(endpoint);
    const validRequest = ApiRequestSchema.parse(request);

    try {
        const response = await fetch(`${API_URL}${validEndpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(toSnakeCase(validRequest)),
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