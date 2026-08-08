import { Button } from "./components/ui/button"
import { Textarea } from "./components/ui/textarea"
import { Spinner } from "./components/ui/spinner"
import { useState } from "react"
import { GiSamuraiHelmet } from "react-icons/gi"
import { fetchSummary } from "./api/summary"
import { Alert, AlertTitle, AlertDescription, AlertAction } from "./components/ui/alert"
import { AlertCircleIcon } from "lucide-react"

function App() {

  const [text, setText] = useState("");
  const [charCount, setCharCount] = useState(0);
  const [summaryArr, setSummaryArr] = useState([]);
  const [summaryStr, setSummaryStr] = useState("");
  const [disableButton, setDisableButton] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isCopied, setIsCopied] = useState(false)
  const [errorExists, setErrorExists] = useState(false);
  const [errorDescription, setErrorDescription] = useState("");

  const handleClick = async (e) => {

    // Prevent default submit behavior
    e.preventDefault();

    setIsLoading(true);
    setDisableButton(true);

    try {
      const summary = await fetchSummary(text);
      setSummaryArr(summary.summaryArray);
      setSummaryStr(summary.summaryString);
      setErrorExists(false)

    } catch (error) {
      setErrorExists(true);
      setErrorDescription(error.message);
      setDisableButton(false);
    }

    setIsLoading(false);

  }

  const handleTextChange = (text) => {
    // Check character count, omitting whitespace
    setCharCount(text.trim().replace(" ", "").length);

    // Set the text value
    setText(text);

  }

  const handleClear = () => {
    setSummaryArr("");
    setText("");
    setCharCount(0);
    setIsCopied(false);
    setDisableButton(false);
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(summaryStr);
    setIsCopied(true);
  }

  return (
    <>
      <div className="mx-auto my-7 max-w-[700px] p-4 bg-gray-50 shadow-md">
        <h1 className="flex align-middle text-4xl pb-5">Summarai <GiSamuraiHelmet /></h1>

        {/* Will render if there are errors */}
        {
          errorExists && 
            <Alert variant="destructive">
              <AlertCircleIcon />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription className="text-black!">{errorDescription}</AlertDescription>
              <AlertAction>
                <Button onClick={() => setErrorExists(false)} size="xs" className="bg-red-400">
                  X
                </Button>
              </AlertAction>
            </Alert>
        }

        <form onSubmit={(e) => handleClick(e)}>
          <Textarea 
            className="h-72 resize-none text-xl mt-1" 
            placeholder="Enter your text here" 
            value={text}
            onChange={(e) => handleTextChange(e.target.value)}
            required
          />

          <div className="flex justify-between py-5">
            <Button type="submit" disabled={disableButton} className="bg-green-400 text-black">Summarize</Button>
            <p>Character count | {charCount}</p>
          </div>

        </form>

        <div className="flex justify-center">
          {
            isLoading && <Spinner className="size-7" />
          }
          {
            summaryArr.length > 0 && 
              <div className="">
                <div className="px-10">
                  {
                    summaryArr.map((elem, index) => (
                      <li key={index}>{elem}</li>
                    ))
                  }
                </div>
                <div className="flex justify-end mt-5">
                  
                  {isCopied && <p>Copied!</p>}
                  <Button onClick={handleCopy}>Copy</Button>
                  <Button onClick={handleClear} className="bg-green-400 text-black">New</Button>
                </div>
              </div>
          }
        </div>

      </div>
    </>
  )
}

export default App
