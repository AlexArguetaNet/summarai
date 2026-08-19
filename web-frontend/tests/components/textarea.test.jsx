import { render, screen } from "@testing-library/react"
import { describe, test, expect } from "vitest"
import { Textarea } from "@/components/ui/textarea"
import userEvent from "@testing-library/user-event"

describe("TextArea", () => {

    test("render Textarea", () => {
        render(<Textarea placeholder="Enter your text here..." />)
        expect(
            screen.getByPlaceholderText(/Enter your text here.../i)
        ).toBeInTheDocument()
    })

    test("allows user to enter text", async () => {
        const user = userEvent.setup() // Create mock user

        // Render the text area and store the textarea in a variable
        render(<Textarea placeholder="Enter your text here..."/>)
        const textarea = screen.getByPlaceholderText(/Enter your text here.../i)

        // Simulate typing action
        await user.type(textarea, "Hello world!")

        // Check result
        expect(textarea).toHaveValue("Hello world!")

    })
    
})