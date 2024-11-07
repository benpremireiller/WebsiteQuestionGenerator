import './App.css';
import React, { useState } from 'react';
import Questions from './components/Questions'

function App() {

  const [url, setURL] = useState('');
  const [questions, SetQuestions] = useState('')

  const getSurveyQuestion = async () => {
    const endpoint = `api/questions?url=${url}`

    try {
      const response = await fetch(endpoint)
      const responseQuestions = await response.json()
      SetQuestions(responseQuestions)

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
          <p></p>
          <Questions questions={questions}/>
      </header>
    </div>
  );
}

export default App;
