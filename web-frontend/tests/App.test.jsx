import { render, screen } from "@testing-library/react"
import { describe, expect, test } from "vitest"
import App from "../src/App"

describe("App", () => {

    // Create individual test
    test("renders the app", () => {
        render(<App />) // Render App component in simulated DOM

        // Look for th string "summarai" in the simulated DOM and check result
        expect(screen.getByText(/summarai/i)).toBeInTheDocument()
    })

})
