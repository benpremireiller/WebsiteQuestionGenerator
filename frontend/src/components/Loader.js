import React from 'react';

function Loader({loading}){
    
    if (!loading) {
        return 
    }

    return (
        <div class="loading-dots">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    )
}

export default Loader;