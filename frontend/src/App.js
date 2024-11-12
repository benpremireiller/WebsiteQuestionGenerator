import './App.css';
import React, { useState } from 'react';
import Questions from './components/Questions'
import Loader from './components/Loader'
import { FaArrowAltCircleUp } from "react-icons/fa";

function App() {

  const [url, setURL] = useState('');
  const [questions, setQuestions] = useState('')
  const [loading, setLoading] = useState(false)

  const getSurveyQuestion = async () => {

    setQuestions('')
    const endpoint = `api/questions?url=${url}`

    try {
      setLoading(true)
      const response = await fetch(endpoint)
      const responseQuestions = await response.json()
      setLoading(false)
      setQuestions(responseQuestions)

    } catch (error) {
      setLoading(false)
      return alert("Error. Unable to retreive question.")
    }
  };

  return ( 
    <>
    <body>
      <header className="header">
        <div>Website Question Generator</div>
      </header>
      <div className='main'>
        <h2>Generate survey questions for any website dynamically.</h2>
        <div className='url-input-container'>
            <input 
              className='url-input-box'
              type="text" 
              placeholder="URL"
              value={url}
              onChange={e => setURL(e.target.value)}
            />
            <button className='url-send-button' onClick={getSurveyQuestion}><FaArrowAltCircleUp size={22}/></button>
        </div>
        <p></p>
        <Loader loading={loading}/>
        <Questions questions={questions}/>
      </div>
    </body>
    <footer>
      <p>&copy; Benjamin Premi-Reiller</p>
    </footer>
    </>
  );
}

export default App;
