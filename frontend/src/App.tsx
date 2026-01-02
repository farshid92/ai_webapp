import { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<number | null>(null);

  const handlePredict = async () => {
    try {
      const inputs = input
        .split(",")
        .map((v) => Number(v.trim()))
        .filter((v) => !isNaN(v));

      if (inputs.length === 0) {
        alert("Please enter at least one valid number");
        return;
      }

      const response = await fetch("/api/predict/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          inputs: inputs,
          model_name: "base"
        }),
      });

      if (!response.ok) {
        // Try to parse as JSON, but handle HTML error pages
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        try {
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.includes("application/json")) {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorData.message || errorMessage;
          } else {
            const text = await response.text();
            errorMessage = `Server error: ${text.substring(0, 100)}`;
          }
        } catch (e) {
          errorMessage = `Failed to parse error response: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      // Check if response is JSON before parsing
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const text = await response.text();
        throw new Error(`Expected JSON but got: ${contentType}. Response: ${text.substring(0, 100)}`);
      }

      const data = await response.json();
      setResult(data.prediction);
    } catch (error) {
      console.error("Prediction error:", error);
      alert(`Error: ${error instanceof Error ? error.message : "Failed to get prediction"}`);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>AI Prediction Demo</h1>

      <input
        type="text"
        placeholder="1, 2, 3, 4"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: "300px", padding: "0.5rem" }}
      />

      <br /><br />

      <button onClick={handlePredict}>Predict</button>

      {result !== null && (
        <p>
          <strong>Prediction:</strong> {result}
        </p>
      )}
    </div>
  );
}

export default App;
