import { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<number | null>(null);

  const handlePredict = async () => {
    const values = input
      .split(",")
      .map((v) => Number(v.trim()))
      .filter((v) => !isNaN(v));

    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ values }),
    });

    const data = await response.json();
    setResult(data.prediction);
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
