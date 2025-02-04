interface ApiRequest {
    text: string;
    key?: number;
    keep_spaces?: boolean;
    keep_punctuation?: boolean;
    transform_case?: 'lowercase' | 'uppercase' | 'keep_case'
}

interface ErrorDetail {
    code: string;
    message: string;
    error_id?: string;
}

interface Metadata {
    key: number;
    confidence_level?: 'low' | 'medium' | 'high';
    analysis_length?: number;
}

interface ApiSolution {
    key: number;
    text: string;
    chi_squared_total?: number;
}

interface ApiText {
    text: string;
}

interface ApiResponse {
    success: boolean;
    data?: ApiSolution[] | ApiText[];
    error?: ErrorDetail;
    metadata?: Metadata;
}