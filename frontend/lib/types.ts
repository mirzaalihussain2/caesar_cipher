import { z } from "zod";

interface ApiRequest {
    text: string;
    key?: number;
    keepSpaces?: boolean;
    keepPunctuation?: boolean;
    transformCase?: 'lowercase' | 'uppercase' | 'keep_case';
}

interface ErrorDetail {
    code: string;
    message: string;
    errorId?: string;
}

interface Metadata {
    key: number;
    confidenceLevel?: 'low' | 'medium' | 'high';
    analysisLength?: number;
}

interface ApiSolution {
    key: number;
    text: string;
    chiSquaredTotal?: number;
}

interface ApiText {
    text: string;
}

interface ApiResponse {
    success: boolean;
    data?: (ApiSolution | ApiText)[];
    error?: ErrorDetail;
    metadata?: Metadata;
}