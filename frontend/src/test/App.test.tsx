import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../App'

// Mock fetch globally
global.fetch = vi.fn()

describe('App Component', () => {
    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('renders the main heading', () => {
        render(<App />)
        expect(screen.getByText('AI Prediction Demo')).toBeInTheDocument()
    })

    it('renders input field and button', () => {
        render(<App />)
        expect(screen.getByPlaceholderText('1, 2, 3, 4')).toBeInTheDocument()
        expect(screen.getByRole('button', { name: /predict/i })).toBeInTheDocument()
    })

    it('allows user to type in input field', async () => {
        const user = userEvent.setup()
        render(<App />)

        const input = screen.getByPlaceholderText('1, 2, 3, 4')
        await user.type(input, '1, 2, 3')

        expect(input).toHaveValue('1, 2, 3')
    })

    it('calls API when predict button is clicked', async () => {
        const user = userEvent.setup()
        const mockFetch = vi.mocked(fetch)

        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ prediction: 42 }),
        } as Response)

        render(<App />)

        const input = screen.getByPlaceholderText('1, 2, 3, 4')
        const button = screen.getByRole('button', { name: /predict/i })

        await user.type(input, '1, 2, 3, 4')
        await user.click(button)

        await waitFor(() => {
            expect(mockFetch).toHaveBeenCalledWith('/api/predict/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ inputs: [1, 2, 3, 4], model_name: 'base' }),
            })
        })
    })

    it('displays prediction result after successful API call', async () => {
        const user = userEvent.setup()
        const mockFetch = vi.mocked(fetch)

        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ prediction: 42.5 }),
        } as Response)

        render(<App />)

        const input = screen.getByPlaceholderText('1, 2, 3, 4')
        const button = screen.getByRole('button', { name: /predict/i })

        await user.type(input, '1, 2, 3, 4')
        await user.click(button)

        await waitFor(() => {
            expect(screen.getByText(/prediction:/i)).toBeInTheDocument()
            expect(screen.getByText('42.5')).toBeInTheDocument()
        })
    })

    it('handles empty input gracefully', async () => {
        const user = userEvent.setup()
        const mockFetch = vi.mocked(fetch)

        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ prediction: 0 }),
        } as Response)

        render(<App />)

        const button = screen.getByRole('button', { name: /predict/i })
        await user.click(button)

        await waitFor(() => {
            expect(mockFetch).toHaveBeenCalledWith('/api/predict/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ inputs: [0], model_name: 'base' }), // Empty string becomes [0] after Number("")
            })
        })
    })

    it('filters out non-numeric values from input', async () => {
        const user = userEvent.setup()
        const mockFetch = vi.mocked(fetch)

        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ prediction: 10 }),
        } as Response)

        render(<App />)

        const input = screen.getByPlaceholderText('1, 2, 3, 4')
        const button = screen.getByRole('button', { name: /predict/i })

        await user.type(input, '1, abc, 2, xyz, 3')
        await user.click(button)

        await waitFor(() => {
            expect(mockFetch).toHaveBeenCalledWith('/api/predict/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ inputs: [1, 2, 3], model_name: 'base' }),
            })
        })
    })
})

