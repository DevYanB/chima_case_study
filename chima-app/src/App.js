import React, { useState } from 'react';
import './App.css';


function App() {
  const [creativityLevel, setCreativityLevel] = useState(2);  // 0: Not Creative, 4: Very Creative
  const [tone, setTone] = useState(2);  // 0: Formal, 4: Casual
  const [style, setStyle] = useState('direct');
  const [keywords, setKeywords] = useState("");
  const [sentences, setSentences] = useState([]);

  const handleSubmit = async () => {
    // Replace with your backend API endpoint
    const API_ENDPOINT = "http://127.0.0.1:5000/generate";

    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        creativityLevel,
        tone,
        style,
        keywords
      })
    });

    const data = await response.json();
    console.log(data)
    if (data && data.sentences) {
      setSentences(data.sentences);
    } else {
        console.error('Unexpected data structure:', data);
        setSentences([]);
    }
  };

  const handleFeedback = async (feedback, sentenceText) => {
    const FEEDBACK_API_ENDPOINT = "http://127.0.0.1:5000/feedback";
  
    const response = await fetch(FEEDBACK_API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        creativityLevel,
        tone,
        style,
        keywords,
        sentence: sentenceText,
        feedback: feedback  // either "thumbs_up" or "thumbs_down"
      })
    });
  
    const data = await response.json();
    console.log(data);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <label>
            Creativity Level: {['Not Creative', 'Slightly Creative', 'Moderately Creative', 'Quite Creative', 'Very Creative'][creativityLevel]}
            <input
              type="range"
              min="0"
              max="4"
              step="1"
              value={creativityLevel}
              onChange={e => setCreativityLevel(e.target.value)}
            />
          </label>
        </div>

        <div>
          <label>
            Tone: {['Formal', 'Slightly Formal', 'Neutral', 'Slightly Casual', 'Casual'][tone]}
            <input
              type="range"
              min="0"
              max="4"
              step="1"
              value={tone}
              onChange={e => setTone(e.target.value)}
            />
          </label>
        </div>

        <div>
          <label>
            Style:
            <select value={style} onChange={e => setStyle(e.target.value)}>
              <option value="humorous">Humorous</option>
              <option value="direct">Direct</option>
              <option value="ambivalent">Ambivalent</option>
            </select>
          </label>
        </div>

        <div>
          <label>
            Keywords:
            <input
              type="text"
              value={keywords}
              onChange={e => setKeywords(e.target.value)}
            />
          </label>
        </div>

        <button onClick={handleSubmit}>Submit</button>

        <div className="sentences">
          {sentences.map((sentence, index) => (
            <div key={index} className="sentence">
            {sentence}
            <button onClick={() => handleFeedback("thumbs_up", sentence)}>👍</button>
            <button onClick={() => handleFeedback("thumbs_down", sentence)}>👎</button>
          </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;
