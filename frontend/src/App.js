import './App.css';
import React, { useState } from 'react';
import Question from './components/Question'

function App() {

  const [url, setURL] = useState('');
  const [question, SetQuestion] = useState('')

  const getSurveyQuestion = async () => {
    const endpoint = `api/questions?url=${url}`

    try {
      const response = await fetch(endpoint)
      const responseQuestion = await response.json()
      SetQuestion(responseQuestion)

    } catch (error) {
      return alert("Error. Unable to retreive question.")
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h3>Enter a URL</h3>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <input 
              type="text" 
              placeholder="URL"
              value={url}
              onChange={e => setURL(e.target.value)}
              id="webpage"
            />
            <button onClick={getSurveyQuestion}>Send</button>
          </div>
          <Question question={question}/>
      </header>
    </div>
  );
}

export default App;
