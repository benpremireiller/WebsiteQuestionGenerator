import React from 'react';

function Question({question}){
    
    return (
        <p className="question">
        {question.question_text}
        {question.options}
        </p>

    )
}

export default Question;