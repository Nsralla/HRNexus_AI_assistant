import { getApiUrl, getAuthToken } from './api.config';

export interface DocumentUploadResponse {
    message: string;
    file_name: string;
    file_size: number;
    chunks_created?: number;
}

export interface DocumentMetadata {
    id: string;
    filename: string;
    file_size: number;
    uploaded_at: string;
    status: 'processing' | 'completed' | 'failed';
}

export const documentService = {
    /**
     * Upload a single text file to be embedded in the vector database
     */
    async uploadDocument(file: File): Promise<DocumentUploadResponse> {
        const formData = new FormData();
        formData.append('file', file);

        const token = getAuthToken();
        const headers: Record<string, string> = {};

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${getApiUrl()}/api/documents/upload`, {
                method: 'POST',
                headers,
                body: formData,
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
                throw new Error(error.detail || 'Failed to upload document');
            }

            return response.json();
        } catch (error) {
            if (error instanceof TypeError && error.message.includes('fetch')) {
                throw new Error('Unable to connect to server. Please check your internet connection.');
            }
            throw error;
        }
    },

    /**
     * Upload multiple text files at once
     */
    async uploadMultipleDocuments(files: File[]): Promise<DocumentUploadResponse[]> {
        const uploadPromises = files.map(file => this.uploadDocument(file));
        return Promise.all(uploadPromises);
    },

    /**
     * Get list of uploaded documents
     */
    async getDocuments(): Promise<DocumentMetadata[]> {
        const token = getAuthToken();
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${getApiUrl()}/api/documents/`, {
                method: 'GET',
                headers,
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Failed to fetch documents' }));
                throw new Error(error.detail || 'Failed to fetch documents');
            }

            return response.json();
        } catch (error) {
            if (error instanceof TypeError && error.message.includes('fetch')) {
                throw new Error('Unable to connect to server. Please check your internet connection.');
            }
            throw error;
        }
    },

    /**
     * Delete a document by ID
     */
    async deleteDocument(documentId: string): Promise<void> {
        const token = getAuthToken();
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${getApiUrl()}/api/documents/${documentId}`, {
                method: 'DELETE',
                headers,
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Failed to delete document' }));
                throw new Error(error.detail || 'Failed to delete document');
            }
        } catch (error) {
            if (error instanceof TypeError && error.message.includes('fetch')) {
                throw new Error('Unable to connect to server. Please check your internet connection.');
            }
            throw error;
        }
    },
};

