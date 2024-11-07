import React from 'react';
import Question from './Question'

function Questions({questions}){
    
    if (questions === ''){
        return
    }

    return (
        <div className="all-questions">
            {questions.map((q) => (
                <Question question={q}></Question>
            ))}
        </div>
    )
    
}

export default Questions;