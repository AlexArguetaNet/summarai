import { Button } from "./components/ui/button"
import { useState } from "react"

function App() {

  const [isClicked, setIsClicked] = useState(false)

  return (
    <>
      <Button variant="secondary" className="bg-emerald-200">El Boton</Button>
    </>
  )
}

export default App
