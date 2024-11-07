import React from 'react';

function Question({question}){
    
    if (question === ''){
        return
    }

    return (
        <div className="question">
        {question.question_text}
        <ol>
        {question.options.map((q, i) => (
            <li>{q}</li>
            ))}
        </ol>
        </div>

    )
}

export default Question;