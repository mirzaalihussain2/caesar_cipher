export function toSnakeCase(obj: Record<string, any>): Record<string, any> {
    if (Array.isArray(obj)) {
        return obj.map(item => toSnakeCase(item));
    }
    
    if (obj !== null && typeof obj === 'object') {
        const snakeObj: Record<string, any> = {};
        
        for (const [key, value] of Object.entries(obj)) {
            const snakeKey = key.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
            snakeObj[snakeKey] = typeof value === 'object' ? toSnakeCase(value) : value;
        }
        
        return snakeObj;
    }
    
    return obj;
}

export function toCamelCase(obj: Record<string, any>): Record<string, any> {
    if (Array.isArray(obj)) {
        return obj.map(item => toCamelCase(item));
    }
    
    if (obj !== null && typeof obj === 'object') {
        const camelObj: Record<string, any> = {};
        
        for (const [key, value] of Object.entries(obj)) {
            const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
            camelObj[camelKey] = typeof value === 'object' ? toCamelCase(value) : value;
        }
        
        return camelObj;
    }
    
    return obj;
}